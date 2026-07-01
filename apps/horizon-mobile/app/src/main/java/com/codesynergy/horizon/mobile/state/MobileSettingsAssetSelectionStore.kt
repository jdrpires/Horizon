package com.codesynergy.horizon.mobile.state

import com.codesynergy.horizon.mobile.settings.MobileSettings

class MobileSettingsAssetSelectionStore(
    private val settings: MobileSettings,
) : AssetSelectionManager.Store {
    override fun load(): SelectedAsset? {
        val assetId = settings.selectedAssetId
        if (assetId.isBlank()) {
            return null
        }
        return SelectedAsset(
            assetId = assetId,
            name = settings.selectedAssetName,
            externalReference = settings.selectedAssetExternalReference,
        )
    }

    override fun save(asset: SelectedAsset) {
        settings.selectedAssetId = asset.assetId
        settings.selectedAssetName = asset.name
        settings.selectedAssetExternalReference = asset.externalReference
        settings.assetReference = asset.assetId
    }

    override fun clear() {
        settings.clearSelectedAsset()
    }
}
