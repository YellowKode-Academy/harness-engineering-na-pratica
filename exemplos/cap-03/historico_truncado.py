# exemplos/cap-03/historico_truncado.py
def truncar_historico(
    mensagens: list[dict],
    limite_tokens_estimado: int = 8000,
    tokens_por_mensagem_estimado: int = 200,
) -> list[dict]:
    """
    Mantém as N mensagens mais recentes que cabem no limite.
    Sempre inclui a primeira mensagem (contexto inicial da conversa).
    """
    if not mensagens:
        return []

    limite_mensagens = limite_tokens_estimado // tokens_por_mensagem_estimado

    if len(mensagens) <= limite_mensagens:
        return mensagens

    # primeira mensagem: contexto inicial que sempre vale preservar
    primeira = mensagens[0]
    # mensagens mais recentes dentro do limite
    recentes = mensagens[-(limite_mensagens - 1):]

    return [primeira] + recentes

# Uso no Code Review Agent (suporte com histórico):
historico_completo = [...]  # 30 mensagens acumuladas
historico_util = truncar_historico(historico_completo, limite_tokens_estimado=6000)
# Output: primeiras + últimas ~29 mensagens dentro do limite, não as 30 completas
