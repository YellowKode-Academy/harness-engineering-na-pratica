# exemplos/cap-11/revisar.py
# A função que os testes com fixtures (tests/unit/test_com_fixtures.py) exercitam:
# confere o budget antes de chamar o modelo e valida a resposta com o guardrail do cap. 5.
from budget_enforcer import BudgetEnforcer
from guardrail_aplicar import validar_output_code_review

SYSTEM_PROMPT = (
    "Você é um revisor de código Python. Analise o diff e retorne SOMENTE JSON no formato: "
    '{"problemas": [{"linha": int, "severidade": "alta|media|baixa", "descricao": str}]}. '
    'Se não houver problemas: {"problemas": []}'
)


def revisar_diff(diff: str, client, budget: BudgetEnforcer | None = None,
                 modelo: str = "claude-sonnet-4-6") -> dict:
    budget = budget or BudgetEnforcer()
    budget.verificar_antes_de_chamar(len(diff) // 4 + 1)  # cerca de 4 caracteres por token

    resposta = client.messages.create(
        model=modelo,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"Revise este diff:\n\n{diff}"}],
    )
    budget.registrar_consumo(resposta.usage.input_tokens, resposta.usage.output_tokens)
    return validar_output_code_review(resposta.content[0].text).model_dump()
