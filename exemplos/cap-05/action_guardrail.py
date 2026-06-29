# exemplos/cap-05/action_guardrail.py
import structlog

log = structlog.get_logger()

def pr_existe_e_esta_aberto(pr_numero: int) -> bool:
    """
    Placeholder — implementação real consultaria a API do GitHub.
    Retorna True para PRs com número > 0 neste exemplo.
    """
    return pr_numero > 0

def _executar_post(pr_numero: int, linha: int, texto: str) -> dict:
    """Placeholder para execução real da postagem de comentário."""
    return {"status": "postado", "pr": pr_numero, "linha": linha}

def guardrail_postar_comentario(pr_numero: int, linha: int, texto: str) -> bool:
    """
    Verifica se é seguro postar o comentário antes de executar.
    Retorna True se seguro, False se deve bloquear.
    """
    # Verificação 1: comprimento do texto
    if len(texto) > 500:
        log.warning("guardrail_bloqueado", motivo="comentario_muito_longo", tamanho=len(texto))
        return False

    # Verificação 2: linha válida
    if linha <= 0:
        log.warning("guardrail_bloqueado", motivo="linha_invalida", linha=linha)
        return False

    # Verificação 3: PR existe (verificação de estado externo)
    if not pr_existe_e_esta_aberto(pr_numero):
        log.warning("guardrail_bloqueado", motivo="pr_nao_encontrado", pr=pr_numero)
        return False

    return True

def postar_comentario_com_guardrail(pr_numero: int, linha: int, texto: str) -> dict:
    if not guardrail_postar_comentario(pr_numero, linha, texto):
        return {"status": "bloqueado", "motivo": "verificar logs"}
    return _executar_post(pr_numero, linha, texto)
