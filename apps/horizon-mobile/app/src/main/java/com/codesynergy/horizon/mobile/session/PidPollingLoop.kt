package com.codesynergy.horizon.mobile.session

import com.codesynergy.horizon.mobile.model.ObdCommands
import com.codesynergy.horizon.mobile.model.ObservationReading
import java.time.Instant

class PidPollingLoop(
    private val protocol: Elm327Protocol,
) {
    fun readOnce(timestamp: Instant = Instant.now()): List<ObservationReading> =
        ObdCommands.pids.map { command ->
            protocol.readPid(command, timestamp)
        }
}
