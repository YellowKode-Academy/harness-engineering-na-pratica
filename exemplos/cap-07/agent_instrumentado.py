# exemplos/cap-07/agent_instrumentado.py
import time
import uuid
import structlog

log = structlog.get_logger()

def revisar_com_logs_completos(diff: str, pr_numero: int) -> dict:
    execution_id = str(uuid.uuid4())[:8]
    inicio = time.monotonic()

    # Log de início com contexto que vai aparecer em todos os logs desta execução
    exec_log = log.bind(execution_id=execution_id, pr=pr_numero)
    exec_log.info("execucao_iniciada", tamanho_diff=len(diff), modelo="claude-sonnet-4-6")

    try:
        # Chamada ao modelo
        t_modelo = time.monotonic()
        resposta_bruta = chamar_api_com_retry(...)
        exec_log.info("modelo_chamado",
            duracao_ms=round((time.monotonic() - t_modelo) * 1000),
        )

        # Validação
        resultado = validar_output_code_review(resposta_bruta)

        # Fim com sucesso
        duracao = round((time.monotonic() - inicio) * 1000)
        exec_log.info("execucao_concluida",
            status="ok",
            duracao_ms=duracao,
            problemas_encontrados=len(resultado.problemas),
        )
        return resultado.model_dump()

    except Exception as e:
        duracao = round((time.monotonic() - inicio) * 1000)
        exec_log.error("execucao_falhou",
            erro=type(e).__name__,
            mensagem=str(e)[:200],
            duracao_ms=duracao,
        )
        raise
