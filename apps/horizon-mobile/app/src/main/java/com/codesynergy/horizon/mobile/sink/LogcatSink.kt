package com.codesynergy.horizon.mobile.sink

import android.util.Log
import com.codesynergy.horizon.mobile.model.ObdObservationPayload
import com.codesynergy.horizon.mobile.model.ObservationPayloadJson

class LogcatSink : ObdObservationSink {
    override fun emit(payload: ObdObservationPayload) {
        Log.i(TAG, ObservationPayloadJson.encode(payload))
    }

    companion object {
        private const val TAG = "HorizonMobile"
    }
}
