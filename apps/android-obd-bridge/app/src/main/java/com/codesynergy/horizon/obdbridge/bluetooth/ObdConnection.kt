package com.codesynergy.horizon.obdbridge.bluetooth

import com.codesynergy.horizon.obdbridge.model.ObdCommand

interface ObdConnection {
    fun connect()
    fun close()
    fun send(command: ObdCommand): String
}
