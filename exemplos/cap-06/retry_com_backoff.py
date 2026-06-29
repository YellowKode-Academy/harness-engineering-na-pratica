# exemplos/cap-06/retry_com_backoff.py
import time
import functools
import anthropic

def com_retry(max_tentativas: int = 3, delay_inicial: float = 1.0, backoff: float = 2.0):
    """
    Decorator que adiciona retry com backoff exponencial.
    Faz retry apenas para erros transitórios da API.
    """
    def decorador(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = delay_inicial
            ultimo_erro = None

            for tentativa in range(max_tentativas):
                try:
                    return func(*args, **kwargs)
                except anthropic.RateLimitError as e:
                    ultimo_erro = e
                    if tentativa < max_tentativas - 1:
                        print(f"Rate limit — aguardando {delay}s (tentativa {tentativa+1}/{max_tentativas})")
                        time.sleep(delay)
                        delay *= backoff
                except anthropic.APIConnectionError as e:
                    ultimo_erro = e
                    if tentativa < max_tentativas - 1:
                        time.sleep(delay)
                        delay *= backoff
                except anthropic.InternalServerError as e:
                    ultimo_erro = e
                    if tentativa < max_tentativas - 1:
                        time.sleep(delay)
                        delay *= backoff

            raise ultimo_erro  # re-raise o último erro se todas as tentativas falharam

        return wrapper
    return decorador

client = anthropic.Anthropic()

@com_retry(max_tentativas=3, delay_inicial=1.0, backoff=2.0)
def chamar_api_com_retry(mensagens: list, system: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=system,
        messages=mensagens,
    )
    return response.content[0].text
# Tenta 3 vezes com delays de 1s, 2s, 4s antes de desistir
