# exemplos/cap-10/budget_enforcer.py
import anthropic
from dataclasses import dataclass, field

class BudgetExcedidoError(Exception):
    def __init__(self, consumido: int, limite: int):
        self.consumido = consumido
        self.limite = limite
        super().__init__(f"Budget excedido: {consumido} tokens consumidos de {limite} permitidos")

@dataclass
class BudgetEnforcer:
    limite_por_execucao: int = 10_000
    tokens_consumidos: int = 0

    def verificar_antes_de_chamar(self, tokens_estimados: int):
        projecao = self.tokens_consumidos + tokens_estimados
        if projecao > self.limite_por_execucao:
            raise BudgetExcedidoError(self.tokens_consumidos, self.limite_por_execucao)

    def registrar_consumo(self, tokens_input: int, tokens_output: int):
        self.tokens_consumidos += tokens_input + tokens_output

    def percentual_consumido(self) -> float:
        return self.tokens_consumidos / self.limite_por_execucao
