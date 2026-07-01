package com.codesynergy.horizon.mobile.session

import com.codesynergy.horizon.mobile.bluetooth.ObdConnection

class BluetoothConnectionManager(
    private val store: BluetoothSessionEngine.SelectedDeviceStore,
    private val connectionFactory: (SelectedBluetoothDevice) -> ObdConnection?,
    private val logger: BluetoothSessionLogger = NoopBluetoothSessionLogger,
) {
    var connection: ObdConnection? = null
        private set

    val selectedDevice: SelectedBluetoothDevice
        get() = store.selectedDevice()

    fun select(device: SelectedBluetoothDevice) {
        store.saveSelectedDevice(device)
    }

    fun clearSelection() {
        close()
        store.clearSelectedDevice()
    }

    fun openSelected(): ObdConnection {
        val selected = selectedDevice
        require(selected.hasAddress) { "Selecione um dispositivo Bluetooth." }
        close()
        logger.log("[Bluetooth] connect requested ${selected.address}")
        val opened = connectionFactory(selected)
            ?: error("Dispositivo selecionado não encontrado: ${selected.address}")
        opened.connect()
        logger.log("[Bluetooth] socket opened ${selected.address}")
        connection = opened
        return opened
    }

    fun close() {
        runCatching { connection?.close() }
        connection = null
    }
}
