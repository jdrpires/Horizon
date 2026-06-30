package com.codesynergy.horizon.obdbridge.sink

import com.codesynergy.horizon.obdbridge.model.ObdObservationPayload

class HttpSink(
    private val endpoint: String,
) : ObdObservationSink {
    override fun emit(payload: ObdObservationPayload) {
        error(
            "HTTP sink is a placeholder until the Horizon ingestion endpoint is approved. " +
                "Configured endpoint: $endpoint; observations=${payload.observations.size}",
        )
    }
}
