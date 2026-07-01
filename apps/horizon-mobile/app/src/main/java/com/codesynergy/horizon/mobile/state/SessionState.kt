package com.codesynergy.horizon.mobile.state

data class SessionState(
    val gatewayUrl: String = "",
    val selectedAssetId: String? = null,
    val selectedAssetName: String? = null,
    val selectedAssetExternalReference: String? = null,
    val selectedBluetoothDeviceName: String? = null,
    val selectedBluetoothDeviceAddress: String? = null,
    val bluetoothStatus: String = "Pendente",
    val gatewayStatus: GatewayHealthStatus = GatewayHealthStatus.UNKNOWN,
    val readingStatus: String = "Pendente",
    val lastObservation: String? = null,
    val lastError: String? = null,
) {
    val hasSelectedAsset: Boolean
        get() = !selectedAssetId.isNullOrBlank()

    val hasGatewayUrl: Boolean
        get() = gatewayUrl.isNotBlank()

    val assetDisplayName: String
        get() = selectedAssetName?.takeIf { it.isNotBlank() } ?: selectedAssetId ?: "Asset não selecionado"

    fun withAsset(asset: SelectedAsset): SessionState =
        copy(
            selectedAssetId = asset.assetId,
            selectedAssetName = asset.name,
            selectedAssetExternalReference = asset.externalReference,
            lastError = null,
        )

    fun withoutAsset(message: String? = null): SessionState =
        copy(
            selectedAssetId = null,
            selectedAssetName = null,
            selectedAssetExternalReference = null,
            lastError = message,
        )
}

enum class GatewayHealthStatus {
    UNKNOWN,
    CHECKING,
    OK,
    ERROR,
}
