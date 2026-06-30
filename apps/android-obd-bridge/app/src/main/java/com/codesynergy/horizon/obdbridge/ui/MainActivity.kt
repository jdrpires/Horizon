package com.codesynergy.horizon.obdbridge.ui

import android.Manifest
import android.app.Activity
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.Spinner
import android.widget.TextView
import com.codesynergy.horizon.obdbridge.bluetooth.BluetoothDeviceItem
import com.codesynergy.horizon.obdbridge.bluetooth.BluetoothDeviceProvider
import com.codesynergy.horizon.obdbridge.bluetooth.BluetoothRfcommObdConnection
import com.codesynergy.horizon.obdbridge.bluetooth.ObdConnection
import com.codesynergy.horizon.obdbridge.elm327.Elm327Parser
import com.codesynergy.horizon.obdbridge.elm327.ObdMapper
import com.codesynergy.horizon.obdbridge.model.ObdCommands
import com.codesynergy.horizon.obdbridge.model.ObdObservationPayload
import com.codesynergy.horizon.obdbridge.model.ObservationReading
import com.codesynergy.horizon.obdbridge.sink.HttpSink
import com.codesynergy.horizon.obdbridge.sink.LogcatSink
import java.time.Instant
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors

class MainActivity : Activity() {
    private lateinit var provider: BluetoothDeviceProvider
    private lateinit var deviceSpinner: Spinner
    private lateinit var statusText: TextView
    private lateinit var rpmText: TextView
    private lateinit var temperatureText: TextView
    private lateinit var voltageText: TextView
    private lateinit var lastReadingText: TextView
    private lateinit var gatewayUrlInput: EditText
    private lateinit var assetReferenceInput: EditText

