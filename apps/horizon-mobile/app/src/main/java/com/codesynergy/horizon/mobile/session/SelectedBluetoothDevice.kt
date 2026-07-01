package com.codesynergy.horizon.mobile.session

data class SelectedBluetoothDevice(
    val name: String,
    val address: String,
) {
    val displayName: String
        get() = name.ifBlank { address.ifBlank { "Nenhum dispositivo selecionado" } }

    val hasAddress: Boolean
        get() = address.isNotBlank()
}
