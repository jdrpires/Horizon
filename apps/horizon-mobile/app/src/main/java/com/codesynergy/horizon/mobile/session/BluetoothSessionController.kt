package com.codesynergy.horizon.mobile.session

import com.codesynergy.horizon.mobile.bluetooth.ObdConnection

class BluetoothSessionController(
    private val store: SelectedDeviceStore,
    private val connectionFactory: (SelectedBluetoothDevice) -> ObdConnection?,
    private val initializer: (ObdConnection) -> Unit,
    private val sleeper: (Long) -> Unit = { Thread.sleep(it) },
) {
    var state: BluetoothSessionState = BluetoothSessionState.DISCONNECTED
        private set

    var connection: ObdConnection? = null
        private set

    var reconnectAttempts: Int = 0
        private set

    var lastError: String? = null
        private set

    val selectedDevice: SelectedBluetoothDevice
        get() = store.selectedDevice()

    fun select(device: SelectedBluetoothDevice) {
        store.saveSelectedDevice(device)
        reconnectAttempts = 0
        lastError = null
    }

    fun clearSelection() {
        stop()
        store.clearSelectedDevice()
    }

    fun connect(): Boolean {
        val selected = selectedDevice
        if (!selected.hasAddress) {
            fail("Selecione um dispositivo Bluetooth.")
            return false
        }
        state = BluetoothSessionState.CONNECTING
        return open(selected, reconnecting = false)
    }

    fun startReading(): Boolean {
        if (connection == null && !connect()) {
            return false
        }
        state = BluetoothSessionState.READING
        return true
    }

    fun stop() {
        runCatching { connection?.close() }
        connection = null
        state = BluetoothSessionState.DISCONNECTED
    }

    fun pauseReading() {
        state = if (connection == null) {
            BluetoothSessionState.DISCONNECTED
        } else {
            BluetoothSessionState.CONNECTED
        }
    }

    fun <T> withConnection(operation: (ObdConnection) -> T): T? {
        val current = connection
        if (current == null) {
            fail("Bluetooth não está conectado.")
            return null
        }
        return runCatching {
            operation(current)
        }.getOrElse { error ->
            lastError = error.message ?: error::class.java.simpleName
            reconnectSameDevice()
            null
        }
    }

    private fun reconnectSameDevice(): Boolean {
        val selected = selectedDevice
        if (!selected.hasAddress) {
            fail("Dispositivo Bluetooth não selecionado.")
            return false
        }
        state = BluetoothSessionState.RECONNECTING
        runCatching { connection?.close() }
        connection = null
        for (delayMs in BACKOFF_MS) {
            reconnectAttempts += 1
            sleeper(delayMs)
            if (open(selected, reconnecting = true)) {
                state = BluetoothSessionState.READING
                return true
            }
        }
        fail("Não foi possível reconectar ao dispositivo selecionado.")
        return false
    }

    private fun open(selected: SelectedBluetoothDevice, reconnecting: Boolean): Boolean =
        runCatching {
            val newConnection = connectionFactory(selected)
                ?: error("Dispositivo selecionado não encontrado: ${selected.address}")
            newConnection.connect()
            initializer(newConnection)
            connection = newConnection
        }.onSuccess {
            lastError = null
            if (!reconnecting) {
                reconnectAttempts = 0
            }
            state = BluetoothSessionState.CONNECTED
        }.onFailure { error ->
            fail(error.message ?: error::class.java.simpleName)
        }.isSuccess

    private fun fail(message: String) {
        lastError = message
        state = BluetoothSessionState.ERROR
    }

    interface SelectedDeviceStore {
        fun selectedDevice(): SelectedBluetoothDevice
        fun saveSelectedDevice(device: SelectedBluetoothDevice)
        fun clearSelectedDevice()
    }

    companion object {
        private val BACKOFF_MS = longArrayOf(1_000L, 2_000L, 5_000L)
    }
}
