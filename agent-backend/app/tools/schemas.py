
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_user_balance",
            "description": "Obtém saldo de um usuário",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string"
                    }
                },
                "required": ["username"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_payment",
            "description": "Obtém informações de um pagamento",
            "parameters": {
                "type": "object",
                "properties": {
                    "payment_id": {
                        "type": "string"
                    }
                },
                "required": ["payment_id"]
            }
        }
    }
]