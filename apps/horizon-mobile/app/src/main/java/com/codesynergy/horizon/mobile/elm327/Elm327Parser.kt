package com.codesynergy.horizon.mobile.elm327

import com.codesynergy.horizon.mobile.model.ObdCommand
import com.codesynergy.horizon.mobile.model.ObdCommands

object Elm327Parser {
    fun parse(command: ObdCommand, rawResponse: String): Double {
        val bytes = hexBytes(rawResponse)
        return when (command.value) {
            ObdCommands.rpm.value -> parseRpm(bytes)
            ObdCommands.coolantTemperature.value -> parseCoolantTemperature(bytes)
            ObdCommands.controlModuleVoltage.value -> parseControlModuleVoltage(bytes)
            else -> error("Unsupported OBD command: ${command.value}")
        }
    }

    private fun parseRpm(bytes: List<Int>): Double {
        val data = dataAfterPrefix(bytes, listOf(0x41, 0x0C), "010C")
        require(data.size >= 2) { "010C response missing data bytes" }
        return ((data[0] * 256) + data[1]) / 4.0
    }

    private fun parseCoolantTemperature(bytes: List<Int>): Double {
        val data = dataAfterPrefix(bytes, listOf(0x41, 0x05), "0105")
        require(data.isNotEmpty()) { "0105 response missing data bytes" }
        return (data[0] - 40).toDouble()
    }

    private fun parseControlModuleVoltage(bytes: List<Int>): Double {
        val data = dataAfterPrefix(bytes, listOf(0x41, 0x42), "0142")
        require(data.size >= 2) { "0142 response missing data bytes" }
        return ((data[0] * 256) + data[1]) / 1000.0
    }

    private fun dataAfterPrefix(bytes: List<Int>, prefix: List<Int>, command: String): List<Int> {
        val index = bytes.windowed(prefix.size).indexOf(prefix)
        require(index >= 0) { "$command response prefix not found" }
        return bytes.drop(index + prefix.size)
    }

    private fun hexBytes(rawResponse: String): List<Int> {
        val compact = rawResponse
            .uppercase()
            .replace("SEARCHING...", "")
            .replace("BUS INIT: OK", "")
            .replace(">", " ")
            .replace("\r", " ")
            .replace("\n", " ")
        val tokens = compact.split(Regex("\\s+")).filter { it.isNotBlank() }
        val bytes = mutableListOf<Int>()
        for (token in tokens) {
            if (token.length % 2 != 0 || !token.all { it in '0'..'9' || it in 'A'..'F' }) {
                continue
            }
            token.chunked(2).forEach { bytes.add(it.toInt(16)) }
        }
        require(bytes.isNotEmpty()) { "No hexadecimal bytes found in ELM327 response" }
        return bytes
    }
}
