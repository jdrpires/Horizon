package com.codesynergy.horizon.obdbridge.bluetooth

import android.annotation.SuppressLint
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothSocket
import com.codesynergy.horizon.obdbridge.model.ObdCommand
import java.io.BufferedInputStream
import java.io.BufferedOutputStream
import java.util.UUID

class BluetoothRfcommObdConnection(
    private val device: BluetoothDevice,
) : ObdConnection {
    private var socket: BluetoothSocket? = null
    private var input: BufferedInputStream? = null
    private var output: BufferedOutputStream? = null

    @SuppressLint("MissingPermission")
    override fun connect() {
        val rfcommSocket = device.createRfcommSocketToServiceRecord(SPP_UUID)
        rfcommSocket.connect()
        socket = rfcommSocket
        input = BufferedInputStream(rfcommSocket.inputStream)
        output = BufferedOutputStream(rfcommSocket.outputStream)
    }

    override fun close() {
        runCatching { input?.close() }
        runCatching { output?.close() }
        runCatching { socket?.close() }
        input = null
        output = null
        socket = null
    }

    override fun send(command: ObdCommand): String {
        val writer = output ?: error("OBD Bluetooth socket is not connected")
        writer.write("${command.value}\r".toByteArray(Charsets.US_ASCII))
        writer.flush()
        return readUntilPrompt()
    }

    private fun readUntilPrompt(): String {
        val reader = input ?: error("OBD Bluetooth socket is not connected")
        val buffer = StringBuilder()
        val deadline = System.currentTimeMillis() + RESPONSE_TIMEOUT_MS
        while (System.currentTimeMillis() < deadline) {
            if (reader.available() <= 0) {
                Thread.sleep(25)
                continue
            }
            val value = reader.read()
            if (value < 0) break
            val char = value.toChar()
            buffer.append(char)
            if (char == '>') break
        }
        return buffer.toString()
    }

    companion object {
        private val SPP_UUID: UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")
        private const val RESPONSE_TIMEOUT_MS = 4_000L
    }
}
