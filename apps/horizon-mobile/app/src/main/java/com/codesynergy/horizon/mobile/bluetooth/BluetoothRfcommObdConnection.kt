package com.codesynergy.horizon.mobile.bluetooth

import android.bluetooth.BluetoothDevice

class BluetoothRfcommObdConnection(
    device: BluetoothDevice,
) : RfcommSocketSession(device)
