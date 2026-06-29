# exemplos/cap-07/execucao_completa.py
import time
import structlog

from contexto_execucao import iniciar_execucao, registrar_chamada_modelo, finalizar_execucao

log = structlog.get_logger()

def revisar_pr_completo(pr_numero: int, diff: str) -> dict:
    inicio = time.monotonic()
    execution_id = iniciar_execucao(pr_numero, diff)

    try:
        # Chamada 1: revisão principal
        t1 = time.monotonic()
        resposta = chamar_api(diff)
        registrar_chamada_modelo("claude-sonnet-4-6", len(diff)//4, round((time.monotonic()-t1)*1000))

        # Chamada 2: retry se necessário (execution_id propagado automaticamente)
        resultado = validar_com_retry(resposta, diff)

        duracao = round((time.monotonic() - inicio) * 1000)
        finalizar_execucao("ok", len(resultado["problemas"]), duracao)
        return resultado

    except Exception as e:
        duracao = round((time.monotonic() - inicio) * 1000)
        log.error("execucao_falhou", erro=type(e).__name__, duracao_ms=duracao)
        structlog.contextvars.clear_contextvars()
        raise

# Todos os logs desta execução terão execution_id="a1b2c3d4" e pr_numero=142
# Para investigar: filtrar logs por execution_id="a1b2c3d4"
