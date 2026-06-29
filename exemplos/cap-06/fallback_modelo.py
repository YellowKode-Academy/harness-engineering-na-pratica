# exemplos/cap-06/fallback_modelo.py
import anthropic

client = anthropic.Anthropic()

MODELOS_POR_PRIORIDADE = ["claude-sonnet-4-6", "claude-haiku-4-5-20251001"]

def _revisar_com_modelo(diff: str, modelo: str) -> dict:
    """Chama a API com um modelo específico e retorna o resultado."""
    response = client.messages.create(
        model=modelo,
        max_tokens=1024,
        messages=[{"role": "user", "content": f"Revise este diff:\n\n{diff}"}],
    )
    return {"resultado": response.content[0].text, "modelo_usado": modelo}

def revisar_com_fallback_de_modelo(diff: str) -> dict:
    ultimo_erro = None
    for modelo in MODELOS_POR_PRIORIDADE:
        try:
            return _revisar_com_modelo(diff, modelo)
        except Exception as e:
            print(f"Modelo {modelo} falhou: {type(e).__name__}. Tentando próximo.")
            ultimo_erro = e

    raise RuntimeError(f"Todos os modelos falharam. Último erro: {ultimo_erro}")
