STORE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
            "description": "Уникальный идентификатор заказа"
        },
        "petId": {
            "type": "integer",
            "description": "Идентификатор питомца"
        },
        "quantity": {
            "type": "integer",
            "minimum": 1,
            "description": "Количество заказанных товаров"
        },
        "status": {
            "type": "string",
            "enum": ["placed", "approved", "delivered"],
            "description": "Статус заказа"
        },
        "complete": {
            "type": "boolean",
            "description": "Флаг завершения заказа"
        }
    },
    "required": ["id", "petId", "quantity", "status", "complete"],
    "additionalProperties": False
}
