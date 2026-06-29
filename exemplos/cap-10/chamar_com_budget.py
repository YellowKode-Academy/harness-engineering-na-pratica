# exemplos/cap-10/chamar_com_budget.py
import anthropic
from budget_enforcer import BudgetEnforcer, BudgetExcedidoError

client = anthropic.Anthropic()

def chamar_modelo_com_budget(mensagens: list, system: str, budget: BudgetEnforcer) -> str:
    # Estimativa de tokens: 1 token ≈ 4 caracteres (aproximação comum)
    tokens_estimados = sum(len(m["content"]) // 4 for m in mensagens) + len(system) // 4
    budget.verificar_antes_de_chamar(tokens_estimados)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=system,
        messages=mensagens,
    )

    # Registra consumo real (não estimado) após a chamada
    budget.registrar_consumo(
        response.usage.input_tokens,
        response.usage.output_tokens
    )
    return response.content[0].text

# Uso:
# budget = BudgetEnforcer(limite_por_execucao=10_000)
# Na 4ª ou 5ª iteração do loop, BudgetExcedidoError interrompe a execução
