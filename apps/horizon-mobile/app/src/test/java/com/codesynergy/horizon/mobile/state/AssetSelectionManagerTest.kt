package com.codesynergy.horizon.mobile.state

import com.codesynergy.horizon.mobile.model.HorizonAsset
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith
import kotlin.test.assertNull

class AssetSelectionManagerTest {
    @Test
    fun selectsAssetUsingUuid() {
        val manager = AssetSelectionManager(MemoryStore())

        val selected = manager.select(c3())

        assertEquals(ASSET_ID, selected.assetId)
        assertEquals("Citroen C3", selected.name)
        assertEquals("c3", selected.externalReference)
        assertEquals(ASSET_ID, manager.requireAssetId())
    }

    @Test
    fun persistsSelection() {
        val store = MemoryStore()
        val manager = AssetSelectionManager(store)

        manager.select(c3())

        assertEquals(ASSET_ID, store.saved?.assetId)
        assertEquals("Citroen C3", store.saved?.name)
        assertEquals("c3", store.saved?.externalReference)
    }

    @Test
    fun restoresPreviousAsset() {
        val manager = AssetSelectionManager(MemoryStore(SelectedAsset(ASSET_ID, "Citroen C3", "c3")))

        val restored = manager.restore()

        assertEquals(ASSET_ID, restored?.assetId)
        assertEquals(ASSET_ID, manager.requireAssetId())
    }

    @Test
    fun changesSelectedAsset() {
        val manager = AssetSelectionManager(MemoryStore())

        manager.select(c3())
        manager.select(HorizonAsset("11111111-1111-1111-1111-111111111111", "Other", null, "vehicle", "registered"))

        assertEquals("11111111-1111-1111-1111-111111111111", manager.requireAssetId())
    }

    @Test
    fun blocksWhenAssetDoesNotExist() {
        val manager = AssetSelectionManager(MemoryStore())

        val error = assertFailsWith<IllegalArgumentException> {
            manager.requireAssetId()
        }

        assertEquals("Selecione um Asset antes de iniciar a coleta.", error.message)
    }

    @Test
    fun clearsSelection() {
        val store = MemoryStore(SelectedAsset(ASSET_ID, "Citroen C3", "c3"))
        val manager = AssetSelectionManager(store)
        manager.restore()

        manager.clear()

        assertNull(manager.current)
        assertNull(store.saved)
    }

    private class MemoryStore(
        initial: SelectedAsset? = null,
    ) : AssetSelectionManager.Store {
        var saved: SelectedAsset? = initial

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
