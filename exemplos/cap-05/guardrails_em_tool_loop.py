# exemplos/cap-05/guardrails_em_tool_loop.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cap-04'))

from dataclasses import dataclass
from guardrail_layer import CodeReviewOutput
from guardrail_aplicar import GuardrailError, validar_output_code_review
from tools_definidas import TOOLS
from processar_tool_calls import executar_tool_call

@dataclass
class ToolCallResult:
    tool_name: str
    output: str
    bloqueado: bool = False
    motivo_bloqueio: str | None = None

def pr_existe_e_esta_aberto(pr_numero: int) -> bool:
    """
    Placeholder — implementação real consultaria a API do GitHub.
    Retorna True para PRs com número > 0 neste exemplo.
    """
    return pr_numero > 0

def validar_tool_call(tool_name: str, tool_input: dict) -> ToolCallResult | None:
    """
    Retorna None se a tool call é segura para executar.
    Retorna ToolCallResult com bloqueado=True se deve ser bloqueada.
    """
    if tool_name == "postar_comentario":
        # Guardrail de ação: verificar antes de qualquer efeito externo
        pr = tool_input.get("pr_numero")
        if not pr_existe_e_esta_aberto(pr):
            return ToolCallResult(
                tool_name=tool_name, output="",
                bloqueado=True,
                motivo_bloqueio=f"PR {pr} não existe ou está fechado"
            )
    return None  # seguro para executar

def executar_loop_com_guardrails(mensagens: list, system_prompt: str) -> dict:
    import anthropic
    client = anthropic.Anthropic()

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6", max_tokens=2048,
            system=system_prompt, messages=mensagens,
            tools=TOOLS
        )

        if response.stop_reason == "end_turn":
            # Guardrail na resposta final: validar antes de retornar
            output_final = response.content[0].text
            try:
                return validar_output_code_review(output_final).model_dump()
            except GuardrailError as e:
                return {"status": "guardrail_failure", "motivo": e.motivo}

        # Processar tool calls com guardrail antes de cada execução
        tool_results = []
        for bloco in response.content:
            if bloco.type != "tool_use":
                continue

            # Guardrail de ação ANTES de executar
            bloqueio = validar_tool_call(bloco.name, bloco.input)
            if bloqueio:
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": bloco.id,
                    "content": f"BLOQUEADO: {bloqueio.motivo_bloqueio}"
                })
            else:
                resultado = executar_tool_call(bloco.name, bloco.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": bloco.id,
                    "content": resultado
                })

        mensagens.extend([
            {"role": "assistant", "content": response.content},
            {"role": "user", "content": tool_results}
        ])
