package com.codesynergy.horizon.mobile.session

import com.codesynergy.horizon.mobile.bluetooth.ObdConnection
import com.codesynergy.horizon.mobile.model.ObdCommand
import com.codesynergy.horizon.mobile.model.ObdCommands
import com.codesynergy.horizon.mobile.model.ObservationReading
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertNotEquals
import kotlin.test.assertNull
import kotlin.test.assertTrue

class BluetoothSessionEngineTest {
    @Test
    fun startsDisconnected() {
        val engine = engine(MemoryDeviceStore())

        assertEquals(BluetoothSessionState.DISCONNECTED, engine.state)
        assertNull(engine.lastError)
    }

    @Test
    fun preservesSelectedDeviceByMacAddress() {
        val store = MemoryDeviceStore()
        val engine = engine(store)

        engine.select(SelectedBluetoothDevice("OBDII", MAC))

        assertEquals("OBDII", engine.selectedDevice.name)
        assertEquals(MAC, engine.selectedDevice.address)
    }

    @Test
    fun selectedMacDoesNotChangeWhenExternalDeviceListChanges() {
        val engine = engine(MemoryDeviceStore(SelectedBluetoothDevice("OBDII", MAC)))
        val refreshedDevices = listOf(
            SelectedBluetoothDevice("Headset", "AA:AA:AA:AA:AA:AA"),
            SelectedBluetoothDevice("Laptop", "BB:BB:BB:BB:BB:BB"),
        )

        assertTrue(refreshedDevices.none { it.address == engine.selectedDevice.address })
        assertEquals(MAC, engine.selectedDevice.address)
    }

    @Test
    fun initializesElm327InRequiredOrder() {
        val connection = FakeConnection()
        val engine = engine(connection = connection)

        assertTrue(engine.connect())

        assertEquals(ObdCommands.initialization.map { it.value }, connection.sentCommands)
        assertEquals(BluetoothSessionState.CONNECTED, engine.state)
    }

    @Test
    fun readCycleSendsPidsInRequiredOrder() {
        val connection = FakeConnection()
        val engine = engine(connection = connection)
        val publisher = CapturingPublisher()

        assertTrue(engine.startReading())
        val result = engine.readAndPublish("c3", publisher)

        assertEquals(3, result?.readings?.size)
        assertEquals(
            ObdCommands.initialization.map { it.value } + ObdCommands.pids.map { it.value },
            connection.sentCommands,
        )
    }

    @Test
    fun timeoutReconnectsUsingSameMacAddress() {
        val first = FakeConnection(failOnCommands = setOf(ObdCommands.rpm.value))
        val second = FakeConnection()
        val connections = ArrayDeque(listOf(first, second))
        val factoryAddresses = mutableListOf<String>()
        val engine = engine { selected ->
            factoryAddresses += selected.address
            connections.removeFirst()
        }

        assertTrue(engine.startReading())
        val result = engine.readAndPublish("c3", CapturingPublisher())

        assertNull(result)
        assertEquals(listOf(MAC, MAC), factoryAddresses)
        assertEquals(BluetoothSessionState.READING, engine.state)
        assertEquals(1, engine.reconnectAttempts)
        assertTrue(first.closed)
    }

    @Test
    fun neverReconnectsToDifferentDevice() {
        val unwantedMac = "AA:AA:AA:AA:AA:AA"
        val factoryAddresses = mutableListOf<String>()
        val engine = engine { selected ->
            factoryAddresses += selected.address
            assertNotEquals(unwantedMac, selected.address)
            if (factoryAddresses.size == 1) {
                FakeConnection(failOnCommands = setOf(ObdCommands.rpm.value))
            } else {
                FakeConnection()
            }
        }

        assertTrue(engine.startReading())
        engine.readAndPublish("c3", CapturingPublisher())

        assertTrue(factoryAddresses.all { it == MAC })
    }

    @Test
    fun stopReadingClosesSocketAndReturnsToDisconnected() {
        val connection = FakeConnection()
        val engine = engine(connection = connection)

        assertTrue(engine.startReading())
        engine.stopReading()

        assertTrue(connection.closed)
        assertEquals(BluetoothSessionState.DISCONNECTED, engine.state)
    }

    @Test
    fun connectionErrorDoesNotCrashApplicationFlow() {
        val engine = engine(MemoryDeviceStore())

        assertFalse(engine.connect())

        assertEquals(BluetoothSessionState.ERROR, engine.state)
        assertEquals("Selecione um dispositivo Bluetooth.", engine.lastError)
    }

    @Test
    fun publisherReceivesCanonicalObservations() {
        val engine = engine(connection = FakeConnection())
        val publisher = CapturingPublisher()

        val result = engine.readAndPublish("c3", publisher)

        assertEquals(3, result?.readings?.size)
        assertEquals("engine.rpm", publisher.readings.first().definitionId)
        assertEquals("engine.temperature", publisher.readings[1].definitionId)
        assertEquals("electrical.battery_voltage", publisher.readings[2].definitionId)
    }

    private fun engine(
        store: MemoryDeviceStore = MemoryDeviceStore(SelectedBluetoothDevice("OBDII", MAC)),
        connection: FakeConnection = FakeConnection(),
    ): BluetoothSessionEngine =
        engine(store) { connection }

    private fun engine(
        store: MemoryDeviceStore = MemoryDeviceStore(SelectedBluetoothDevice("OBDII", MAC)),
        factory: (SelectedBluetoothDevice) -> ObdConnection?,
    ): BluetoothSessionEngine =
        BluetoothSessionEngine(
            store = store,
            connectionFactory = factory,
            sleeper = {},
        )

    private class MemoryDeviceStore(
        private var device: SelectedBluetoothDevice = SelectedBluetoothDevice("", ""),
    ) : BluetoothSessionEngine.SelectedDeviceStore {
        override fun selectedDevice(): SelectedBluetoothDevice = device

        override fun saveSelectedDevice(device: SelectedBluetoothDevice) {
            this.device = device
        }

        override fun clearSelectedDevice() {
            device = SelectedBluetoothDevice("", "")
        }
    }

    private class FakeConnection(
        private val failOnCommands: Set<String> = emptySet(),
    ) : ObdConnection {
        val sentCommands = mutableListOf<String>()
        var closed = false
            private set

        override fun connect() {
            closed = false
        }

        override fun close() {
            closed = true
        }

        override fun send(command: ObdCommand): String {
            sentCommands += command.value
            if (command.value in failOnCommands) {
                error("read failed, socket might closed or timeout, read ret: -1")
            }
            return RESPONSES.getValue(command.value)
        }
    }

    private class CapturingPublisher : ObservationPublisher {
        val readings = mutableListOf<ObservationReading>()

        override fun publish(assetReference: String, readings: List<ObservationReading>): PublishResult {
            this.readings += readings
            return PublishResult(latencyMs = 12L)
        }
    }

    private companion object {
        const val MAC = "00:11:22:33:44:55"

        val RESPONSES = mapOf(
            "ATZ" to "ELM327 v1.5\r>",
            "ATE0" to "OK\r>",
            "ATL0" to "OK\r>",
            "ATS0" to "OK\r>",
            "ATH0" to "OK\r>",
            "ATSP0" to "OK\r>",
            "010C" to "410C1F40\r>",
            "0105" to "41055B\r>",
            "0142" to "41423930\r>",
        )
    }
}
