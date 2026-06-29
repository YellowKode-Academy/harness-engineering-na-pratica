# exemplos/cap-04/tools_ambiguas.py

# Versão com descrições ambíguas — o modelo vai errar
tools_com_ambiguidade = [
    {
        "name": "ler_arquivo",
        "description": "Lê um arquivo do repositório.",
        "input_schema": {
            "type": "object",
            "properties": {
                "caminho": {"type": "string"}
            },
            "required": ["caminho"]
        }
    },
    {
        "name": "ler_arquivo_binario",
        "description": "Lê um arquivo binário do repositório.",
        "input_schema": {
            "type": "object",
            "properties": {
                "caminho": {"type": "string"}
            },
            "required": ["caminho"]
        }
    }
]
