package com.codesynergy.horizon.mobile.settings

import android.content.Context

class MobileSettings(context: Context) {
    private val preferences = context.getSharedPreferences("horizon-mobile", Context.MODE_PRIVATE)

    var gatewayUrl: String
        get() = preferences.getString(KEY_GATEWAY_URL, "").orEmpty()
        set(value) = preferences.edit().putString(KEY_GATEWAY_URL, value.trim()).apply()

    var assetReference: String
        get() = preferences.getString(KEY_ASSET_REFERENCE, "").orEmpty()
        set(value) = preferences.edit().putString(KEY_ASSET_REFERENCE, value.trim()).apply()

    var readFrequencyHz: Int
        get() = preferences.getInt(KEY_READ_FREQUENCY, 1)
        set(value) = preferences.edit().putInt(KEY_READ_FREQUENCY, value.coerceIn(1, 5)).apply()

    var bluetoothDeviceName: String
        get() = preferences.getString(KEY_BLUETOOTH_DEVICE_NAME, "").orEmpty()
        set(value) = preferences.edit().putString(KEY_BLUETOOTH_DEVICE_NAME, value.trim()).apply()

    var bluetoothDeviceAddress: String
        get() = preferences.getString(KEY_BLUETOOTH_DEVICE_ADDRESS, "").orEmpty()
        set(value) = preferences.edit().putString(KEY_BLUETOOTH_DEVICE_ADDRESS, value.trim()).apply()

    fun clearBluetoothDevice() {
        preferences.edit()
            .remove(KEY_BLUETOOTH_DEVICE_NAME)
            .remove(KEY_BLUETOOTH_DEVICE_ADDRESS)
            .apply()
    }

    companion object {
        private const val KEY_GATEWAY_URL = "gateway_url"
        private const val KEY_ASSET_REFERENCE = "asset_reference"
        private const val KEY_READ_FREQUENCY = "read_frequency_hz"
        private const val KEY_BLUETOOTH_DEVICE_NAME = "bluetooth_device_name"
        private const val KEY_BLUETOOTH_DEVICE_ADDRESS = "bluetooth_device_address"
    }
}
