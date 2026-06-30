package com.codesynergy.horizon.obdbridge.sink

import com.codesynergy.horizon.obdbridge.model.ObdObservationPayload
import com.codesynergy.horizon.obdbridge.model.ObservationPayloadJson
import java.net.HttpURLConnection
import java.net.URL

class HttpSink(
    private val endpoint: String,
) : ObdObservationSink {
    override fun emit(payload: ObdObservationPayload) {
        val body = ObservationPayloadJson.encode(payload)
        val connection = openConnection("POST")
        try {
            connection.doOutput = true
            connection.setRequestProperty("Content-Type", "application/json; charset=utf-8")
            connection.outputStream.use { output ->
                output.write(body.toByteArray(Charsets.UTF_8))
            }
            val status = connection.responseCode
            if (status !in 200..299) {
                val errorBody = connection.errorStream?.bufferedReader()?.use { it.readText() }
                throw IllegalStateException("Gateway rejected payload: HTTP $status $errorBody")
            }
        } finally {
            connection.disconnect()
        }
    }

    fun testConnection(): Boolean {
        val connection = openConnection("GET")
        return try {
            connection.responseCode in 200..499
        } finally {
            connection.disconnect()
        }
    }

    private fun openConnection(method: String): HttpURLConnection {
        val cleanEndpoint = endpoint.trim()
        require(cleanEndpoint.isNotBlank()) { "Gateway URL is required" }
        return (URL(cleanEndpoint).openConnection() as HttpURLConnection).apply {
            requestMethod = method
            connectTimeout = 5000
            readTimeout = 5000
        }
    }
}
