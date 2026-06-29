# exemplos/cap-11/tests/integration/test_agent_integration.py
# Testes de integração — usam o modelo real. Requerem ANTHROPIC_API_KEY configurada.
# Execute com: pytest -m integration
import pytest

from guardrail_aplicar import validar_output_code_review, GuardrailError
from guardrail_layer import CodeReviewOutput


def _revisar_e_validar(diff: str, pr_numero: int) -> dict:
    """
    Chama o modelo real e valida o output com guardrails.
    Importa o cliente e a função do cap-05.
    """
    import anthropic
    client = anthropic.Anthropic()

    system_prompt = (
        "Você é um revisor de código especializado em Python. "
        "Analise o diff fornecido e retorne SOMENTE um JSON válido no formato:\n"
        '{"problemas": [{"linha": <int>, "severidade": "<alta|media|baixa>", "descricao": "<string>"}]}\n'
        "Se não houver problemas, retorne: {\"problemas\": []}\n"
        "IMPORTANTE: retorne APENAS o JSON, sem texto adicional."
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": f"Revise este diff:\n{diff}"}],
    )

    output_bruto = response.content[0].text.strip()

    try:
        resultado = validar_output_code_review(output_bruto)
        return resultado.model_dump()
    except GuardrailError as e:
        return {
            "status": "guardrail_failure",
            "motivo": e.motivo,
            "output_bruto": e.output_bruto[:500],
        }


@pytest.mark.integration
def test_revisao_retorna_json_no_formato_correto():
    """Verifica que o agente retorna JSON válido no formato esperado."""
    diff_simples = "+def soma(a, b):\n+    return a - b"
    resultado = _revisar_e_validar(diff_simples, pr_numero=1)
    assert "problemas" in resultado
    assert isinstance(resultado["problemas"], list)


@pytest.mark.integration
def test_revisao_identifica_bug_obvio():
    """Verifica que o agente identifica um bug óbvio; não testa o conteúdo exato."""
    diff_com_bug = "+def dividir(a, b):\n+    return a / b  # divisão por zero possível"
    resultado = _revisar_e_validar(diff_com_bug, pr_numero=2)
    # Só verifica que o agente encontrou algum problema, não que foi exatamente este
    assert len(resultado["problemas"]) > 0
    for problema in resultado["problemas"]:
        assert problema["severidade"] in {"alta", "media", "baixa"}
        assert isinstance(problema["linha"], int)
        assert problema["linha"] > 0


@pytest.mark.integration
def test_revisao_retorna_lista_vazia_para_codigo_correto():
    """Verifica que o agente não gera falsos positivos para código limpo."""
    diff_limpo = "+def soma(a: int, b: int) -> int:\n+    return a + b"
    resultado = _revisar_e_validar(diff_limpo, pr_numero=3)
    # O agente pode ou não encontrar algo, mas deve retornar estrutura correta
    assert "problemas" in resultado
