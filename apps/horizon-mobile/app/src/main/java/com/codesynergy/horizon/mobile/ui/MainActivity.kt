package com.codesynergy.horizon.mobile.ui

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
import android.widget.ScrollView
import android.widget.Spinner
import android.widget.TextView
import com.codesynergy.horizon.mobile.bluetooth.BluetoothDeviceItem
import com.codesynergy.horizon.mobile.bluetooth.BluetoothDeviceProvider
import com.codesynergy.horizon.mobile.bluetooth.BluetoothRfcommObdConnection
import com.codesynergy.horizon.mobile.model.CurrentStateSnapshot
import com.codesynergy.horizon.mobile.model.CurrentStateValue
import com.codesynergy.horizon.mobile.model.HorizonAsset
import com.codesynergy.horizon.mobile.model.ObservationReading
import com.codesynergy.horizon.mobile.model.TimelineEntry
import com.codesynergy.horizon.mobile.network.GatewayResponseException
import com.codesynergy.horizon.mobile.network.HorizonGatewayClient
import com.codesynergy.horizon.mobile.settings.MobileSettings
import com.codesynergy.horizon.mobile.session.BluetoothSessionEngine
import com.codesynergy.horizon.mobile.session.BluetoothSessionState
import com.codesynergy.horizon.mobile.session.GatewayObservationPublisher
import com.codesynergy.horizon.mobile.session.LogcatBluetoothSessionLogger
import com.codesynergy.horizon.mobile.session.MobileSettingsDeviceStore
import com.codesynergy.horizon.mobile.session.SelectedBluetoothDevice
import com.codesynergy.horizon.mobile.sink.LogcatSink
import com.codesynergy.horizon.mobile.state.AssetAutoBinder
import com.codesynergy.horizon.mobile.state.AssetBindingResult
import com.codesynergy.horizon.mobile.state.AssetSelectionManager
import com.codesynergy.horizon.mobile.state.GatewayHealthStatus
import com.codesynergy.horizon.mobile.state.LogcatAssetSelectionLogger
import com.codesynergy.horizon.mobile.state.MobileSettingsAssetSelectionStore
import com.codesynergy.horizon.mobile.state.SessionState
import java.time.Instant
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors

class MainActivity : Activity() {
    private lateinit var provider: BluetoothDeviceProvider
    private lateinit var settings: MobileSettings
    private lateinit var session: BluetoothSessionEngine
    private lateinit var assetSelection: AssetSelectionManager
    private lateinit var assetAutoBinder: AssetAutoBinder
    private lateinit var content: LinearLayout
    private lateinit var titleText: TextView
    private lateinit var subtitleText: TextView
    private var deviceSpinner: Spinner? = null

    private val mainHandler = Handler(Looper.getMainLooper())
    private val executor: ExecutorService = Executors.newSingleThreadExecutor()
    private val logcatSink = LogcatSink()

