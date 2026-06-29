# exemplos/cap-10/investigar_incidente.py
import json
from collections import defaultdict

def reconstruir_execucao(arquivo: str, execution_id: str) -> dict:
    eventos = []
    with open(arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            r = json.loads(linha)
            if r.get("execution_id") == execution_id:
                eventos.append(r)

    tokens_total = sum(r.get("tokens_input", 0) + r.get("tokens_output", 0)
                       for r in eventos)

    return {
        "execution_id": execution_id,
        "eventos": eventos,
        "total_eventos": len(eventos),
        "tokens_total": tokens_total,
        "custo_usd_estimado": round(tokens_total / 1_000_000 * 3.0, 4),
    }

def top_execucoes_por_custo(arquivo: str, top_n: int = 5) -> list:
    consumo_por_execucao = defaultdict(int)
    for linha in open(arquivo, "r", encoding="utf-8"):
        r = json.loads(linha)
        eid = r.get("execution_id", "desconhecido")
        consumo_por_execucao[eid] += r.get("tokens_input", 0) + r.get("tokens_output", 0)

    ordenado = sorted(consumo_por_execucao.items(), key=lambda x: x[1], reverse=True)
    return [{"execution_id": k, "tokens": v} for k, v in ordenado[:top_n]]

# Output: [{'execution_id': 'a1b2c3d4', 'tokens': 182000},
#           {'execution_id': 'f9e8d7c6', 'tokens': 8200}, ...]
