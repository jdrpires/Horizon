package com.codesynergy.horizon.mobile.session

import com.codesynergy.horizon.mobile.bluetooth.ObdConnection
import com.codesynergy.horizon.mobile.model.ObdCommand
import com.codesynergy.horizon.mobile.model.ObdCommands
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertNotEquals
import kotlin.test.assertNull
import kotlin.test.assertTrue

class BluetoothSessionControllerTest {
    @Test
    fun preservesSelectedDevice() {
        val store = MemoryDeviceStore()
        val controller = controller(store)

        controller.select(SelectedBluetoothDevice("OBDII", "00:11:22:33:44:55"))

        assertEquals("OBDII", controller.selectedDevice.name)
        assertEquals("00:11:22:33:44:55", controller.selectedDevice.address)
    }

    @Test
    fun selectedMacDoesNotChangeWhenPairedListChanges() {
        val store = MemoryDeviceStore(
            SelectedBluetoothDevice("OBDII", "00:11:22:33:44:55"),
        )
        val controller = controller(store)
        val refreshedDevices = listOf(
            SelectedBluetoothDevice("Phone", "AA:AA:AA:AA:AA:AA"),
            SelectedBluetoothDevice("Scanner", "BB:BB:BB:BB:BB:BB"),
        )

        assertTrue(refreshedDevices.none { it.address == controller.selectedDevice.address })
        assertEquals("00:11:22:33:44:55", controller.selectedDevice.address)
    }

    @Test
    fun readingLoopUsesSameSelectedDevice() {
        val store = MemoryDeviceStore(
            SelectedBluetoothDevice("OBDII", "00:11:22:33:44:55"),
        )
        val factoryAddresses = mutableListOf<String>()
        val connection = FakeConnection()
        val controller = controller(store) { selected ->
            factoryAddresses += selected.address
            connection
        }

        assertTrue(controller.startReading())
        val response = controller.withConnection { it.send(ObdCommands.rpm) }

        assertEquals("OK", response)
        assertEquals(listOf("00:11:22:33:44:55"), factoryAddresses)
        assertEquals(listOf("010C"), connection.sentCommands)
    }

    @Test
    fun readFailureReconnectsUsingSameMacAddress() {
        val store = MemoryDeviceStore(
            SelectedBluetoothDevice("OBDII", "00:11:22:33:44:55"),
        )
        val factoryAddresses = mutableListOf<String>()
        val first = FakeConnection(failOnSend = true)
        val second = FakeConnection()
        val connections = mutableListOf(first, second)
        val controller = controller(store) { selected ->
            factoryAddresses += selected.address
            if (connections.isNotEmpty()) connections.removeAt(0) else second
        }

        assertTrue(controller.startReading())
        val response = controller.withConnection { it.send(ObdCommands.rpm) }

        assertNull(response)
        assertEquals(
            listOf("00:11:22:33:44:55", "00:11:22:33:44:55"),
            factoryAddresses.take(2),
        )
        assertEquals(BluetoothSessionState.READING, controller.state)
        assertEquals(1, controller.reconnectAttempts)
    }

    @Test
    fun doesNotReconnectToDifferentDevice() {
        val store = MemoryDeviceStore(
            SelectedBluetoothDevice("OBDII", "00:11:22:33:44:55"),
        )
        val unwantedMac = "AA:AA:AA:AA:AA:AA"
        val factoryAddresses = mutableListOf<String>()
        val controller = controller(store) { selected ->
            factoryAddresses += selected.address
            assertNotEquals(unwantedMac, selected.address)
            FakeConnection(failOnSend = factoryAddresses.size == 1)
        }

        assertTrue(controller.startReading())
        controller.withConnection { it.send(ObdCommands.rpm) }

        assertTrue(factoryAddresses.all { it == "00:11:22:33:44:55" })
    }

    private fun controller(
        store: MemoryDeviceStore,
        factory: (SelectedBluetoothDevice) -> ObdConnection? = { FakeConnection() },
    ): BluetoothSessionController =
        BluetoothSessionController(
            store = store,
            connectionFactory = factory,
            initializer = {},
            sleeper = {},
        )

    private class MemoryDeviceStore(
        private var device: SelectedBluetoothDevice = SelectedBluetoothDevice("", ""),
    ) : BluetoothSessionController.SelectedDeviceStore {
        override fun selectedDevice(): SelectedBluetoothDevice = device

        override fun saveSelectedDevice(device: SelectedBluetoothDevice) {
            this.device = device
        }

        override fun clearSelectedDevice() {
            device = SelectedBluetoothDevice("", "")
        }
    }

    private class FakeConnection(
        private val failOnSend: Boolean = false,
    ) : ObdConnection {
        val sentCommands = mutableListOf<String>()

        override fun connect() = Unit

        override fun close() = Unit

        override fun send(command: ObdCommand): String {
            sentCommands += command.value
            if (failOnSend) error("read failed")
            return "OK"
        }
    }
}
