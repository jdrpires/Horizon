package com.codesynergy.horizon.mobile.session

import com.codesynergy.horizon.mobile.bluetooth.ObdConnection
import com.codesynergy.horizon.mobile.elm327.Elm327Parser
import com.codesynergy.horizon.mobile.elm327.ObdMapper
import com.codesynergy.horizon.mobile.model.ObdCommand
import com.codesynergy.horizon.mobile.model.ObdCommands
import com.codesynergy.horizon.mobile.model.ObservationReading
import java.time.Instant

class Elm327Protocol(
    private val connection: ObdConnection,
    private val logger: BluetoothSessionLogger = NoopBluetoothSessionLogger,
    private val onExchange: (command: String, response: String) -> Unit = { _, _ -> },
) {
    fun initialize() {
        ObdCommands.initialization.forEach { command ->
            val response = send(command, "[ELM327]")
            validateInitializationResponse(command, response)
        }
        logger.log("[ELM327] initialized")
    }

    fun readPid(command: ObdCommand, timestamp: Instant): ObservationReading {
        val response = send(command, "[OBD]")
        val value = Elm327Parser.parse(command, response)
        return ObdMapper.toObservation(command, value, timestamp)
    }

    private fun send(command: ObdCommand, prefix: String): String {
        logger.log("$prefix sending ${command.value}")
        val response = connection.send(command)
        logger.log("$prefix response ${response.trim()}")
        onExchange(command.value, response.trim())
        return response
    }

    private fun validateInitializationResponse(command: ObdCommand, response: String) {
        val normalized = response
            .replace(">", "")
            .replace("\r", "")
            .replace("\n", "")
            .trim()
            .uppercase()
        require(normalized.isNotBlank()) { "Resposta vazia para ${command.value}" }
        require("?" !in normalized) { "Comando não reconhecido pelo ELM327: ${command.value}" }
        require("ERROR" !in normalized) { "ELM327 recusou ${command.value}: $normalized" }
        require("NO DATA" !in normalized) { "ELM327 sem resposta para ${command.value}" }
    }
}
