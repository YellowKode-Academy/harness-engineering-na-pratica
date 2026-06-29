# exemplos/cap-08/metricas_locais.py
import time
from dataclasses import dataclass, field
from statistics import median, quantiles

@dataclass
class MetricasAgente:
    tokens_input: list[int] = field(default_factory=list)
    tokens_output: list[int] = field(default_factory=list)
    latencias_ms: list[float] = field(default_factory=list)
    retries_total: int = 0
    guardrail_failures: int = 0
    execucoes_ok: int = 0
    execucoes_erro: int = 0

    def registrar_execucao(self, tokens_in: int, tokens_out: int,
                           duracao_ms: float, sucesso: bool, retries: int = 0):
        self.tokens_input.append(tokens_in)
        self.tokens_output.append(tokens_out)
        self.latencias_ms.append(duracao_ms)
        self.retries_total += retries
        if sucesso:
            self.execucoes_ok += 1
        else:
            self.execucoes_erro += 1

    def resumo(self) -> dict:
        total = self.execucoes_ok + self.execucoes_erro
        if not total:
            return {"erro": "nenhuma execução registrada"}

        lat = sorted(self.latencias_ms)
        return {
            "total_execucoes": total,
            "taxa_sucesso": round(self.execucoes_ok / total, 3),
            "latencia_p50_ms": round(median(lat)) if lat else 0,
            "latencia_p95_ms": round(quantiles(lat, n=20)[18]) if len(lat) >= 20 else max(lat, default=0),
            "tokens_input_medio": round(sum(self.tokens_input) / len(self.tokens_input)) if self.tokens_input else 0,
            "tokens_output_medio": round(sum(self.tokens_output) / len(self.tokens_output)) if self.tokens_output else 0,
            "taxa_retry": round(self.retries_total / total, 3) if total else 0,
            "guardrail_failures": self.guardrail_failures,
        }

metricas = MetricasAgente()
# Após 100 execuções:
# metricas.resumo() →
# {"total_execucoes": 100, "taxa_sucesso": 0.94, "latencia_p50_ms": 2340, ...}
