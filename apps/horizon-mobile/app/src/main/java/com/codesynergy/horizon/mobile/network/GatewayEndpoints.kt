package com.codesynergy.horizon.mobile.network

import java.net.URLEncoder

class GatewayEndpoints(rawUrl: String) {
    val baseUrl: String

    init {
        val clean = rawUrl.trim().trimEnd('/')
        require(clean.isNotBlank()) { "Informe o endereço do Horizon" }
        baseUrl = if (clean.endsWith("/observations")) {
            clean.removeSuffix("/observations")
        } else {
            clean
        }
    }

    val observationsUrl: String
        get() = "$baseUrl/observations"

    val healthUrl: String
        get() = "$baseUrl/health"

    fun assetsUrl(): String = "$baseUrl/assets"

    fun currentStateUrl(assetReference: String): String =
        "$baseUrl/assets/${assetReference.pathSegment()}/current-state"

    fun timelineUrl(assetReference: String): String =
        "$baseUrl/assets/${assetReference.pathSegment()}/timeline"

    private fun String.pathSegment(): String =
        URLEncoder.encode(trim(), Charsets.UTF_8.name()).replace("+", "%20")
}
