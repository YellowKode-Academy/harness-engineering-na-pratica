# exemplos/cap-04/processar_tool_calls.py
import json
from tool_result import ler_arquivo, ToolResult

# Placeholder para a função de postagem de comentários no GitHub
# (implementação real integraria com a API do GitHub)
def postar_comentario_no_github(**params) -> ToolResult:
    raise NotImplementedError("integração com GitHub não implementada neste exemplo")

EXECUTORES_DE_TOOL = {
    "ler_arquivo": lambda params: ler_arquivo(**params),
    "postar_comentario": lambda params: postar_comentario_no_github(**params),
}

def executar_tool_call(tool_name: str, tool_input: dict) -> str:
    if tool_name not in EXECUTORES_DE_TOOL:
        return f"ERRO: ferramenta '{tool_name}' não existe"

    executor = EXECUTORES_DE_TOOL[tool_name]
    resultado = executor(tool_input)
    return resultado.para_texto()

# Uso: o modelo retorna tool_use blocks que você processa em loop
# tool_block.name → nome da ferramenta
# tool_block.input → parâmetros como dict
# executar_tool_call(tool_block.name, tool_block.input) → string de resultado
