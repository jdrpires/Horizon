package com.codesynergy.horizon.mobile.bluetooth

import android.Manifest
import android.annotation.SuppressLint
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.content.Context
import android.content.pm.PackageManager
import android.os.Build

class BluetoothDeviceProvider(
    private val context: Context,
) {
    private val adapter: BluetoothAdapter? = BluetoothAdapter.getDefaultAdapter()

    fun hasConnectPermission(): Boolean =
        Build.VERSION.SDK_INT < Build.VERSION_CODES.S ||
            context.checkSelfPermission(Manifest.permission.BLUETOOTH_CONNECT) ==
            PackageManager.PERMISSION_GRANTED

    @SuppressLint("MissingPermission")
    fun pairedDevices(): List<BluetoothDeviceItem> {
        if (!hasConnectPermission()) return emptyList()
        val bluetoothAdapter = adapter ?: return emptyList()
        return bluetoothAdapter.bondedDevices
            .map { device ->
                BluetoothDeviceItem(
                    name = device.name.orEmpty(),
                    address = device.address,
                    device = device,
                )
            }
            .sortedBy { it.toString() }
    }

    @SuppressLint("MissingPermission")
    fun deviceByAddress(address: String, fallbackName: String = ""): BluetoothDeviceItem? {
        if (!hasConnectPermission()) return null
        val bluetoothAdapter = adapter ?: return null
        val cleanAddress = address.trim()
        if (!BluetoothAdapter.checkBluetoothAddress(cleanAddress)) return null
        val device: BluetoothDevice = bluetoothAdapter.getRemoteDevice(cleanAddress)
        return BluetoothDeviceItem(
            name = device.name ?: fallbackName,
            address = device.address,
            device = device,
        )
    }
}
