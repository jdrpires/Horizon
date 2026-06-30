package com.codesynergy.horizon.obdbridge.sink

import android.util.Log
import com.codesynergy.horizon.obdbridge.model.ObdObservationPayload
import com.codesynergy.horizon.obdbridge.model.ObservationPayloadJson

class LogcatSink : ObdObservationSink {
    override fun emit(payload: ObdObservationPayload) {
        Log.i(TAG, ObservationPayloadJson.encode(payload))
    }

    companion object {
        private const val TAG = "HorizonObdBridge"
    }
}
