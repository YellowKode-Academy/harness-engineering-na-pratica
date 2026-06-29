# exemplos/cap-11/tests/test_golden.py
# Golden tests de regressão — verificam que o formato do output não mudou.
# Testes marcados como integration pois chamam o modelo real.
import json
import pytest
from pathlib import Path

from guardrail_aplicar import validar_output_code_review, GuardrailError

GOLDEN_DIR = Path(__file__).parent / "golden"


def _revisar_e_validar(diff: str, pr_numero: int) -> dict:
    """
    Chama o modelo real e valida o output com guardrails.
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
def test_golden_revisao_basica(request):
    diff = "+def processar(dados):\n+    return dados['resultado']"
    resultado = _revisar_e_validar(diff, pr_numero=0)

    golden_file = GOLDEN_DIR / "revisao_basica.json"
    if not golden_file.exists():
        GOLDEN_DIR.mkdir(exist_ok=True)
        golden_file.write_text(json.dumps(resultado, indent=2, ensure_ascii=False))
        pytest.skip("Golden criado. Rode novamente para validar")

    golden = json.loads(golden_file.read_text())
    assert "problemas" in resultado
    assert type(resultado["problemas"]) == type(golden["problemas"])
    # Não compara conteúdo exato: o modelo pode identificar coisas diferentes
