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
}

