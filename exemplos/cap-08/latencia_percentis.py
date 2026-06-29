# exemplos/cap-08/latencia_percentis.py
import time
from statistics import median, quantiles

latencias = []

def medir_latencia(func, *args):
    inicio = time.monotonic()
    resultado = func(*args)
    duracao_ms = (time.monotonic() - inicio) * 1000
    latencias.append(duracao_ms)
    return resultado

def calcular_percentis(dados: list[float]) -> dict:
    if len(dados) < 20:
        return {"p50": median(dados), "p95": max(dados), "aviso": "amostra pequena"}
    lat_sorted = sorted(dados)
    return {
        "p50": round(median(lat_sorted), 1),
        "p95": round(quantiles(lat_sorted, n=20)[18], 1),
    }

# Após 100 execuções:
# calcular_percentis(latencias)
# Output: {"p50": 2340.5, "p95": 8120.3}
