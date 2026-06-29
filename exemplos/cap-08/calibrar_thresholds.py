# exemplos/cap-08/calibrar_thresholds.py
from statistics import median, quantiles
from datetime import datetime, timedelta

def calcular_thresholds_historicos(historico_7d: list[dict]) -> dict:
    latencias = [r["latencia_p95_ms"] for r in historico_7d]
    custos = [r["custo_usd"] for r in historico_7d]
    taxas_sucesso = [r["taxa_sucesso"] for r in historico_7d]

    lat_p95_normal = quantiles(sorted(latencias), n=20)[18]
    custo_mediano = median(custos)
    sucesso_minimo = min(taxas_sucesso)

    return {
        "latencia_p95_threshold": round(lat_p95_normal * 1.5, 0),
        "custo_diario_threshold": round(custo_mediano * 2.0, 4),
        "taxa_sucesso_minima": round(sucesso_minimo * 0.9, 3),
    }

# Dados de 7 dias com p95 normal de 6.000ms, custo mediano 0.05 USD, sucesso 0.96
# calcular_thresholds_historicos(historico)
# Output: {"latencia_p95_threshold": 9000.0, "custo_diario_threshold": 0.1, "taxa_sucesso_minima": 0.864}
