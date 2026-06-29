# exemplos/cap-04/schema_comparacao.py

# Schema incompleto — o agente vai adivinhar em vários pontos
schema_incompleto = {
    "name": "postar_comentario",
    "description": "posta um comentário no PR",
    "input_schema": {
        "type": "object",
        "properties": {
            "linha": {"type": "integer"},
            "texto": {"type": "string"},
            "pr": {"type": "integer"},
        }
    }
}

# Schema completo — o agente tem especificação suficiente
schema_completo = {
    "name": "postar_comentario",
    "description": (
        "Posta um comentário de revisão em uma linha específica do pull request. "
        "Use apenas para problemas confirmados com localização exata no código."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "pr_numero": {
                "type": "integer",
                "description": "Número do pull request. Ex: 142"
            },
            "linha": {
                "type": "integer",
                "description": "Número da linha onde o problema está. Começa em 1."
            },
            "severidade": {
                "type": "string",
                "enum": ["alta", "media", "baixa"],
                "description": "alta = bloqueia merge; media = deve corrigir; baixa = sugestão"
            },
            "descricao": {
                "type": "string",
                "description": "Descrição do problema. Máximo 200 caracteres. Seja específico."
            }
        },
        "required": ["pr_numero", "linha", "severidade", "descricao"]
    }
}
