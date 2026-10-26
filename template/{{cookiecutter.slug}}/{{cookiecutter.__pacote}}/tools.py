# {{ cookiecutter.__pacote }}/tools.py
# Tool Layer (cap. 4): schema completo, parâmetros validados antes de executar e resultado sempre no mesmo formato.
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, Field, ValidationError

from .security import Permissao


@dataclass
class ToolResult:
    sucesso: bool
    dados: Any
    erro: str | None = None

    def para_texto(self) -> str:
        if self.sucesso:
            return f"OK: {self.dados}"
        return f"ERRO: {self.erro}"


# IMPLEMENTE: troque a tool de exemplo pelas do seu agente.
class ContarPalavrasParams(BaseModel):
    texto: str = Field(min_length=1, description="Texto a contar")


def contar_palavras(params: ContarPalavrasParams) -> ToolResult:
    return ToolResult(sucesso=True, dados=len(params.texto.split()))


TOOLS: list[dict] = [
    {
        "name": "contar_palavras",
        "description": "Conta as palavras de um texto. Use quando precisar do tamanho exato de um trecho.",
        "input_schema": {
            "type": "object",
            "properties": {
                "texto": {"type": "string", "description": "Texto a contar. Ex.: 'revisar o PR 42'"},
            },
            "required": ["texto"],
        },
    },
]

# nome da tool -> (modelo dos parâmetros, executor, permissão exigida)
EXECUTORES: dict[str, tuple[type[BaseModel], Callable[[Any], ToolResult], Permissao]] = {
    "contar_palavras": (ContarPalavrasParams, contar_palavras, Permissao.LER),
}


def executar_tool(nome: str, parametros: dict, permissoes: frozenset) -> ToolResult:
    if nome not in EXECUTORES:
        return ToolResult(sucesso=False, dados=None, erro=f"tool '{nome}' não existe. Disponíveis: {sorted(EXECUTORES)}")
    modelo, executor, permissao = EXECUTORES[nome]
    if permissao not in permissoes:
        return ToolResult(sucesso=False, dados=None, erro=f"sem permissão '{permissao.value}' para a tool '{nome}'")
    try:
        params = modelo(**parametros)
    except ValidationError as e:
        return ToolResult(sucesso=False, dados=None, erro=f"parâmetros inválidos para '{nome}': {e.errors()[0]['msg']}")
    return executor(params)
