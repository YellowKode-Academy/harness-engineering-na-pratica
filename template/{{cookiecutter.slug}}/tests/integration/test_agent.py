# Chama o modelo de verdade. Sem ANTHROPIC_API_KEY, o conftest pula estes testes.
import pytest

from {{ cookiecutter.__pacote }}.agent import criar_agente


@pytest.mark.integration
def test_agente_real_devolve_o_formato_do_output_model(tmp_path):
    agente = criar_agente("desenvolvimento", arquivo_audit=str(tmp_path / "audit.jsonl"))
    resultado = agente.executar({"texto": "def dividir(a, b):\n    return a / b"})
    assert isinstance(resultado["problemas"], list)
