# exemplos/cap-08/sistema_de_alertas.py
import structlog

log = structlog.get_logger()

THRESHOLDS = {
    "latencia_p95_ms": 10_000,     # acima de 10s é lento demais
    "taxa_sucesso_minima": 0.90,    # abaixo de 90% é preocupante
    "guardrail_failures_hora": 15,  # 15 falhas/hora indica problema no contrato
    "tokens_medio_por_exec": 5_000, # acima disso, verificar se há loop
}

def verificar_e_alertar(metricas):
    resumo = metricas.resumo()

    if resumo["latencia_p95_ms"] > THRESHOLDS["latencia_p95_ms"]:
        log.warning("alerta_latencia",
            latencia_p95=resumo["latencia_p95_ms"],
            threshold=THRESHOLDS["latencia_p95_ms"],
            acao="verificar se API está lenta ou se há chamadas em loop",
        )

    if resumo["taxa_sucesso"] < THRESHOLDS["taxa_sucesso_minima"]:
        log.error("alerta_taxa_sucesso",
            taxa_atual=resumo["taxa_sucesso"],
            threshold=THRESHOLDS["taxa_sucesso_minima"],
            acao="verificar logs de erro recentes: provável mudança de comportamento do modelo",
        )

    if resumo["tokens_input_medio"] > THRESHOLDS["tokens_medio_por_exec"]:
        log.warning("alerta_tokens",
            tokens_medio=resumo["tokens_input_medio"],
            threshold=THRESHOLDS["tokens_medio_por_exec"],
            acao="verificar se input está sendo truncado corretamente",
        )
