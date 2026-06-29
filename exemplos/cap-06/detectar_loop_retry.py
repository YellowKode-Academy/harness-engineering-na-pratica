# exemplos/cap-06/detectar_loop_retry.py
from collections import Counter

def retry_com_deteccao_de_loop(
    func, max_tentativas: int = 3, max_erros_distintos: int = 2
):
    """
    Retry que para mais cedo se detectar que os erros estão variando.
    Erros variados indicam problema ambiental, não transitório.
    """
    erros_vistos = []

    for tentativa in range(max_tentativas):
        try:
            return func()
        except Exception as e:
            tipo_erro = type(e).__name__
            erros_vistos.append(tipo_erro)

            contagem = Counter(erros_vistos)
            erros_distintos = len(contagem)

            # Para se temos muitos tipos de erro diferentes
            if erros_distintos >= max_erros_distintos and tentativa < max_tentativas - 1:
                raise RuntimeError(
                    f"Abortando após {tentativa+1} tentativas: "
                    f"{erros_distintos} tipos de erro distintos sugere problema estrutural. "
                    f"Erros: {dict(contagem)}"
                ) from e

            if tentativa == max_tentativas - 1:
                raise

    raise RuntimeError("nunca alcançado")

# Output se detectar loop:
# RuntimeError: "Abortando após 2 tentativas: 2 tipos de erro distintos sugere
#                problema estrutural. Erros: {'RateLimitError': 1, 'InternalServerError': 1}"
