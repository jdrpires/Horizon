package com.codesynergy.horizon.mobile.state

import com.codesynergy.horizon.mobile.model.HorizonAsset

class AssetAutoBinder(
    private val manager: AssetSelectionManager,
    private val logger: AssetSelectionLogger = NoopAssetSelectionLogger,
) {
    fun bind(assets: List<HorizonAsset>): AssetBindingResult =
        when (assets.size) {
            0 -> {
                logger.log("[Asset] Assets loaded count=0")
                AssetBindingResult.NoAssets
            }
            1 -> {
                logger.log("[Asset] Assets loaded count=1")
                val selected = manager.select(assets.single())
                logger.log("[Asset] Asset auto-selected ${selected.displayName}")
                logger.log("[Asset] Selected asset_id=${selected.assetId}")
                AssetBindingResult.AutoSelected(selected)
            }
            else -> {
                logger.log("[Asset] Assets loaded count=${assets.size}")
                AssetBindingResult.ManualSelectionRequired
            }
        }
}

sealed interface AssetBindingResult {
    data object NoAssets : AssetBindingResult
    data object ManualSelectionRequired : AssetBindingResult
    data class AutoSelected(val asset: SelectedAsset) : AssetBindingResult
}
