package com.codesynergy.horizon.mobile.bluetooth

import com.codesynergy.horizon.mobile.model.ObdCommand

interface ObdConnection {
    fun connect()
    fun close()
    fun send(command: ObdCommand): String
}
