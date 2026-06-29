# exemplos/cap-09/permissoes_multi_agente.py
from dataclasses import dataclass
from allowlist_dinamica import ContextoDeExecucao

@dataclass
class Pipeline:
    orquestrador_ctx: ContextoDeExecucao
    analisador_ctx: ContextoDeExecucao
    reporter_ctx: ContextoDeExecucao

def criar_pipeline_review(pr_numero: int) -> Pipeline:
    exec_id = f"pr-{pr_numero}"
    return Pipeline(
        # Orquestrador: só coordena, não executa ferramentas de código
        orquestrador_ctx=ContextoDeExecucao(
            tipo="orquestracao",
            exec_id=f"{exec_id}-orch",
        ),
        # Analisador: lê arquivos, não posta nada
        analisador_ctx=ContextoDeExecucao(
            tipo="analise_leitura",
            exec_id=f"{exec_id}-anal",
        ),
        # Reporter: posta comentários, não lê código
        reporter_ctx=ContextoDeExecucao(
            tipo="postagem_resultado",
            exec_id=f"{exec_id}-repo",
        ),
    )
# ESCOPOS_POR_TIPO["orquestracao"] = frozenset()  # nenhuma ferramenta de I/O
# ESCOPOS_POR_TIPO["analise_leitura"] = frozenset({LER_ARQUIVO, LER_PR_INFO})
# ESCOPOS_POR_TIPO["postagem_resultado"] = frozenset({POSTAR_COMENTARIO})