    private var devices: List<BluetoothDeviceItem> = emptyList()
    private var assets: List<HorizonAsset> = emptyList()
    private var selectedAsset: HorizonAsset? = null
    private var currentState: CurrentStateSnapshot? = null
    private var timeline: List<TimelineEntry> = emptyList()
    private var activeScreen = Screen.HOME
    private var readingActive = false
    private var sentPackets = 0
    private var receivedPackets = 0
    private var lastLatencyMs: Long? = null
    private var lastSync: String? = null
    private var appState = SessionState()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        provider = BluetoothDeviceProvider(this)
        settings = MobileSettings(this)
        assetSelection = AssetSelectionManager(
            store = MobileSettingsAssetSelectionStore(settings),
            logger = LogcatAssetSelectionLogger,
        )
        val restoredAsset = assetSelection.restore()
        assetAutoBinder = AssetAutoBinder(assetSelection, LogcatAssetSelectionLogger)
        appState = SessionState(
            gatewayUrl = settings.gatewayUrl,
            selectedAssetId = restoredAsset?.assetId,
            selectedAssetName = restoredAsset?.name,
            selectedAssetExternalReference = restoredAsset?.externalReference,
            selectedBluetoothDeviceName = settings.bluetoothDeviceName.ifBlank { null },
            selectedBluetoothDeviceAddress = settings.bluetoothDeviceAddress.ifBlank { null },
            bluetoothStatus = "Desconectado",
        )
        LogcatBluetoothSessionLogger.log("[Session] Session restored")
        session = BluetoothSessionEngine(
            store = MobileSettingsDeviceStore(settings),
            connectionFactory = { selected ->
                provider.deviceByAddress(selected.address, selected.name)?.let { device ->
                    BluetoothRfcommObdConnection(device.device)
                }
            },
            logger = LogcatBluetoothSessionLogger,
        )
        setContentView(createLayout())
        requestBluetoothPermissionIfNeeded()
        show(Screen.HOME)
        if (appState.hasGatewayUrl) {
            testHorizonConnection(silent = true)
        }
    }

    override fun onDestroy() {
        readingActive = false
        executor.shutdownNow()
        session.disconnect()
        super.onDestroy()
    }

    private fun createLayout(): LinearLayout {
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(28, 28, 28, 28)
            layoutParams = ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT,
            )
        }
        titleText = text("Horizon Mobile", 24f)
        subtitleText = text("Acompanhando o estado do Asset", 15f)
        content = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
        }
        val scroll = ScrollView(this).apply {
            addView(content)
        }
        root.addView(titleText)
        root.addView(subtitleText)
        root.addView(navRow(Screen.HOME, Screen.ASSETS, Screen.CURRENT_STATE))
        root.addView(navRow(Screen.TIMELINE, Screen.CONNECTION, Screen.SETTINGS))
        root.addView(scroll)
        return root
    }

    private fun navRow(vararg screens: Screen): LinearLayout =
        LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            screens.forEach { screen ->
                addView(
                    Button(this@MainActivity).apply {
                        text = screen.label
                        setOnClickListener { show(screen) }
                    },
                    LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f),
                )
            }
        }

    private fun show(screen: Screen) {
        activeScreen = screen
        content.removeAllViews()
        subtitleText.text = screen.subtitle
        when (screen) {
            Screen.HOME -> renderHome()
            Screen.ASSETS -> renderAssets()
            Screen.CURRENT_STATE -> renderCurrentState()
            Screen.TIMELINE -> renderTimeline()
            Screen.CONNECTION -> renderConnection()
            Screen.SETTINGS -> renderSettings()
        }
    }

    private fun renderHome() {
        val selected = assetSelection.current
        val assetName = selectedAsset?.name ?: selected?.displayName ?: appState.assetDisplayName
        val state = currentState
        section("Home")
        content.addView(text(assetName, 22f))
        content.addView(line("Status", selectedAsset?.status?.replaceFirstChar { it.uppercase() } ?: "--"))
        content.addView(line("Última atualização", state?.lastUpdatedAt ?: "--"))
        content.addView(line("Conexão", connectionQuality()))
        content.addView(primaryButton("Conectar") { connectSelectedDevice() })
        content.addView(primaryButton("Iniciar leitura") { startReading() })
        content.addView(primaryButton("Parar leitura") { stopReading() })
        content.addView(primaryButton("Atualizar estado") { syncFromHorizon() })
    }

    private fun renderAssets() {
        section("Assets")
        val assetItems = assets.ifEmpty {
            listOf(HorizonAsset("", "Nenhum Asset carregado", null, "", ""))
        }
        val assetSpinner = Spinner(this)
        assetSpinner.adapter = ArrayAdapter(
            this,
            android.R.layout.simple_spinner_dropdown_item,
            assetItems,
        )
        val selectedAssetId = assetSelection.current?.assetId
        val selectedIndex = assetItems.indexOfFirst { it.assetId == selectedAssetId }
        if (selectedIndex >= 0) {
            assetSpinner.setSelection(selectedIndex)
        }
        content.addView(assetSpinner)
        content.addView(primaryButton("Buscar Assets no Horizon") { fetchAssets() })
        content.addView(primaryButton("Usar Asset selecionado") {
            val item = assetSpinner.selectedItem as? HorizonAsset
            if (item != null && item.assetId.isNotBlank()) {
                selectedAsset = item
                val selected = assetSelection.select(item)
                appState = appState.withAsset(selected)
                status("Asset selecionado: ${item.name}")
                show(Screen.HOME)
            } else {
                status("Nenhum Asset disponível")
            }
        })
        if (assets.isNotEmpty()) {
            content.addView(spacer())
            assets.forEach { asset ->
                content.addView(text("${asset.name}\n${asset.category} • ${asset.status}", 17f))
            }
        }
    }

    private fun renderCurrentState() {
        section("Estado Atual")
        val state = currentState
        if (state == null || state.values.isEmpty()) {
            content.addView(text(if (appState.hasSelectedAsset) "Nenhuma leitura recebida para este Asset." else "Nenhum Asset selecionado.", 17f))
            content.addView(primaryButton("Buscar estado") { syncFromHorizon() })
            return
        }
        val rpm = state.valueOf("rpm")
        val temperature = state.valueOf("temperature")
        val voltage = state.valueOf("voltage")
        content.addView(text("Motor", 20f))
        content.addView(line("Funcionamento", rpm?.let { engineState(it.value) } ?: "--"))
        content.addView(line("RPM", rpm?.friendlyValue() ?: "--"))
        content.addView(line("Temperatura", temperature?.friendlyValue() ?: "--"))
        content.addView(spacer())
        content.addView(text("Sistema elétrico", 20f))
        content.addView(line("Condição", voltage?.let { electricalState(it.value) } ?: "--"))
        content.addView(line("Tensão", voltage?.friendlyValue() ?: "--"))
        content.addView(spacer())
        content.addView(line("Última atualização", state.lastUpdatedAt ?: "--"))
        content.addView(primaryButton("Atualizar estado") { syncFromHorizon() })
    }

    private fun renderTimeline() {
        section("Timeline")
        if (timeline.isEmpty()) {
            content.addView(text(if (appState.hasSelectedAsset) "Ainda não há leituras na Timeline deste Asset." else "Nenhum Asset selecionado.", 17f))
            content.addView(primaryButton("Buscar Timeline") { syncTimeline() })
            return
        }
        timeline.sortedByDescending { it.timestamp }.forEach { entry ->
            content.addView(
                text(
                    "${entry.timestamp.takeLast(14).take(8)}\n" +
                        "${friendlyType(entry.type)}\n" +
                        "${entry.friendlyValue()}\n" +
                        "Origem: ${friendlySource(entry.source)}",
                    16f,
                )
            )
            content.addView(separator())
        }
        content.addView(primaryButton("Atualizar Timeline") { syncTimeline() })
    }

    private fun renderConnection() {
        section("Conexão")
        val selected = session.selectedDevice
        content.addView(text("Diagnóstico", 20f))
        content.addView(line("Bluetooth", diagnosticStatus(session.state == BluetoothSessionState.CONNECTED || session.state == BluetoothSessionState.READING, appState.bluetoothStatus)))
        content.addView(line("ELM327", diagnosticStatus(session.lastResponse != null, session.lastError)))
        content.addView(line("Gateway", gatewayDiagnostic()))
        content.addView(line("Asset", diagnosticStatus(appState.hasSelectedAsset, appState.lastError)))
        content.addView(line("Current State", diagnosticStatus(currentState != null, appState.lastError)))
        content.addView(line("Timeline", diagnosticStatus(timeline.isNotEmpty(), appState.lastError)))
        content.addView(line("Publisher", diagnosticStatus(sentPackets > 0, appState.lastError)))
        content.addView(spacer())
        content.addView(line("Dispositivo selecionado", selected.displayName))
        content.addView(line("MAC address", selected.address.ifBlank { "--" }))
        content.addView(line("Estado Bluetooth", session.state.name))
        content.addView(line("Horizon", gatewayDiagnostic()))
        content.addView(line("Última leitura", lastSync ?: "--"))
        content.addView(line("Último comando", session.lastCommand ?: "--"))
        content.addView(line("Última resposta", session.lastResponse ?: "--"))
        content.addView(line("Tentativas de reconexão", session.reconnectAttempts.toString()))
        content.addView(line("Erro", appState.lastError ?: session.lastError ?: "--"))
        content.addView(line("Pacotes enviados", sentPackets.toString()))
        content.addView(line("Pacotes recebidos", receivedPackets.toString()))
        content.addView(line("Latência", lastLatencyMs?.let { "$it ms" } ?: "--"))
        content.addView(primaryButton("Listar dispositivos") {
            refreshDevices()
            show(Screen.CONNECTION)
        })
        if (devices.isEmpty()) {
            content.addView(text("Nenhum dispositivo pareado encontrado.", 16f))
            deviceSpinner = null
        } else {
            content.addView(deviceSelector())
        }
        content.addView(primaryButton("Selecionar dispositivo") { selectDeviceFromList() })
        content.addView(primaryButton("Conectar") { connectSelectedDevice() })
        content.addView(primaryButton("Iniciar leitura") { startReading() })
        content.addView(primaryButton("Parar leitura") { stopReading() })
        content.addView(primaryButton("Desconectar") { disconnectBluetooth() })
        content.addView(primaryButton("Trocar dispositivo") { changeDevice() })
        content.addView(primaryButton("Testar Horizon") { testHorizonConnection() })
    }

    private fun renderSettings() {
        section("Ajustes")
        val gatewayInput = EditText(this).apply {
            hint = "Endereço do Horizon"
            setSingleLine(true)
            setText(appState.gatewayUrl)
        }
        val assetInput = EditText(this).apply {
            hint = "Asset selecionado"
            setSingleLine(true)
            setText(assetSelection.current?.assetId.orEmpty())
            isEnabled = false
        }
        val frequencySpinner = Spinner(this).apply {
            adapter = ArrayAdapter(
                this@MainActivity,
                android.R.layout.simple_spinner_dropdown_item,
                listOf("1 Hz", "2 Hz", "5 Hz"),
            )
            setSelection(when (settings.readFrequencyHz) {
                2 -> 1
                5 -> 2
                else -> 0
            })
        }
        content.addView(line("Horizon", "Configure o endpoint local do Gateway."))
        content.addView(gatewayInput)
        content.addView(assetInput)
        content.addView(frequencySpinner)
        content.addView(primaryButton("Salvar ajustes") {
            settings.gatewayUrl = gatewayInput.text.toString()
            appState = appState.copy(gatewayUrl = settings.gatewayUrl, gatewayStatus = GatewayHealthStatus.UNKNOWN)
            settings.readFrequencyHz = when (frequencySpinner.selectedItemPosition) {
                1 -> 2
                2 -> 5
                else -> 1
            }
            status("Ajustes salvos")
            show(Screen.HOME)
        })
    }

    private fun deviceSelector(): Spinner =
        Spinner(this).apply {
            deviceSpinner = this
            adapter = ArrayAdapter(
                this@MainActivity,
                android.R.layout.simple_spinner_dropdown_item,
                devices,
            )
            val selectedAddress = session.selectedDevice.address
            val selectedIndex = devices.indexOfFirst { it.address == selectedAddress }
            if (selectedIndex >= 0) {
                setSelection(selectedIndex)
            }
        }

    private fun requestBluetoothPermissionIfNeeded() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S && !provider.hasConnectPermission()) {
            requestPermissions(arrayOf(Manifest.permission.BLUETOOTH_CONNECT), 1001)
        }
    }

    private fun refreshDevices() {
        devices = provider.pairedDevices()
        appState = appState.copy(
            bluetoothStatus = if (devices.isEmpty()) "Nenhum dispositivo pareado" else "Lista atualizada",
        )
    }

    private fun selectDeviceFromList() {
        val selected = devices.getOrNull(deviceSpinner?.selectedItemPosition ?: -1)
        if (selected == null) {
            status("Liste e selecione um dispositivo pareado")
            return
        }
        session.select(
            SelectedBluetoothDevice(
                name = selected.name,
                address = selected.address,
            )
        )
        appState = appState.copy(
            selectedBluetoothDeviceName = selected.name,
            selectedBluetoothDeviceAddress = selected.address,
            bluetoothStatus = "Selecionado: ${selected.name.ifBlank { selected.address }}",
            lastError = null,
        )
        status("Dispositivo selecionado")
        show(Screen.CONNECTION)
    }

    private fun connectSelectedDevice() {
        val selected = session.selectedDevice
        if (!selected.hasAddress) {
            appState = appState.copy(bluetoothStatus = "Selecione um dispositivo pareado")
            show(Screen.CONNECTION)
            return
        }
        appState = appState.copy(bluetoothStatus = "Conectando ${selected.displayName}")
        show(Screen.CONNECTION)
        executor.execute {
            runCatching {
                check(session.connect()) { session.lastError ?: "Falha ao conectar" }
            }.onSuccess {
                appState = appState.copy(bluetoothStatus = "Conectado a ${selected.displayName}", lastError = null)
                status("Bluetooth conectado")
                refreshScreen()
            }.onFailure { error ->
                appState = appState.copy(bluetoothStatus = "Erro ao conectar", lastError = error.message)
                status("Não foi possível conectar ao Bluetooth")
                refreshScreen()
            }
        }
    }

    private fun startReading() {
        if (readingActive) {
            status("Leitura já está em andamento")
            return
        }
        if (!appState.hasGatewayUrl) {
            appState = appState.copy(lastError = "Configure o endereço do Horizon antes de iniciar a coleta.")
            status("Configure o endereço do Horizon antes de iniciar a coleta.")
            show(Screen.SETTINGS)
            return
        }
        if (assetSelection.current?.assetId.isNullOrBlank()) {
            appState = appState.copy(lastError = "Selecione um Asset antes de iniciar a coleta.")
            status("Selecione um Asset antes de iniciar a coleta.")
            show(Screen.ASSETS)
            return
        }
        if (session.state != BluetoothSessionState.CONNECTED && session.state != BluetoothSessionState.READING) {
            appState = appState.copy(lastError = "Conecte e inicialize o ELM327 antes de iniciar a coleta.")
            status("Conecte e inicialize o ELM327 antes de iniciar a coleta.")
            show(Screen.CONNECTION)
            return
        }
        appState = appState.copy(bluetoothStatus = "Iniciando leitura", readingStatus = "Iniciando", lastError = null)
        refreshScreen()
        executor.execute {
            if (!session.startReading()) {
                readingActive = false
                status(session.lastError ?: "Conecte o Bluetooth antes de acompanhar o Asset")
                refreshScreen()
                return@execute
            }
            readingActive = true
            appState = appState.copy(readingStatus = "Coletando")
            status("Acompanhando o Asset")
            mainHandler.post { scheduleReading() }
            refreshScreen()
        }
    }

    private fun stopReading() {
        readingActive = false
        appState = appState.copy(readingStatus = "Pausada")
        status("Leitura pausada")
        refreshScreen()
        executor.execute {
            session.stopReading()
            refreshScreen()
        }
    }

    private fun disconnectBluetooth() {
        readingActive = false
        appState = appState.copy(bluetoothStatus = "Desconectado", readingStatus = "Pendente")
        status("Bluetooth desconectado")
        refreshScreen()
        executor.execute {
            session.disconnect()
            refreshScreen()
        }
    }

    private fun changeDevice() {
        readingActive = false
        devices = emptyList()
        appState = appState.copy(
            selectedBluetoothDeviceName = null,
            selectedBluetoothDeviceAddress = null,
            bluetoothStatus = "Seleção de Bluetooth removida",
        )
        status("Liste os dispositivos para selecionar outro ELM327")
        executor.execute {
            session.clearSelection()
            showOnMain(Screen.CONNECTION)
        }
    }

    private fun scheduleReading() {
        if (!readingActive) {
            return
        }
        readOnce()
        val interval = 1000L / settings.readFrequencyHz.coerceIn(1, 5)
        mainHandler.postDelayed({ scheduleReading() }, interval)
    }

    private fun readOnce() {
        val assetId = runCatching {
            assetSelection.requireAssetId()
        }.getOrElse { error ->
            LogcatBluetoothSessionLogger.log("[Publisher] Skipped POST because asset_id is null")
            appState = appState.copy(lastError = error.message)
            status(error.message ?: "Selecione um Asset antes de iniciar a coleta.")
            showOnMain(Screen.ASSETS)
            return
        }
        executor.execute {
            val result = runCatching {
                session.readAndPublish(
                    assetReference = assetId,
                    publisher = GatewayObservationPublisher(
                        gatewayUrl = settings.gatewayUrl,
                        logcatSink = logcatSink,
                        logger = LogcatBluetoothSessionLogger,
                    ),
                )
            }.getOrElse { error ->
                val message = friendlyGatewayError(error)
                appState = appState.copy(gatewayStatus = GatewayHealthStatus.ERROR, lastError = message)
                status(message)
                refreshScreen()
                return@execute
            }
            if (result == null) {
                appState = appState.copy(bluetoothStatus = "Reconectando ${session.selectedDevice.displayName}", lastError = session.lastError)
                status(session.lastError ?: "Falha de leitura; tentando reconectar")
                refreshScreen()
                return@execute
            }
            lastLatencyMs = result.latencyMs
            sentPackets += 1
            appState = appState.copy(lastObservation = result.readings.firstOrNull()?.timestamp, lastError = null)
            LogcatBluetoothSessionLogger.log("[Publisher] Published observations count=${result.readings.size}")
            status("Leitura enviada ao Horizon")
            syncAfterSend(assetId, result.readings)
        }
    }

    private fun syncAfterSend(assetId: String, readings: List<ObservationReading>) {
        executor.execute {
            runCatching {
                val client = HorizonGatewayClient(settings.gatewayUrl)
                LogcatBluetoothSessionLogger.log("[Gateway] GET current-state asset_id=$assetId")
                currentState = client.getCurrentState(assetId)
                LogcatBluetoothSessionLogger.log("[Gateway] GET timeline asset_id=$assetId")
                timeline = client.getTimeline(assetId)
                receivedPackets += 2
                lastSync = readings.firstOrNull()?.timestamp ?: Instant.now().toString()
                appState = appState.copy(gatewayStatus = GatewayHealthStatus.OK, lastError = null)
            }.onSuccess {
                refreshScreen()
            }.onFailure { error ->
                appState = appState.copy(gatewayStatus = GatewayHealthStatus.ERROR, lastError = friendlyGatewayError(error))
                status("Leitura enviada, mas o estado não foi atualizado: ${friendlyGatewayError(error)}")
                refreshScreen()
            }
        }
    }

    private fun fetchAssets() {
        executor.execute {
            runCatching {
                LogcatBluetoothSessionLogger.log("[Gateway] GET /assets")
                val result = HorizonGatewayClient(settings.gatewayUrl).listAssets()
                assets = result
                when (val binding = assetAutoBinder.bind(result)) {
                    AssetBindingResult.NoAssets -> {
                        selectedAsset = null
                        appState = appState.withoutAsset("Nenhum Asset disponível.")
                    }
                    AssetBindingResult.ManualSelectionRequired -> {
                        val restored = assetSelection.current
                        selectedAsset = result.firstOrNull {
                            it.assetId == restored?.assetId || it.externalReference == restored?.externalReference
                        }
                        selectedAsset?.let { appState = appState.withAsset(assetSelection.current ?: assetSelection.select(it)) }
                    }
                    is AssetBindingResult.AutoSelected -> {
                        selectedAsset = result.single()
                        appState = appState.withAsset(binding.asset)
                    }
                }
                receivedPackets += 1
                appState = appState.copy(gatewayStatus = GatewayHealthStatus.OK, lastError = null)
            }.onSuccess {
                status(if (assets.isEmpty()) "Nenhum Asset disponível." else "Assets atualizados")
                showOnMain(Screen.ASSETS)
            }.onFailure { error ->
                appState = appState.copy(gatewayStatus = GatewayHealthStatus.ERROR, lastError = friendlyGatewayError(error))
                status("Não foi possível buscar Assets: ${friendlyGatewayError(error)}")
                refreshScreen()
            }
        }
    }

    private fun syncFromHorizon() {
        val assetId = runCatching {
            assetSelection.requireAssetId()
        }.getOrElse { error ->
            appState = appState.copy(lastError = "Nenhum Asset selecionado.")
            status(error.message ?: "Selecione um Asset antes de iniciar a coleta.")
            showOnMain(Screen.ASSETS)
            return
        }
        executor.execute {
            runCatching {
                val client = HorizonGatewayClient(settings.gatewayUrl)
                LogcatBluetoothSessionLogger.log("[Gateway] GET current-state asset_id=$assetId")
                currentState = client.getCurrentState(assetId)
                LogcatBluetoothSessionLogger.log("[Gateway] GET timeline asset_id=$assetId")
                timeline = client.getTimeline(assetId)
                receivedPackets += 2
                lastSync = currentState?.lastUpdatedAt ?: Instant.now().toString()
                appState = appState.copy(gatewayStatus = GatewayHealthStatus.OK, lastError = null)
            }.onSuccess {
                status("Estado atualizado")
                refreshScreen()
            }.onFailure { error ->
                appState = appState.copy(gatewayStatus = GatewayHealthStatus.ERROR, lastError = friendlyGatewayError(error))
                status("Não foi possível atualizar o estado: ${friendlyGatewayError(error)}")
                refreshScreen()
            }
        }
    }

    private fun syncTimeline() {
        val assetId = runCatching {
            assetSelection.requireAssetId()
        }.getOrElse { error ->
            appState = appState.copy(lastError = "Nenhum Asset selecionado.")
            status(error.message ?: "Selecione um Asset antes de iniciar a coleta.")
            showOnMain(Screen.ASSETS)
            return
        }
        executor.execute {
            runCatching {
                LogcatBluetoothSessionLogger.log("[Gateway] GET timeline asset_id=$assetId")
                timeline = HorizonGatewayClient(settings.gatewayUrl).getTimeline(assetId)
                receivedPackets += 1
                lastSync = Instant.now().toString()
                appState = appState.copy(gatewayStatus = GatewayHealthStatus.OK, lastError = null)
            }.onSuccess {
                status("Timeline atualizada")
                showOnMain(Screen.TIMELINE)
            }.onFailure { error ->
                appState = appState.copy(gatewayStatus = GatewayHealthStatus.ERROR, lastError = friendlyGatewayError(error))
                status("Não foi possível buscar a Timeline: ${friendlyGatewayError(error)}")
                refreshScreen()
            }
        }
    }

    private fun testHorizonConnection(silent: Boolean = false) {
        appState = appState.copy(gatewayStatus = GatewayHealthStatus.CHECKING)
        if (!silent) refreshScreen()
        executor.execute {
            runCatching {
                HorizonGatewayClient(appState.gatewayUrl).testConnection()
            }.onSuccess { connected ->
                appState = appState.copy(
                    gatewayStatus = if (connected) GatewayHealthStatus.OK else GatewayHealthStatus.ERROR,
                    lastError = if (connected) null else "Horizon indisponível",
                )
                if (!silent) status(gatewayDiagnostic())
                refreshScreen()
            }.onFailure { error ->
                appState = appState.copy(gatewayStatus = GatewayHealthStatus.ERROR, lastError = friendlyGatewayError(error))
                if (!silent) status("Não foi possível conectar ao Horizon: ${friendlyGatewayError(error)}")
                refreshScreen()
            }
        }
    }

    private fun section(value: String) {
        content.addView(text(value, 22f))
        content.addView(separator())
    }

    private fun line(label: String, value: String): TextView =
        text("$label\n$value", 16f)

    private fun primaryButton(label: String, action: () -> Unit): Button =
        Button(this).apply {
            text = label
            setOnClickListener { action() }
        }

    private fun text(value: String, size: Float): TextView =
        TextView(this).apply {
            text = value
            textSize = size
            setPadding(0, 12, 0, 12)
        }

    private fun separator(): TextView = text("------------------------------", 12f)

    private fun spacer(): TextView = text("", 8f)

    private fun status(message: String) {
        mainHandler.post {
            subtitleText.text = message
        }
    }

    private fun refreshScreen() {
        mainHandler.post { show(activeScreen) }
    }

    private fun showOnMain(screen: Screen) {
        mainHandler.post { show(screen) }
    }

    private fun connectionQuality(): String =
        when {
            session.state == BluetoothSessionState.READING && appState.gatewayStatus == GatewayHealthStatus.OK -> "Boa"
            session.state == BluetoothSessionState.CONNECTED || session.state == BluetoothSessionState.READING -> "Bluetooth conectado"
            appState.gatewayStatus == GatewayHealthStatus.OK -> "Horizon conectado"
            else -> "Aguardando conexão"
        }

    private fun gatewayDiagnostic(): String =
        when (appState.gatewayStatus) {
            GatewayHealthStatus.UNKNOWN -> "Pendente"
            GatewayHealthStatus.CHECKING -> "Verificando"
            GatewayHealthStatus.OK -> "OK"
            GatewayHealthStatus.ERROR -> "Erro"
        }

    private fun diagnosticStatus(ok: Boolean, error: String?): String =
        when {
            ok -> "OK"
            !error.isNullOrBlank() -> "Erro"
            else -> "Pendente"
        }

    private fun friendlyGatewayError(error: Throwable): String {
        if (error is GatewayResponseException && error.statusCode == 422) {
            LogcatBluetoothSessionLogger.log("[Gateway] 422 body=${error.responseBody}")
        }
        return error.message ?: error::class.java.simpleName
    }

    private fun CurrentStateSnapshot.valueOf(type: String): CurrentStateValue? =
        values.firstOrNull { it.type == type }

    private fun CurrentStateValue.friendlyValue(): String = "${formatNumber(value)} ${friendlyUnit(unit)}"

    private fun TimelineEntry.friendlyValue(): String = "${formatNumber(value)} ${friendlyUnit(unit)}"

    private fun engineState(rpm: Double): String =
        if (rpm in 650.0..1000.0) "Marcha lenta" else "Em funcionamento"

    private fun electricalState(voltage: Double): String =
        if (voltage in 12.0..14.8) "Normal" else "Requer atenção"

    private fun friendlyType(type: String): String =
        when (type) {
            "rpm" -> "RPM"
            "temperature" -> "Temperatura"
            "voltage" -> "Sistema elétrico"
            else -> type.replaceFirstChar { it.uppercase() }
        }

    private fun friendlyUnit(unit: String): String =
        when (unit) {
            "celsius" -> "°C"
            "volt" -> "V"
            else -> unit
        }

    private fun friendlySource(source: String): String =
        when (source) {
            "android-obd-elm327" -> "Horizon Mobile"
            "manual" -> "Manual"
            else -> source
        }

    private fun formatNumber(value: Double): String {
        val asLong = value.toLong()
        return if (value == asLong.toDouble()) asLong.toString() else "%.2f".format(value)
    }
}

private enum class Screen(
    val label: String,
    val subtitle: String,
) {
    HOME("Home", "Estado do Asset"),
    ASSETS("Assets", "Seleção do Asset"),
    CURRENT_STATE("Estado", "Current State do Horizon"),
    TIMELINE("Timeline", "Memória cronológica"),
    CONNECTION("Conexão", "Bluetooth e Horizon"),
    SETTINGS("Ajustes", "Configuração local"),
}
