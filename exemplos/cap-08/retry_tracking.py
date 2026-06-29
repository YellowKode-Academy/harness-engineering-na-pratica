# exemplos/cap-08/retry_tracking.py
import time
import random

def chamar_com_retry(func, max_retries: int = 3) -> tuple:
    retries = 0
    for tentativa in range(max_retries):
        try:
            resultado = func()
            return resultado, retries
        except Exception:
            retries += 1
            if tentativa < max_retries - 1:
                espera = (2 ** tentativa) + random.uniform(0, 1)
                time.sleep(espera)
    raise RuntimeError("max retries atingido")

# resultado, retries_usados = chamar_com_retry(chamar_api)
# Output: ({"problemas": [...]}, 0)  # sucesso na primeira tentativa
# Output: ({"problemas": [...]}, 2)  # precisou de 2 retries
