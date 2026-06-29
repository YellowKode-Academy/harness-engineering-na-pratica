# exemplos/cap-12/monitorar_deploy.py
import time
import statistics

def coletar_metricas_janela(duracao_minutos: int = 30) -> dict:
    """
    Coleta métricas do período pós-deploy e compara com baseline de 7 dias.
    Retorna dicionário com status de cada métrica.
    """
    # Em produção real, essas funções consultam seu sistema de métricas
    metricas_atuais = coletar_metricas_recentes(duracao_minutos)
    baseline_7d = coletar_baseline_historico(dias=7)

    resultado = {}

    # Taxa de erro: alerta se > 2x do baseline
    taxa_erro_atual = metricas_atuais["taxa_erro"]
    taxa_erro_base = baseline_7d["taxa_erro"]
    resultado["taxa_erro"] = {
        "atual": taxa_erro_atual,
        "baseline": taxa_erro_base,
        "desvio": taxa_erro_atual / max(taxa_erro_base, 0.001),
        "status": "alerta" if taxa_erro_atual > taxa_erro_base * 2 else "ok",
    }

    # Latência p95: alerta se > 1.5x do baseline
    p95_atual = metricas_atuais["latencia_p95_ms"]
    p95_base = baseline_7d["latencia_p95_ms"]
    resultado["latencia_p95"] = {
        "atual": p95_atual,
        "baseline": p95_base,
        "desvio": p95_atual / max(p95_base, 1),
        "status": "alerta" if p95_atual > p95_base * 1.5 else "ok",
    }

    # Custo por execução: alerta se > 1.3x do baseline
    custo_atual = metricas_atuais["custo_por_exec_usd"]
    custo_base = baseline_7d["custo_por_exec_usd"]
    resultado["custo_por_exec"] = {
        "atual": custo_atual,
        "baseline": custo_base,
        "desvio": custo_atual / max(custo_base, 0.0001),
        "status": "alerta" if custo_atual > custo_base * 1.3 else "ok",
    }

    alertas = [k for k, v in resultado.items() if v["status"] == "alerta"]
    resultado["_resumo"] = {
        "alertas": alertas,
        "deploy_saudavel": len(alertas) == 0,
    }

    return resultado
