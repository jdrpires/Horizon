package com.codesynergy.horizon.obdbridge.elm327

import com.codesynergy.horizon.obdbridge.model.ObdCommand
import com.codesynergy.horizon.obdbridge.model.ObdCommands
import com.codesynergy.horizon.obdbridge.model.ObservationReading
import java.time.Instant

object ObdMapper {
    fun toObservation(command: ObdCommand, value: Double, timestamp: Instant): ObservationReading {
        val (definitionId, unit) = when (command.value) {
            ObdCommands.rpm.value -> "engine.rpm" to "rpm"
            ObdCommands.coolantTemperature.value -> "engine.temperature" to "celsius"
            ObdCommands.controlModuleVoltage.value -> "electrical.battery_voltage" to "volt"
            else -> error("Unsupported OBD command: ${command.value}")
        }
        return ObservationReading(
            definitionId = definitionId,
            value = value,
            unit = unit,
            timestamp = timestamp.toString(),
        )
    }
}
