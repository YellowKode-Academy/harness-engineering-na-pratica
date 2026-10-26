# exemplos/cap-11/tests/unit/test_com_fixtures.py
# Usa as fixtures de tests/conftest.py. Sem chamada real ao LLM, sem API key necessária.
import pytest

from revisar import revisar_diff


def test_bug_obvio_gera_problema(mock_anthropic_com_bug, diffs, budget_baixo):
    resultado = revisar_diff(diffs["bug_obvio"], client=mock_anthropic_com_bug)
    assert len(resultado["problemas"]) > 0
    assert resultado["problemas"][0]["severidade"] == "alta"


def test_budget_baixo_cancela_arquivo_grande(mock_anthropic_client, diffs, budget_baixo):
    from budget_enforcer import BudgetExcedidoError
    with pytest.raises(BudgetExcedidoError):
        revisar_diff(diffs["arquivo_grande"], client=mock_anthropic_client,
                     budget=budget_baixo)

# Output ao rodar: 2 passed
