
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
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": (
                "Pesquisa documentos internos da empresa, "
                "políticas, procedimentos, integrações, "
                "chargebacks, pagamentos e conhecimento corporativo."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string"
                    }
                },
                "required": ["query"]
            }
        }
    }
]