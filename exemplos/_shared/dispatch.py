"""Dispatcher genérico de tool calls para exemplos que precisam de executar_ferramenta."""
from __future__ import annotations
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "cap-04"))


def executar_ferramenta(tool_name: str, tool_input: dict):
    """Roteia tool_name para o executor correto. Importa cap-04 sob demanda."""
    try:
        from processar_tool_calls import executar_tool_call

        return executar_tool_call(tool_name, tool_input)
    except ImportError:
        from github_client import ToolResult

        return ToolResult(sucesso=False, erro=f"executor não disponível para {tool_name}")
