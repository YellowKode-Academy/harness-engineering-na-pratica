# exemplos/cap-11/tests/unit/test_guardrails.py
# Testes unitários dos guardrails — sem chamada real ao LLM, sem API key necessária.
import pytest
from guardrail_layer import CodeReviewOutput
from guardrail_aplicar import validar_output_code_review, GuardrailError


class TestGuardrailsOutputValido:
    def test_aceita_lista_vazia(self):
        resultado = validar_output_code_review('{"problemas": []}')
        assert len(resultado.problemas) == 0

    def test_aceita_problema_valido(self):
        json_valido = '{"problemas": [{"linha": 42, "severidade": "alta", "descricao": "SQL injection"}]}'
        resultado = validar_output_code_review(json_valido)
        assert len(resultado.problemas) == 1
        assert resultado.problemas[0].linha == 42
        assert resultado.problemas[0].severidade == "alta"

    def test_normaliza_severidade_para_minusculo(self):
        json_maiusculo = '{"problemas": [{"linha": 1, "severidade": "Alta", "descricao": "bug"}]}'
        resultado = validar_output_code_review(json_maiusculo)
        assert resultado.problemas[0].severidade == "alta"


class TestGuardrailsOutputInvalido:
    def test_rejeita_texto_livre(self):
        with pytest.raises(GuardrailError) as exc_info:
            validar_output_code_review("Este código tem um bug na linha 42")
        assert "não é JSON válido" in exc_info.value.motivo

    def test_rejeita_severidade_invalida(self):
        json_invalido = '{"problemas": [{"linha": 1, "severidade": "CRÍTICA", "descricao": "bug"}]}'
        with pytest.raises(GuardrailError) as exc_info:
            validar_output_code_review(json_invalido)
        assert "schema inválido" in exc_info.value.motivo

    def test_rejeita_descricao_vazia(self):
        json_sem_desc = '{"problemas": [{"linha": 1, "severidade": "alta", "descricao": ""}]}'
        with pytest.raises(GuardrailError) as exc_info:
            validar_output_code_review(json_sem_desc)
        assert exc_info.value.motivo  # tem motivo
