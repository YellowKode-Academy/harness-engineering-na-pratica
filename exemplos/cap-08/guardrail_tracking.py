# exemplos/cap-08/guardrail_tracking.py
from dataclasses import dataclass

@dataclass
class GuardrailStats:
    total: int = 0
    falhas: int = 0

    def registrar(self, passou: bool):
        self.total += 1
        if not passou:
            self.falhas += 1

    def taxa_falha(self) -> float:
        return round(self.falhas / self.total, 3) if self.total else 0.0

stats = GuardrailStats()
# Após 200 execuções com 14 falhas:
# stats.taxa_falha()
# Output: 0.07  (7% de falha)
