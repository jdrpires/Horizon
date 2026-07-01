package com.codesynergy.horizon.mobile.state

import com.codesynergy.horizon.mobile.model.HorizonAsset

class AssetSelectionManager(
    private val store: Store,
    private val logger: AssetSelectionLogger = NoopAssetSelectionLogger,
) {
    var current: SelectedAsset? = null
        private set

    fun restore(): SelectedAsset? {
        current = store.load()
        current?.let { asset ->
            logger.log("[Asset] Asset restored ${asset.name}")
            logger.log("[Asset] Asset UUID ${asset.assetId}")
            logger.log("[Asset] Selected asset_id=${asset.assetId}")
        }
        return current
    }

    fun select(asset: HorizonAsset): SelectedAsset {
        require(asset.assetId.isNotBlank()) { "Asset selecionado não possui UUID." }
        val selected = SelectedAsset(
            assetId = asset.assetId,
            name = asset.name,
            externalReference = asset.externalReference,
        )
        val previous = current
        current = selected
        store.save(selected)
        logger.log("[Asset] Asset selected ${selected.name}")
        logger.log("[Asset] Asset UUID ${selected.assetId}")
        logger.log("[Asset] Selected asset_id=${selected.assetId}")
        if (previous != null && previous.assetId != selected.assetId) {
            logger.log("[Asset] Asset changed ${previous.assetId} -> ${selected.assetId}")
        }
        return selected
    }

    fun clear() {
        current = null
        store.clear()
        logger.log("[Asset] Asset changed none")
    }

    fun requireAssetId(): String {
        val assetId = current?.assetId.orEmpty()
        require(assetId.isNotBlank()) { "Selecione um Asset antes de iniciar a coleta." }
        return assetId
    }

    interface Store {
        fun load(): SelectedAsset?
        fun save(asset: SelectedAsset)
        fun clear()
    }
}

data class SelectedAsset(
    val assetId: String,
    val name: String,
    val externalReference: String?,
) {
    val displayName: String
        get() = name.ifBlank { assetId }
}

interface AssetSelectionLogger {
    fun log(message: String)
}

object NoopAssetSelectionLogger : AssetSelectionLogger {
    override fun log(message: String) = Unit
}
