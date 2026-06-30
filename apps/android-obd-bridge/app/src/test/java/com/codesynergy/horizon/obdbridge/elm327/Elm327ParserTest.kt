package com.codesynergy.horizon.obdbridge.elm327

import com.codesynergy.horizon.obdbridge.model.ObdCommands
import com.codesynergy.horizon.obdbridge.model.ObdObservationPayload
import com.codesynergy.horizon.obdbridge.model.ObservationPayloadJson
import java.time.Instant
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith
import kotlin.test.assertTrue

class Elm327ParserTest {
    @Test
    fun parsesSupportedPidResponses() {
        assertEquals(900.0, Elm327Parser.parse(ObdCommands.rpm, "41 0C 0E 10\r>"))
        assertEquals(91.0, Elm327Parser.parse(ObdCommands.coolantTemperature, "41 05 83\r>"))
        assertEquals(14.18, Elm327Parser.parse(ObdCommands.controlModuleVoltage, "41 42 37 64\r>"))
    }

    @Test
    fun toleratesEchoAndCompactResponses() {
        assertEquals(900.0, Elm327Parser.parse(ObdCommands.rpm, "010C\r410C0E10\r>"))
    }

    @Test
    fun rejectsMismatchedResponses() {
        assertFailsWith<IllegalArgumentException> {
            Elm327Parser.parse(ObdCommands.rpm, "41 05 83\r>")
        }
    }

    @Test
    fun mapsPidValuesToObservationReadings() {
        val timestamp = Instant.parse("2026-06-30T20:00:00Z")
        val reading = ObdMapper.toObservation(ObdCommands.rpm, 900.0, timestamp)

        assertEquals("engine.rpm", reading.definitionId)
        assertEquals("rpm", reading.unit)
        assertEquals("2026-06-30T20:00:00Z", reading.timestamp)
    }

    @Test
    fun encodesPayloadJson() {
        val timestamp = Instant.parse("2026-06-30T20:00:00Z")
        val payload = ObdObservationPayload(
            observations = listOf(
                ObdMapper.toObservation(ObdCommands.rpm, 900.0, timestamp),
            ),
        )

        val json = ObservationPayloadJson.encode(payload)

        assertTrue(json.contains("\"source\":\"android-obd-elm327\""))
        assertTrue(json.contains("\"asset_id\":null"))
        assertTrue(json.contains("\"definition_id\":\"engine.rpm\""))
        assertTrue(json.contains("\"value\":900"))
    }
}
