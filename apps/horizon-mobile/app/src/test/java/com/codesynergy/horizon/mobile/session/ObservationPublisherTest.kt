package com.codesynergy.horizon.mobile.session

import com.codesynergy.horizon.mobile.model.ObdObservationPayload
import com.codesynergy.horizon.mobile.model.ObservationReading
import com.codesynergy.horizon.mobile.sink.ObdObservationSink
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith

class ObservationPublisherTest {
    @Test
    fun postPayloadUsesAssetUuid() {
        val sink = CapturingSink()
        val publisher = SinkObservationPublisher(sink, clock = { 10L })

        publisher.publish(ASSET_ID, listOf(reading()))

        assertEquals(ASSET_ID, sink.payload?.assetId)
    }

    @Test
    fun rejectsBlankAssetId() {
        val publisher = SinkObservationPublisher(CapturingSink())

        assertFailsWith<IllegalArgumentException> {
            publisher.publish("", listOf(reading()))
        }
    }

    private class CapturingSink : ObdObservationSink {
        var payload: ObdObservationPayload? = null

        override fun emit(payload: ObdObservationPayload) {
            this.payload = payload
        }
    }

    private companion object {
        const val ASSET_ID = "3662b190-0a62-4e76-829f-86d500d4552c"

        fun reading(): ObservationReading =
            ObservationReading(
                definitionId = "engine.rpm",
                value = 805.0,
                unit = "rpm",
                timestamp = "2026-07-01T14:00:00Z",
            )
    }
}
