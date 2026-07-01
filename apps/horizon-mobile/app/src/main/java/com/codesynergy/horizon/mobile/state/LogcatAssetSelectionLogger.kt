package com.codesynergy.horizon.mobile.state

import android.util.Log

object LogcatAssetSelectionLogger : AssetSelectionLogger {
    override fun log(message: String) {
        Log.i(TAG, message)
    }

    private const val TAG = "HorizonMobile"
}
