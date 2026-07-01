package com.codesynergy.horizon.mobile.network

import kotlin.test.Test
import kotlin.test.assertEquals

class GatewayEndpointsTest {
    @Test
    fun buildsEndpointUrlsFromGatewayBaseUrl() {
        val endpoints = GatewayEndpoints("http://192.168.0.10:8000")

        assertEquals("http://192.168.0.10:8000/health", endpoints.healthUrl)
        assertEquals("http://192.168.0.10:8000/observations", endpoints.observationsUrl)
        assertEquals("http://192.168.0.10:8000/assets", endpoints.assetsUrl())
        assertEquals(
            "http://192.168.0.10:8000/assets/citroen-c3/current-state",
            endpoints.currentStateUrl("citroen-c3"),
        )
        assertEquals(
            "http://192.168.0.10:8000/assets/citroen-c3/timeline",
            endpoints.timelineUrl("citroen-c3"),
        )
    }

    @Test
    fun acceptsLegacyObservationEndpointConfiguration() {
        val endpoints = GatewayEndpoints("http://192.168.0.10:8000/observations")

        assertEquals("http://192.168.0.10:8000", endpoints.baseUrl)
        assertEquals("http://192.168.0.10:8000/observations", endpoints.observationsUrl)
    }

    @Test
    fun buildsAssetQueriesUsingUuid() {
        val endpoints = GatewayEndpoints("http://192.168.0.10:8000")
        val assetId = "3662b190-0a62-4e76-829f-86d500d4552c"

        assertEquals(
            "http://192.168.0.10:8000/assets/$assetId/current-state",
            endpoints.currentStateUrl(assetId),
        )
        assertEquals(
            "http://192.168.0.10:8000/assets/$assetId/timeline",
            endpoints.timelineUrl(assetId),
        )
    }
}
