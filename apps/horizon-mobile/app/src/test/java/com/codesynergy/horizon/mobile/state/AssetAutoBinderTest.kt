package com.codesynergy.horizon.mobile.state

import com.codesynergy.horizon.mobile.model.HorizonAsset
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertIs
import kotlin.test.assertNull

class AssetAutoBinderTest {
    @Test
    fun autoSelectsWhenGatewayReturnsSingleAsset() {
        val store = MemoryStore()
        val manager = AssetSelectionManager(store)
        val binder = AssetAutoBinder(manager)

        val result = binder.bind(listOf(c3()))

        assertIs<AssetBindingResult.AutoSelected>(result)
        assertEquals(ASSET_ID, manager.current?.assetId)
        assertEquals(ASSET_ID, store.saved?.assetId)
    }

    @Test
    fun doesNotAutoSelectWhenGatewayReturnsMultipleAssets() {
        val store = MemoryStore()
        val manager = AssetSelectionManager(store)
        val binder = AssetAutoBinder(manager)

        val result = binder.bind(
            listOf(
                c3(),
                HorizonAsset("11111111-1111-1111-1111-111111111111", "Other", null, "vehicle", "registered"),
            )
        )

        assertIs<AssetBindingResult.ManualSelectionRequired>(result)
        assertNull(manager.current)
        assertNull(store.saved)
    }

    @Test
    fun keepsSelectionEmptyWhenGatewayReturnsNoAssets() {
        val manager = AssetSelectionManager(MemoryStore())
        val binder = AssetAutoBinder(manager)

        val result = binder.bind(emptyList())

        assertIs<AssetBindingResult.NoAssets>(result)
        assertNull(manager.current)
    }

    private class MemoryStore : AssetSelectionManager.Store {
        var saved: SelectedAsset? = null

        override fun load(): SelectedAsset? = saved

        override fun save(asset: SelectedAsset) {
            saved = asset
        }

        override fun clear() {
            saved = null
        }
    }

    private companion object {
        const val ASSET_ID = "3662b190-0a62-4e76-829f-86d500d4552c"

        fun c3(): HorizonAsset =
            HorizonAsset(
                assetId = ASSET_ID,
                name = "Citroen C3",
                externalReference = "c3",
                category = "vehicle",
                status = "registered",
            )
    }
}
