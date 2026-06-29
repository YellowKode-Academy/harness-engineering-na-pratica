# exemplos/cap-05/retry_dirigido.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import anthropic
from guardrail_aplicar import GuardrailError, validar_output_code_review
from guardrail_layer import CodeReviewOutput

client = anthropic.Anthropic()

def construir_mensagem_de_correcao(guardrail_error: GuardrailError) -> str:
    """Constrói uma instrução específica baseada no motivo do erro."""
    motivo = guardrail_error.motivo

    if "não é JSON válido" in motivo:
        return (
            "Sua resposta anterior não era JSON válido. "
            "Retorne APENAS o JSON, sem texto antes ou depois, sem markdown. "
            f"Erro específico: {motivo}"
        )

    if "severidade" in motivo:
        return (
            "Sua resposta anterior usou um valor inválido para 'severidade'. "
            "Os únicos valores aceitos são: 'alta', 'media', 'baixa' (minúsculas, sem acento). "
            f"Output que falhou: {guardrail_error.output_bruto[:200]}"
        )

    return (
        f"Sua resposta anterior falhou na validação: {motivo}. "
        "Corrija e retorne o JSON com o schema correto."
    )

def revisar_com_retry(diff: str, system_prompt: str) -> CodeReviewOutput | dict:
    messages = [{"role": "user", "content": diff}]

    # Tentativa 1
    response = client.messages.create(
        model="claude-sonnet-4-6", max_tokens=1024,
        system=system_prompt, messages=messages
    )
    output_bruto = response.content[0].text

    try:
        return validar_output_code_review(output_bruto)
    except GuardrailError as e:
        # Tentativa 2 com instrução de correção direcionada
        mensagem_correcao = construir_mensagem_de_correcao(e)
        messages.extend([
            {"role": "assistant", "content": output_bruto},
            {"role": "user", "content": mensagem_correcao}
        ])

        response2 = client.messages.create(
            model="claude-sonnet-4-6", max_tokens=1024,
            system=system_prompt, messages=messages
        )
        output_bruto2 = response2.content[0].text

        try:
            return validar_output_code_review(output_bruto2)
        except GuardrailError as e2:
            return {"status": "guardrail_failure_dupla", "motivo": e2.motivo}

# Output tentativa 1 com JSON inválido: retorna CodeReviewOutput validado na tentativa 2
# Output falha dupla: {"status": "guardrail_failure_dupla", "motivo": "..."}
