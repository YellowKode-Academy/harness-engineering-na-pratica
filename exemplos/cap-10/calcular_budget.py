# exemplos/cap-10/calcular_budget.py
import json
import statistics
from pathlib import Path

def calcular_budget_recomendado(arquivo_audit: str = "audit.jsonl") -> dict:
    registros = []
    with open(arquivo_audit, "r", encoding="utf-8") as f:
        for linha in f:
            r = json.loads(linha)
            if r.get("evento") == "revisao_concluida" and "tokens_total" in r:
                registros.append(r["tokens_total"])

    if len(registros) < 5:
        return {"erro": "Poucas execuções para calcular. Precisamos de pelo menos 5."}

    media = statistics.mean(registros)
    desvio = statistics.stdev(registros)
    registros_sorted = sorted(registros)
    idx_p95 = max(0, int(len(registros_sorted) * 0.95) - 1)
    p95 = registros_sorted[idx_p95]

    budget_recomendado = int(p95 * 2)
    teto_maximo = int(media * 10)  # interrompe um loop com 10 iterações extras

    return {
        "execucoes_analisadas": len(registros),
        "media_tokens": round(media),
        "desvio_padrao": round(desvio),
        "p95_tokens": round(p95),
        "budget_recomendado": budget_recomendado,
        "teto_maximo": teto_maximo,
    }

# Output: {'execucoes_analisadas': 25, 'media_tokens': 3200, 'desvio_padrao': 890,
#          'p95_tokens': 5100, 'budget_recomendado': 10200, 'teto_maximo': 32000}
