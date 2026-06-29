# exemplos/cap-05/agent_com_guardrails.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import anthropic
from guardrail_aplicar import GuardrailError, validar_output_code_review

client = anthropic.Anthropic()

def revisar_e_validar(diff: str, pr_numero: int) -> dict:
    system_prompt = (
        "Você é um agente de revisão de código. "
        "Analise o diff fornecido e retorne um JSON com o campo 'problemas', "
        "uma lista de objetos com 'linha' (int), 'severidade' ('alta'|'media'|'baixa') e 'descricao' (str)."
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": diff}],
    )
    output_bruto = response.content[0].text

    try:
        resultado = validar_output_code_review(output_bruto)
        return resultado.model_dump()
    except GuardrailError as e:
        # Falha registrada mas não levantada: retorna estrutura de erro controlada
        return {
            "status": "guardrail_failure",
            "motivo": e.motivo,
            "output_bruto": e.output_bruto[:500],  # truncado para logging seguro
        }

# Output com JSON válido: {"problemas": [...]}
# Output com JSON inválido: {"status": "guardrail_failure", "motivo": "output não é JSON válido", ...}
