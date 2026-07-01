package com.codesynergy.horizon.mobile.session

import android.util.Log

interface BluetoothSessionLogger {
    fun log(message: String)
}

object NoopBluetoothSessionLogger : BluetoothSessionLogger {
    override fun log(message: String) = Unit
}

object LogcatBluetoothSessionLogger : BluetoothSessionLogger {
    override fun log(message: String) {
        Log.i(TAG, message)
    }

    private const val TAG = "HorizonBluetooth"
}
