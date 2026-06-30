package com.codesynergy.horizon.mobile.sink

import com.codesynergy.horizon.mobile.model.ObdObservationPayload

interface ObdObservationSink {
    fun emit(payload: ObdObservationPayload)
}
