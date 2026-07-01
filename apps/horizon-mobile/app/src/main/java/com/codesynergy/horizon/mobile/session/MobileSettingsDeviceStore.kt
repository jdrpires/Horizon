package com.codesynergy.horizon.mobile.session

import com.codesynergy.horizon.mobile.settings.MobileSettings

class MobileSettingsDeviceStore(
    private val settings: MobileSettings,
) : BluetoothSessionController.SelectedDeviceStore {
    override fun selectedDevice(): SelectedBluetoothDevice =
        SelectedBluetoothDevice(
            name = settings.bluetoothDeviceName,
            address = settings.bluetoothDeviceAddress,
        )

    override fun saveSelectedDevice(device: SelectedBluetoothDevice) {
        settings.bluetoothDeviceName = device.name
        settings.bluetoothDeviceAddress = device.address
    }

    override fun clearSelectedDevice() {
        settings.clearBluetoothDevice()
    }
}
