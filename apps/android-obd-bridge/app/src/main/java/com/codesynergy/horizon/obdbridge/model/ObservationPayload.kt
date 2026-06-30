package com.codesynergy.horizon.obdbridge.model

data class ObservationReading(
    val definitionId: String,
    val value: Double,
    val unit: String,
    val timestamp: String,
    val quality: String = "good",
)

data class ObdObservationPayload(
    val source: String = "android-obd-elm327",
    val assetId: String? = null,
    val observations: List<ObservationReading>,
)

object ObservationPayloadJson {
    fun encode(payload: ObdObservationPayload): String {
        val assetValue = payload.assetId?.let { "\"${escape(it)}\"" } ?: "null"
        val observations = payload.observations.joinToString(separator = ",") { observation ->
            buildString {
                append("{")
                append("\"definition_id\":\"${escape(observation.definitionId)}\",")
                append("\"value\":${formatNumber(observation.value)},")
                append("\"unit\":\"${escape(observation.unit)}\",")
                append("\"timestamp\":\"${escape(observation.timestamp)}\",")
                append("\"quality\":\"${escape(observation.quality)}\"")
                append("}")
            }
        }
        return buildString {
            append("{")
            append("\"source\":\"${escape(payload.source)}\",")
            append("\"asset_id\":$assetValue,")
            append("\"observations\":[")
            append(observations)
            append("]")
            append("}")
        }
    }

    private fun formatNumber(value: Double): String {
        val asLong = value.toLong()
        return if (value == asLong.toDouble()) asLong.toString() else value.toString()
    }

    private fun escape(value: String): String =
        value
            .replace("\\", "\\\\")
            .replace("\"", "\\\"")
}
