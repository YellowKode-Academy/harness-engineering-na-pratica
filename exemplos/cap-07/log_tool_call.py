# exemplos/cap-07/log_tool_call.py
import time
import structlog

log = structlog.get_logger()

def executar_ferramenta_com_log(
    nome: str, parametros: dict, execution_id: str
) -> str:
    tool_log = log.bind(execution_id=execution_id, ferramenta=nome)
    inicio = time.monotonic()

    tool_log.info("ferramenta_chamada",
        params=str(parametros)[:200]  # resumo dos parâmetros
    )

    resultado = executar_ferramenta(nome, parametros)
    duracao = round((time.monotonic() - inicio) * 1000)

    if resultado.sucesso:
        tool_log.info("ferramenta_ok",
            duracao_ms=duracao,
            resultado_tamanho=len(str(resultado.dados)),
        )
    else:
        tool_log.warning("ferramenta_falhou",
            duracao_ms=duracao,
            erro=resultado.erro,
        )

    return resultado.para_texto()

# Output para chamada bem-sucedida:
# {"event": "ferramenta_chamada", "execution_id": "a1b2c3d4", "ferramenta": "ler_arquivo", "params": "..."}
# {"event": "ferramenta_ok", "execution_id": "a1b2c3d4", "ferramenta": "ler_arquivo", "duracao_ms": 45, ...}
