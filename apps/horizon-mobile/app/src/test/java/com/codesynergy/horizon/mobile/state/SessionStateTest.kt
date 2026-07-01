package com.codesynergy.horizon.mobile.state

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertTrue

class SessionStateTest {
    @Test
    fun startsWithSafeDefaults() {
        val state = SessionState()

        assertEquals("", state.gatewayUrl)
        assertFalse(state.hasSelectedAsset)
        assertEquals(GatewayHealthStatus.UNKNOWN, state.gatewayStatus)
        assertEquals("Pendente", state.bluetoothStatus)
        assertEquals("Pendente", state.readingStatus)
    }

    @Test
    fun reflectsSelectedAsset() {
        val state = SessionState().withAsset(
            SelectedAsset(
                assetId = "3662b190-0a62-4e76-829f-86d500d4552c",
                name = "Citroen C3",
                externalReference = "c3",
            )
        )

        assertTrue(state.hasSelectedAsset)
        assertEquals("3662b190-0a62-4e76-829f-86d500d4552c", state.selectedAssetId)
        assertEquals("Citroen C3", state.assetDisplayName)
    }
}
