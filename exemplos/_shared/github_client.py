"""Stubs para GitHub API. Em produção, substituir por chamadas reais com GITHUB_TOKEN."""
from __future__ import annotations
import os
import logging

log = logging.getLogger(__name__)


class ToolResult:
    """Resultado tipado de uma tool call (espelho simplificado de cap-04/tool_result.py)."""

    def __init__(self, sucesso: bool, dados=None, erro: str | None = None):
        self.sucesso = sucesso
        self.dados = dados
        self.erro = erro

    def para_texto(self) -> str:
        if self.sucesso:
            return f"OK: {self.dados}"
        return f"ERRO: {self.erro}"


def pr_existe_e_esta_aberto(pr_numero: int) -> bool:
    """Verifica se o PR existe e está aberto. Stub: retorna True se sem token."""
    token = os.getenv("GITHUB_TOKEN", "")
    if not token:
        log.debug("GITHUB_TOKEN ausente — assumindo PR %s aberto", pr_numero)
        return True
    # TODO: GET /repos/{owner}/{repo}/pulls/{pr_numero}
    return True


def postar_comentario_no_github(
    pr_numero: int, linha: int, severidade: str, descricao: str
) -> ToolResult:
    """Posta comentário de revisão no PR. Stub: só loga, não faz request real."""
    token = os.getenv("GITHUB_TOKEN", "")
    if token:
        log.info(
            "comentario_postado",
            pr=pr_numero,
            linha=linha,
            severidade=severidade,
            descricao=descricao[:80],
        )
        return ToolResult(sucesso=True, dados={"pr": pr_numero, "linha": linha})
    log.warning("GITHUB_TOKEN ausente — comentário não enviado")
    return ToolResult(sucesso=True, dados={"stub": True, "pr": pr_numero})


def _executar_post_github(pr_numero: int, linha: int, texto: str) -> bool:
    """Executa POST de comentário. Stub: sempre retorna True."""
    log.debug("_executar_post_github pr=%s linha=%s", pr_numero, linha)
    return True


def coletar_metricas_recentes(n: int = 50) -> list[dict]:
    """Retorna amostra de métricas recentes (stub para testes sem DB)."""
    import random, time

    base = time.time()
    return [
        {
            "timestamp": base - i * 60,
            "latencia_p95": round(random.uniform(2.0, 8.0), 2),
            "custo_usd": round(random.uniform(0.01, 0.08), 4),
            "taxa_guardrail": round(random.uniform(0.0, 0.15), 3),
            "taxa_retry": round(random.uniform(0.0, 0.3), 3),
        }
        for i in range(n)
    ]


def coletar_baseline_historico(dias: int = 7) -> list[dict]:
    """Retorna histórico de N dias (stub)."""
    import random, time

    base = time.time()
    return [
        {
            "timestamp": base - i * 3600,
            "latencia_p95": round(random.uniform(3.0, 6.0), 2),
            "custo_usd": round(random.uniform(0.02, 0.06), 4),
        }
        for i in range(dias * 24)
    ]
