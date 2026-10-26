# python -m {{ cookiecutter.__pacote }} < entrada.txt
import json
import sys

from .agent import criar_agente


def main() -> int:
    texto = sys.stdin.read()
    resultado = criar_agente().executar({"texto": texto})
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
