package com.codesynergy.horizon.mobile.session

class BluetoothSessionEngine(
    private val store: SelectedDeviceStore,
    private val connectionFactory: (SelectedBluetoothDevice) -> com.codesynergy.horizon.mobile.bluetooth.ObdConnection?,
    private val logger: BluetoothSessionLogger = NoopBluetoothSessionLogger,
    private val sleeper: (Long) -> Unit = { Thread.sleep(it) },
) {
    private val manager = BluetoothConnectionManager(store, connectionFactory, logger)
    private var pollingLoop: PidPollingLoop? = null

    var state: BluetoothSessionState = BluetoothSessionState.DISCONNECTED
        private set

    var reconnectAttempts: Int = 0
        private set

    var lastCommand: String? = null
        private set

    var lastResponse: String? = null
        private set

    var lastError: String? = null
        private set

    val selectedDevice: SelectedBluetoothDevice
        get() = manager.selectedDevice

    fun select(device: SelectedBluetoothDevice) {
        manager.select(device)
        reconnectAttempts = 0
        lastError = null
    }

    fun clearSelection() {
        disconnect()
        manager.clearSelection()
    }

    fun connect(): Boolean {
        if (state == BluetoothSessionState.CONNECTED || state == BluetoothSessionState.READING) {
            return true
        }
        state = BluetoothSessionState.CONNECTING
        return openAndInitialize()
    }

    fun startReading(): Boolean {
        if (!connect()) {
            return false
        }
        state = BluetoothSessionState.READING
        return true
    }

    fun stopReading() {
        state = BluetoothSessionState.STOPPING
        manager.close()
        pollingLoop = null
        state = BluetoothSessionState.DISCONNECTED
    }

    fun disconnect() {
        state = BluetoothSessionState.STOPPING
        manager.close()
        pollingLoop = null
        state = BluetoothSessionState.DISCONNECTED
    }

    fun readAndPublish(assetReference: String, publisher: ObservationPublisher): ReadCycleResult? {
        if (state != BluetoothSessionState.READING) {
            if (!startReading()) return null
        }
        val readings = runCatching {
            requireNotNull(pollingLoop).readOnce()
        }.getOrElse { error ->
            lastError = error.message ?: error::class.java.simpleName
            logger.log("[Bluetooth] read timeout ${lastError.orEmpty()}")
            reconnectSameMac()
            return null
        }
        val publishResult = publisher.publish(assetReference, readings)
        return ReadCycleResult(readings = readings, latencyMs = publishResult.latencyMs)
    }

    private fun reconnectSameMac(): Boolean {
        state = BluetoothSessionState.RECONNECTING
        manager.close()
        pollingLoop = null
        logger.log("[Bluetooth] reconnecting same MAC ${selectedDevice.address}")
        for (delayMs in BACKOFF_MS) {
            reconnectAttempts += 1
            sleeper(delayMs)
            if (openAndInitialize(reconnecting = true)) {
                state = BluetoothSessionState.READING
                return true
            }
        }
        state = BluetoothSessionState.ERROR
        lastError = "Não foi possível reconectar ao dispositivo selecionado."
        return false
    }

    private fun openAndInitialize(reconnecting: Boolean = false): Boolean =
        runCatching {
            val connection = manager.openSelected()
            state = BluetoothSessionState.INITIALIZING
            val protocol = Elm327Protocol(
                connection = connection,
                logger = logger,
                onExchange = { command, response ->
                    lastCommand = command
                    lastResponse = response
                },
            )
            protocol.initialize()
            pollingLoop = PidPollingLoop(protocol)
        }.onSuccess {
            lastError = null
            if (!reconnecting) reconnectAttempts = 0
            state = BluetoothSessionState.CONNECTED
        }.onFailure { error ->
            lastError = error.message ?: error::class.java.simpleName
            state = BluetoothSessionState.ERROR
            manager.close()
        }.isSuccess

    interface SelectedDeviceStore {
        fun selectedDevice(): SelectedBluetoothDevice
        fun saveSelectedDevice(device: SelectedBluetoothDevice)
        fun clearSelectedDevice()
    }

    companion object {
        private val BACKOFF_MS = longArrayOf(1_000L, 2_000L, 5_000L, 10_000L)
    }
}

data class ReadCycleResult(
    val readings: List<com.codesynergy.horizon.mobile.model.ObservationReading>,
    val latencyMs: Long,
)
