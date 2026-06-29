# exemplos/cap-03/context_window.py
def montar_mensagens_para_revisao(diff: str, pr_numero: int) -> list[dict]:
    """
    Monta apenas o que é necessário para revisar este PR.
    Não inclui histórico de outras revisões.
    """
    return [
        {
            "role": "user",
            "content": f"Revise o diff do PR #{pr_numero}:\n\n```diff\n{diff}\n```"
        }
    ]

def montar_mensagens_com_ferramenta(mensagens: list, resultado_tool: str) -> list[dict]:
    """
    Adiciona resultado de tool call para continuação da revisão.
    Usado quando o agente precisa ler um arquivo antes de completar.
    """
    return mensagens + [
        {"role": "assistant", "content": "[tool_use result]"},
        {"role": "user", "content": f"Resultado: {resultado_tool}"}
    ]
