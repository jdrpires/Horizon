package com.codesynergy.horizon.mobile.session

import com.codesynergy.horizon.mobile.model.ObdObservationPayload
import com.codesynergy.horizon.mobile.model.ObservationReading
import com.codesynergy.horizon.mobile.network.GatewayResponseException
import com.codesynergy.horizon.mobile.network.HorizonGatewayClient
import com.codesynergy.horizon.mobile.sink.ObdObservationSink

interface ObservationPublisher {
    fun publish(assetId: String, readings: List<ObservationReading>): PublishResult
}

data class PublishResult(
    val latencyMs: Long,
)

class SinkObservationPublisher(
    private val sink: ObdObservationSink,
    private val logger: BluetoothSessionLogger = NoopBluetoothSessionLogger,
    private val clock: () -> Long = { System.currentTimeMillis() },
) : ObservationPublisher {
    override fun publish(assetId: String, readings: List<ObservationReading>): PublishResult {
        require(assetId.isNotBlank()) { "Asset UUID obrigatório para publicar observações." }
        logger.log("[Gateway] POST asset_id=$assetId")
        val startedAt = clock()
        sink.emit(
            ObdObservationPayload(
                assetId = assetId,
                observations = readings,
            )
        )
        val latency = clock() - startedAt
        logger.log("[Gateway] response accepted latency=${latency}ms")
        return PublishResult(latencyMs = latency)
    }
}

class GatewayObservationPublisher(
    private val gatewayUrl: String,
    private val logcatSink: ObdObservationSink,
    private val logger: BluetoothSessionLogger = NoopBluetoothSessionLogger,
    private val clock: () -> Long = { System.currentTimeMillis() },
) : ObservationPublisher {
    override fun publish(assetId: String, readings: List<ObservationReading>): PublishResult {
        require(assetId.isNotBlank()) { "Asset UUID obrigatório para publicar observações." }
        val payload = ObdObservationPayload(
            assetId = assetId,
            observations = readings,
        )
        logcatSink.emit(payload)
        logger.log("[Gateway] POST asset_id=$assetId")
        val startedAt = clock()
        runCatching {
            HorizonGatewayClient(gatewayUrl).send(payload)
        }.onFailure { error ->
            if (error is GatewayResponseException && error.statusCode == 422) {
                logger.log("[Gateway] 422 body=${error.responseBody}")
            }
            logger.log("[Gateway] response error ${error.message}")
            throw error
        }
        val latency = clock() - startedAt
        logger.log("[Gateway] response accepted latency=${latency}ms")
        return PublishResult(latencyMs = latency)
    }
}
