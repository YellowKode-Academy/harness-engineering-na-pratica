# exemplos/cap-04/tools_definidas.py
TOOLS = [
    {
        "name": "ler_arquivo",
        "description": (
            "Lê o conteúdo de um arquivo no repositório. "
            "Use antes de postar um comentário quando precisar ver o código completo de uma função ou classe."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "caminho": {
                    "type": "string",
                    "description": "Caminho relativo ao repositório. Ex: 'src/auth/login.py'"
                },
                "linhas": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "Linhas específicas a ler. Ex: [10, 11, 12]. Omitir para ler o arquivo inteiro."
                }
            },
            "required": ["caminho"]
        }
    },
    {
        "name": "postar_comentario",
        "description": "Posta comentário de revisão no PR. Use apenas para problemas confirmados com linha exata.",
        "input_schema": {
            "type": "object",
            "properties": {
                "pr_numero": {"type": "integer", "description": "Número do PR"},
                "linha": {"type": "integer", "description": "Linha onde está o problema"},
                "severidade": {
                    "type": "string",
                    "enum": ["alta", "media", "baixa"],
                    "description": "alta bloqueia merge; media deve corrigir; baixa é sugestão"
                },
                "descricao": {"type": "string", "description": "Descrição do problema (máx 200 chars)"}
            },
            "required": ["pr_numero", "linha", "severidade", "descricao"]
        }
    }
]
