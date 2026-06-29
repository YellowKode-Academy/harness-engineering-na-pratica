# exemplos/cap-04/tools_distintas.py

# Versão com descrições que distinguem claramente o caso de uso
tools_sem_ambiguidade = [
    {
        "name": "ler_arquivo",
        "description": (
            "Lê arquivos de texto do repositório: .py, .js, .ts, .go, .md, .json, .yaml, .toml. "
            "NÃO use para arquivos de lock (.lock), binários (.whl, .jar, .zip) ou imagens."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "caminho": {
                    "type": "string",
                    "description": "Ex: 'src/auth/login.py'. Apenas arquivos texto."
                }
            },
            "required": ["caminho"]
        }
    },
    {
        "name": "ler_arquivo_binario",
        "description": (
            "Lê arquivos que não são texto puro: .lock, .whl, .jar, .zip, imagens. "
            "Use quando o arquivo pode conter bytes não-UTF-8 ou é um formato binário. "
            "NÃO use para código-fonte ou arquivos de configuração texto."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "caminho": {
                    "type": "string",
                    "description": "Ex: 'poetry.lock', 'dist/package.whl'"
                }
            },
            "required": ["caminho"]
        }
    }
]
