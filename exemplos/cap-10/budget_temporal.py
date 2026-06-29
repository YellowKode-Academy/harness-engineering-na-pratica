# exemplos/cap-10/budget_temporal.py
import json
import datetime
from pathlib import Path
from dataclasses import dataclass, field
from budget_enforcer import BudgetExcedidoError

ARQUIVO_CONSUMO = Path("consumo_budget.json")

@dataclass
class BudgetTemporal:
    limite_diario_tokens: int = 100_000
    limite_mensal_tokens: int = 2_000_000
    _dados: dict = field(default_factory=dict)

    def _carregar(self) -> dict:
        if ARQUIVO_CONSUMO.exists():
            return json.loads(ARQUIVO_CONSUMO.read_text())
        return {"dia": "", "mes": "", "tokens_dia": 0, "tokens_mes": 0}

    def _salvar(self, dados: dict):
        ARQUIVO_CONSUMO.write_text(json.dumps(dados, ensure_ascii=False))

    def registrar_e_verificar(self, tokens: int) -> dict:
        agora = datetime.datetime.utcnow()
        dia_atual = agora.strftime("%Y-%m-%d")
        mes_atual = agora.strftime("%Y-%m")

        dados = self._carregar()

        if dados.get("dia") != dia_atual:
            dados["dia"] = dia_atual
            dados["tokens_dia"] = 0

        if dados.get("mes") != mes_atual:
            dados["mes"] = mes_atual
            dados["tokens_mes"] = 0

        dados["tokens_dia"] += tokens
        dados["tokens_mes"] += tokens
        self._salvar(dados)

        pct_dia = dados["tokens_dia"] / self.limite_diario_tokens
        pct_mes = dados["tokens_mes"] / self.limite_mensal_tokens

        alertas = []
        if pct_mes >= 1.0:
            raise BudgetExcedidoError(dados["tokens_mes"], self.limite_mensal_tokens)
        if pct_mes >= 0.9:
            alertas.append("ALERTA: 90% do budget mensal consumido")
        elif pct_mes >= 0.7:
            alertas.append("AVISO: 70% do budget mensal consumido")
        if pct_dia >= 1.0:
            raise BudgetExcedidoError(dados["tokens_dia"], self.limite_diario_tokens)

        return {"tokens_dia": dados["tokens_dia"], "tokens_mes": dados["tokens_mes"],
                "pct_dia": round(pct_dia, 3), "pct_mes": round(pct_mes, 3),
                "alertas": alertas}

# Output quando consumo do mês atinge 71%:
# {'tokens_dia': 12300, 'tokens_mes': 1420000, 'pct_dia': 0.123, 'pct_mes': 0.71,
#  'alertas': ['AVISO: 70% do budget mensal consumido']}
