package com.codesynergy.horizon.mobile.model

data class HorizonAsset(
    val assetId: String,
    val name: String,
    val externalReference: String?,
    val category: String,
    val status: String,
) {
    override fun toString(): String = name
}

data class CurrentStateValue(
    val type: String,
    val value: Double,
    val unit: String,
    val source: String,
    val timestamp: String,
)

data class CurrentStateSnapshot(
    val assetId: String,
    val lastUpdatedAt: String?,
    val observationCount: Int,
    val values: List<CurrentStateValue>,
)

data class TimelineEntry(
    val type: String,
    val value: Double,
    val unit: String,
    val source: String,
    val timestamp: String,
)

