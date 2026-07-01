package com.codesynergy.horizon.mobile.network

import com.codesynergy.horizon.mobile.model.CurrentStateSnapshot
import com.codesynergy.horizon.mobile.model.CurrentStateValue
import com.codesynergy.horizon.mobile.model.HorizonAsset
import com.codesynergy.horizon.mobile.model.ObdObservationPayload
import com.codesynergy.horizon.mobile.model.ObservationPayloadJson
import com.codesynergy.horizon.mobile.model.TimelineEntry
import java.net.HttpURLConnection
import java.net.URL
import org.json.JSONObject

class HorizonGatewayClient(
    rawUrl: String,
) {
    private val endpoints = GatewayEndpoints(rawUrl)

    fun observationsUrl(): String = endpoints.observationsUrl

    fun testConnection(): Boolean {
        val connection = open(endpoints.healthUrl, "GET")
        return try {
            connection.responseCode in 200..299
        } finally {
            connection.disconnect()
        }
    }

    fun listAssets(): List<HorizonAsset> {
        val json = JSONObject(get(endpoints.assetsUrl()))
        val assets = json.getJSONArray("assets")
        return List(assets.length()) { index ->
            val item = assets.getJSONObject(index)
            HorizonAsset(
                assetId = item.getString("asset_id"),
                name = item.getString("name"),
                externalReference = item.optString("external_reference").ifBlank { null },
                category = item.getString("category"),
                status = item.getString("status"),
            )
        }
    }

    fun getCurrentState(assetReference: String): CurrentStateSnapshot {
        val json = JSONObject(get(endpoints.currentStateUrl(assetReference)))
        val values = json.getJSONArray("values")
        return CurrentStateSnapshot(
            assetId = json.getString("asset_id"),
            lastUpdatedAt = json.optString("last_updated_at").ifBlank { null },
            observationCount = json.getInt("observation_count"),
            values = List(values.length()) { index ->
                val item = values.getJSONObject(index)
                CurrentStateValue(
                    type = item.getString("type"),
                    value = item.getDouble("value"),
                    unit = item.getString("unit"),
                    source = item.getString("source"),
                    timestamp = item.getString("timestamp"),
                )
            },
        )
    }

    fun getTimeline(assetReference: String): List<TimelineEntry> {
        val json = JSONObject(get(endpoints.timelineUrl(assetReference)))
        val entries = json.getJSONArray("entries")
        return List(entries.length()) { index ->
            val item = entries.getJSONObject(index)
            TimelineEntry(
                type = item.getString("type"),
                value = item.getDouble("value"),
                unit = item.getString("unit"),
                source = item.getString("source"),
                timestamp = item.getString("timestamp"),
            )
        }
    }

    fun send(payload: ObdObservationPayload): String {
        val body = ObservationPayloadJson.encode(payload)
        val connection = open(endpoints.observationsUrl, "POST")
        try {
            connection.doOutput = true
            connection.setRequestProperty("Content-Type", "application/json; charset=utf-8")
            connection.outputStream.use { output ->
                output.write(body.toByteArray(Charsets.UTF_8))
            }
            val status = connection.responseCode
            val response = readResponse(connection)
            if (status !in 200..299) {
                throw GatewayResponseException(status, response)
            }
            return response
        } finally {
            connection.disconnect()
        }
    }

    private fun get(url: String): String {
        val connection = open(url, "GET")
        try {
            val status = connection.responseCode
            val response = readResponse(connection)
            if (status !in 200..299) {
                throw GatewayResponseException(status, response)
            }
            return response
        } finally {
            connection.disconnect()
        }
    }

    private fun open(url: String, method: String): HttpURLConnection =
        (URL(url).openConnection() as HttpURLConnection).apply {
            requestMethod = method
            connectTimeout = 5000
            readTimeout = 5000
        }

    private fun readResponse(connection: HttpURLConnection): String {
        val stream = if (connection.responseCode in 200..299) {
            connection.inputStream
        } else {
            connection.errorStream
        }
        return stream?.bufferedReader()?.use { it.readText() }.orEmpty()
    }
}

class GatewayResponseException(
    val statusCode: Int,
    val responseBody: String,
) : IllegalStateException(GatewayErrorMessage.friendly(statusCode, responseBody))

object GatewayErrorMessage {
    fun friendly(statusCode: Int, body: String): String {
        val reason = when {
            statusCode == 422 && body.contains("asset", ignoreCase = true) -> "Asset inexistente ou inválido."
            statusCode == 422 && body.contains("definition", ignoreCase = true) -> "Definition inválida."
            statusCode == 422 && body.contains("required", ignoreCase = true) -> "Campo obrigatório ausente."
            statusCode == 422 -> "Payload inválido."
            else -> "Horizon retornou HTTP $statusCode."
        }
        return "$reason $body".trim()
    }
}