    private val mainHandler = Handler(Looper.getMainLooper())
    private val executor: ExecutorService = Executors.newSingleThreadExecutor()
    private val logcatSink = LogcatSink()
    private var devices: List<BluetoothDeviceItem> = emptyList()
    private var connection: ObdConnection? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        provider = BluetoothDeviceProvider(this)
        setContentView(createLayout())
        requestBluetoothPermissionIfNeeded()
        refreshDevices()
    }

    override fun onDestroy() {
        executor.shutdownNow()
        runCatching { connection?.close() }
        super.onDestroy()
    }

    private fun createLayout(): LinearLayout {
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(32, 32, 32, 32)
            layoutParams = ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT,
            )
        }

        deviceSpinner = Spinner(this)
        statusText = label("Status: aguardando dispositivo")
        rpmText = label("RPM: --")
        temperatureText = label("Temperatura: --")
        voltageText = label("Tensão: --")
        lastReadingText = label("Última leitura: --")
        gatewayUrlInput = EditText(this).apply {
            hint = "Gateway URL (ex: http://192.168.0.10:8000/observations)"
            setSingleLine(true)
        }
        assetReferenceInput = EditText(this).apply {
            hint = "Asset ID ou referência externa"
            setSingleLine(true)
        }

        val refreshButton = Button(this).apply {
            text = "Listar pareados"
            setOnClickListener { refreshDevices() }
        }
        val connectButton = Button(this).apply {
            text = "Conectar"
            setOnClickListener { connectSelectedDevice() }
        }
        val readButton = Button(this).apply {
            text = "Iniciar leitura"
            setOnClickListener { readOnce() }
        }
        val testGatewayButton = Button(this).apply {
            text = "Testar Gateway"
            setOnClickListener { testGatewayConnection() }
        }

        root.addView(label("Horizon Android OBD Bridge"))
        root.addView(gatewayUrlInput)
        root.addView(assetReferenceInput)
        root.addView(testGatewayButton)
        root.addView(deviceSpinner)
        root.addView(refreshButton)
        root.addView(connectButton)
        root.addView(readButton)
        root.addView(statusText)
        root.addView(rpmText)
        root.addView(temperatureText)
        root.addView(voltageText)
        root.addView(lastReadingText)
        return root
    }

    private fun label(value: String): TextView =
        TextView(this).apply {
            text = value
            textSize = 18f
            setPadding(0, 12, 0, 12)
        }

    private fun requestBluetoothPermissionIfNeeded() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S && !provider.hasConnectPermission()) {
            requestPermissions(arrayOf(Manifest.permission.BLUETOOTH_CONNECT), 1001)
        }
    }

    private fun refreshDevices() {
        devices = provider.pairedDevices()
        deviceSpinner.adapter = ArrayAdapter(
            this,
            android.R.layout.simple_spinner_dropdown_item,
            devices,
        )
        statusText.text =
            if (devices.isEmpty()) {
                "Status: nenhum dispositivo pareado encontrado"
            } else {
                "Status: selecione o ELM327 pareado"
            }
    }

    private fun connectSelectedDevice() {
        val selected = devices.getOrNull(deviceSpinner.selectedItemPosition)
        if (selected == null) {
            statusText.text = "Status: selecione um dispositivo pareado"
            return
        }
        statusText.text = "Status: conectando ${selected.name.ifBlank { selected.address }}"
        executor.execute {
            runCatching {
                val socketConnection = BluetoothRfcommObdConnection(selected.device)
                socketConnection.connect()
                initializeElm327(socketConnection)
                connection = socketConnection
            }.onSuccess {
                postStatus("Status: conectado")
            }.onFailure { error ->
                postStatus("Status: erro ao conectar - ${error.message}")
            }
        }
    }

    private fun initializeElm327(obdConnection: ObdConnection) {
        ObdCommands.initialization.forEach { command ->
            obdConnection.send(command)
            Thread.sleep(150)
        }
    }

    private fun readOnce() {
        val obdConnection = connection
        if (obdConnection == null) {
            statusText.text = "Status: conecte ao ELM327 antes de ler"
            return
        }
        val gatewayUrl = gatewayUrlInput.text.toString().trim()
        val assetReference = assetReferenceInput.text.toString().trim().ifBlank { null }
        statusText.text = "Status: lendo PIDs"
        executor.execute {
            runCatching {
                val timestamp = Instant.now()
                val readings = ObdCommands.pids.map { command ->
                    val raw = obdConnection.send(command)
                    val value = Elm327Parser.parse(command, raw)
                    ObdMapper.toObservation(command, value, timestamp)
                }
                emitPayload(
                    payload = ObdObservationPayload(
                        assetId = assetReference,
                        observations = readings,
                    ),
                    gatewayUrl = gatewayUrl,
                )
                readings
            }.onSuccess { readings ->
                mainHandler.post { renderReadings(readings) }
            }.onFailure { error ->
                postStatus("Status: erro na leitura - ${error.message}")
            }
        }
    }

    private fun testGatewayConnection() {
        val gatewayUrl = gatewayUrlInput.text.toString().trim()
        if (gatewayUrl.isBlank()) {
            statusText.text = "Status: informe a URL do Gateway"
            return
        }
        statusText.text = "Status: testando Gateway"
        executor.execute {
            runCatching {
                HttpSink(gatewayUrl).testConnection()
            }.onSuccess { reachable ->
                postStatus(
                    if (reachable) {
                        "Status: Gateway alcançável"
                    } else {
                        "Status: Gateway indisponível"
                    },
                )
            }.onFailure { error ->
                postStatus("Status: erro no Gateway - ${error.message}")
            }
        }
    }

    private fun emitPayload(payload: ObdObservationPayload, gatewayUrl: String) {
        logcatSink.emit(payload)
        if (gatewayUrl.isNotBlank()) {
            HttpSink(gatewayUrl).emit(payload)
        }
    }

    private fun renderReadings(readings: List<ObservationReading>) {
        val byDefinition = readings.associateBy { it.definitionId }
        rpmText.text = "RPM: ${byDefinition["engine.rpm"]?.value ?: "--"} rpm"
        temperatureText.text =
            "Temperatura: ${byDefinition["engine.temperature"]?.value ?: "--"} °C"
        voltageText.text =
            "Tensão: ${byDefinition["electrical.battery_voltage"]?.value ?: "--"} V"
        lastReadingText.text = "Última leitura: ${readings.firstOrNull()?.timestamp ?: "--"}"
        statusText.text = "Status: leitura concluída"
    }

    private fun postStatus(value: String) {
        mainHandler.post { statusText.text = value }
    }
}
