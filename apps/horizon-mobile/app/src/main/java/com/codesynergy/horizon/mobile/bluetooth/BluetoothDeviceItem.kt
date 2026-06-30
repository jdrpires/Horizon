package com.codesynergy.horizon.mobile.bluetooth

import android.bluetooth.BluetoothDevice

data class BluetoothDeviceItem(
    val name: String,
    val address: String,
    val device: BluetoothDevice,
) {
    override fun toString(): String =
        if (name.isBlank()) address else "$name ($address)"
}
