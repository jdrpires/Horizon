package com.codesynergy.horizon.mobile.network

import kotlin.test.Test
import kotlin.test.assertContains

class GatewayErrorMessageTest {
    @Test
    fun exposesResponseBodyForValidationError() {
        val message = GatewayErrorMessage.friendly(
            statusCode = 422,
            body = """{"detail":"asset_id is required"}""",
        )

        assertContains(message, "Asset inexistente ou inválido.")
        assertContains(message, "asset_id is required")
    }

    @Test
    fun exposesDefinitionErrors() {
        val message = GatewayErrorMessage.friendly(
            statusCode = 422,
            body = """{"detail":"definition_id not found"}""",
        )

        assertContains(message, "Definition inválida.")
        assertContains(message, "definition_id not found")
    }
}
