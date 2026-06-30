package com.codesynergy.horizon.obdbridge.sink

import com.codesynergy.horizon.obdbridge.model.ObdObservationPayload

interface ObdObservationSink {
    fun emit(payload: ObdObservationPayload)
}
