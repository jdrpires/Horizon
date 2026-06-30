package com.codesynergy.horizon.obdbridge.model

data class ObdCommand(
    val value: String,
    val label: String,
)

object ObdCommands {
    val initialization = listOf(
        ObdCommand("ATZ", "Reset"),
        ObdCommand("ATE0", "Echo off"),
        ObdCommand("ATL0", "Linefeeds off"),
        ObdCommand("ATS0", "Spaces off"),
        ObdCommand("ATH0", "Headers off"),
        ObdCommand("ATSP0", "Automatic protocol"),
    )

    val rpm = ObdCommand("010C", "RPM")
    val coolantTemperature = ObdCommand("0105", "Coolant temperature")
    val controlModuleVoltage = ObdCommand("0142", "Control module voltage")

    val pids = listOf(rpm, coolantTemperature, controlModuleVoltage)
}
