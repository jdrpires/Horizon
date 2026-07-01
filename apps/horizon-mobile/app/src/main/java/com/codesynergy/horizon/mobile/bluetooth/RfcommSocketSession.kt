package com.codesynergy.horizon.mobile.bluetooth

import android.annotation.SuppressLint
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothSocket
import com.codesynergy.horizon.mobile.model.ObdCommand
import java.io.BufferedInputStream
import java.io.BufferedOutputStream
import java.util.UUID

open class RfcommSocketSession(
    private val device: BluetoothDevice,
    private val responseTimeoutMs: Long = RESPONSE_TIMEOUT_MS,
) : ObdConnection {
    private var socket: BluetoothSocket? = null
    private var input: BufferedInputStream? = null
    private var output: BufferedOutputStream? = null

    @SuppressLint("MissingPermission")
    @Synchronized
    override fun connect() {
        val rfcommSocket = device.createRfcommSocketToServiceRecord(SPP_UUID)
        rfcommSocket.connect()
        socket = rfcommSocket
        input = BufferedInputStream(rfcommSocket.inputStream)
        output = BufferedOutputStream(rfcommSocket.outputStream)
    }

    @Synchronized
    override fun close() {
        runCatching { input?.close() }
        runCatching { output?.close() }
        runCatching { socket?.close() }
        input = null
        output = null
        socket = null
    }

    @Synchronized
    override fun send(command: ObdCommand): String {
        val writer = output ?: error("OBD Bluetooth socket is not connected")
        writer.write("${command.value}\r".toByteArray(Charsets.US_ASCII))
        writer.flush()
        return readUntilPrompt(command)
    }

    private fun readUntilPrompt(command: ObdCommand): String {
        val reader = input ?: error("OBD Bluetooth socket is not connected")
        val buffer = StringBuilder()
        val deadline = System.currentTimeMillis() + responseTimeoutMs
        while (System.currentTimeMillis() < deadline) {
            if (reader.available() <= 0) {
                Thread.sleep(25)
                continue
            }
            val value = reader.read()
            if (value < 0) {
                error("read failed for ${command.value}: socket closed")
            }
            val char = value.toChar()
            buffer.append(char)
            if (char == '>') {
                return buffer.toString()
            }
        }
        error("read timeout for ${command.value}")
    }

    companion object {
        private val SPP_UUID: UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")
        private const val RESPONSE_TIMEOUT_MS = 4_000L
    }
}
