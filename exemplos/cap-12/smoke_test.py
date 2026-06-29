# exemplos/cap-12/smoke_test.py
import sys
import time
import requests

def smoke_test(base_url: str, timeout_s: int = 30) -> bool:
    """
    Verifica que o agente está respondendo após deploy.
    Retorna True se saudável, False se falhou.
    """
    diff_teste = "+def soma(a: int, b: int) -> int:\n+    return a + b"
    endpoint = f"{base_url}/revisar"

    print(f"Smoke test em: {endpoint}")
    inicio = time.monotonic()

    try:
        response = requests.post(
            endpoint,
            json={"diff": diff_teste, "linguagem": "python", "pr_numero": 0},
            timeout=timeout_s,
        )

        duracao = round((time.monotonic() - inicio) * 1000)

        if response.status_code != 200:
            print(f"FALHOU: HTTP {response.status_code} em {duracao}ms")
            return False

        dados = response.json()
        if "problemas" not in dados:
            print(f"FALHOU: campo 'problemas' ausente. Response: {str(dados)[:200]}")
            return False

        print(f"OK: {len(dados['problemas'])} problema(s) encontrado(s) em {duracao}ms")
        return True

    except requests.Timeout:
        print(f"FALHOU: timeout após {timeout_s}s")
        return False
    except Exception as e:
        print(f"FALHOU: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    sys.exit(0 if smoke_test(url) else 1)
