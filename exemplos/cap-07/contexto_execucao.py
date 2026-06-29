# exemplos/cap-07/contexto_execucao.py
import uuid
import time
import structlog
import contextvars

# Variável de contexto: disponível em qualquer função chamada a partir da execução
_execution_id: contextvars.ContextVar[str] = contextvars.ContextVar(
    "execution_id", default="sem-contexto"
)

log = structlog.get_logger()

def iniciar_execucao(pr_numero: int, diff: str) -> str:
    """
    Inicia uma execução e configura o contexto de log.
    Retorna o execution_id para referência externa.
    """
    execution_id = str(uuid.uuid4())[:8]
    _execution_id.set(execution_id)

    # Configura contexto global do structlog para esta execução
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        execution_id=execution_id,
        pr_numero=pr_numero,
        input_hash=str(hash(diff))[:6],
    )

    log.info(
        "execucao_iniciada",
        tamanho_diff=len(diff),
        modelo="claude-sonnet-4-6",
    )
    return execution_id

def registrar_chamada_modelo(modelo: str, tokens_input: int, duracao_ms: int):
    """Loga uma chamada ao modelo com contexto automático da execução."""
    log.info(
        "modelo_chamado",
        modelo=modelo,
        tokens_input=tokens_input,
        duracao_ms=duracao_ms,
    )
    # Output inclui automaticamente execution_id e pr_numero do contexto:
    # {"event": "modelo_chamado", "execution_id": "a1b2c3d4", "pr_numero": 142,
    #  "modelo": "claude-sonnet-4-6", "tokens_input": 3200, "duracao_ms": 2100}

def finalizar_execucao(status: str, problemas: int, duracao_ms: int):
    """Loga o fim da execução e limpa o contexto."""
    log.info(
        "execucao_concluida",
        status=status,
        problemas_encontrados=problemas,
        duracao_ms=duracao_ms,
    )
    structlog.contextvars.clear_contextvars()
