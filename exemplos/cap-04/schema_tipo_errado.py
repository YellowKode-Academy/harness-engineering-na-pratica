# exemplos/cap-04/schema_tipo_errado.py

# Schema com problema: linha aceita qualquer coisa que "parece" número
schema_com_bug = {
    "name": "postar_comentario",
    "description": "posta um comentário no PR",
    "input_schema": {
        "type": "object",
        "properties": {
            "linha": {
                "description": "número da linha"
                # sem "type": "integer" explícito
            },
            "severidade": {"type": "string"},
            "descricao": {"type": "string"}
        },
        "required": ["linha", "severidade", "descricao"]
    }
}

# Schema corrigido: tipo obrigatório + constraint de valor mínimo
schema_corrigido = {
    "name": "postar_comentario",
    "description": "posta um comentário no PR",
    "input_schema": {
        "type": "object",
        "properties": {
            "linha": {
                "type": "integer",
                "minimum": 1,
                "description": "Número inteiro da linha. Ex: 42. Nunca string."
            },
            "severidade": {
                "type": "string",
                "enum": ["alta", "media", "baixa"]
            },
            "descricao": {
                "type": "string",
                "minLength": 10,
                "maxLength": 200
            }
        },
        "required": ["linha", "severidade", "descricao"]
    }
}
