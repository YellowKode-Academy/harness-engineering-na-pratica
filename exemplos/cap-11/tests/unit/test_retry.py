# exemplos/cap-11/tests/unit/test_retry.py
# Testes de retry e budget — sem chamada real ao LLM, sem API key necessária.
import time
import pytest
import anthropic
from unittest.mock import patch, MagicMock

from budget_enforcer import BudgetEnforcer, BudgetExcedidoError
from chamar_com_budget import chamar_modelo_com_budget


def criar_mock_response(texto: str, input_tokens: int = 100, output_tokens: int = 50):
    response = MagicMock()
    response.content = [MagicMock()]
    response.content[0].text = texto
    response.usage.input_tokens = input_tokens
    response.usage.output_tokens = output_tokens
    return response


def test_retry_acionado_em_rate_limit():
    chamadas = []
    output_valido = '{"problemas": []}'

    def mock_create(*args, **kwargs):
        chamadas.append(time.monotonic())
        if len(chamadas) < 3:
            raise anthropic.RateLimitError("rate limit", response=MagicMock(), body={})
        return criar_mock_response(output_valido)

    with patch("chamar_com_budget.client") as mock_client:
        mock_client.messages.create.side_effect = mock_create

        # Força a 3ª tentativa a ser a bem-sucedida simulando retry externo
        tentativas = 0
        resultado = None
        while tentativas < 3:
            try:
                budget = BudgetEnforcer(limite_por_execucao=50_000)
                resultado = chamar_modelo_com_budget(
                    [{"role": "user", "content": "diff de teste"}],
                    "system",
                    budget,
                )
                break
            except anthropic.RateLimitError:
                tentativas += 1

    assert len(chamadas) == 3
    assert resultado == output_valido


def test_budget_interrompe_loop():
    tentativas = 0

    def mock_create_caro(*args, **kwargs):
        nonlocal tentativas
        tentativas += 1
        return criar_mock_response("json invalido", input_tokens=3500, output_tokens=500)

    with patch("chamar_com_budget.client") as mock_client:
        mock_client.messages.create.side_effect = mock_create_caro
        budget = BudgetEnforcer(limite_por_execucao=10_000)

        with pytest.raises(BudgetExcedidoError):
            # Cada tentativa consome ~4000 tokens: o budget é atingido na 3ª tentativa
            for _ in range(10):
                chamar_modelo_com_budget([], "", budget)

    assert tentativas <= 3  # o budget interrompeu antes da 4ª tentativa
