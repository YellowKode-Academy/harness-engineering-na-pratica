# exemplos/cap-06/retry_de_formato.py
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from cap_05_guardrail_layer import validar_output_code_review, GuardrailError  # type: ignore
from cap_06_retry_com_backoff import chamar_api_com_retry, code_review_context  # type: ignore


def chamar_com_retry_de_formato(diff: str, max_tentativas: int = 2) -> dict:
    """
    Tenta obter output no formato correto.
    Na segunda tentativa, adiciona instrução de correção ao contexto.
    """
    system_prompt = code_review_context.build_system_prompt()
    mensagens = [{"role": "user", "content": f"Revise este diff:\n\n{diff}"}]

    for tentativa in range(max_tentativas):
        resposta_bruta = chamar_api_com_retry(mensagens, system_prompt)
        try:
            return validar_output_code_review(resposta_bruta).model_dump()
        except GuardrailError as e:
            if tentativa == max_tentativas - 1:
                raise  # sem mais tentativas — re-raise o erro
            # Adiciona contexto de correção para a próxima tentativa
            mensagens = mensagens + [
                {"role": "assistant", "content": resposta_bruta},
                {
                    "role": "user",
                    "content": (
                        f"Formato incorreto: {e.motivo}. "
                        "Retorne JSON válido com a estrutura: "
                        '{"problemas": [{"linha": int, "severidade": "alta|media|baixa", "descricao": str}]}. '
                        "Se não houver problemas, retorne: {\"problemas\": []}"
                    )
                },
            ]

    raise RuntimeError("nunca alcançado — raise acima garante isso")
