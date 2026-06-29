# exemplos/cap-12/verificar_secrets.py
import os
import sys

SECRETS_OBRIGATORIOS = {
    "ANTHROPIC_API_KEY": "Chave de API da Anthropic para produção",
    "GITHUB_TOKEN": "Token para postar comentários nos PRs",
}

def verificar_secrets() -> bool:
    """Verifica que todos os secrets necessários estão configurados."""
    ausentes = []
    for nome, descricao in SECRETS_OBRIGATORIOS.items():
        valor = os.getenv(nome, "")
        if not valor or valor == "None":
            ausentes.append(f"  {nome}: {descricao}")

    if ausentes:
        print("ERRO: Secrets não configurados:")
        for ausente in ausentes:
            print(ausente)
        return False

    print(f"OK: {len(SECRETS_OBRIGATORIOS)} secret(s) verificado(s)")
    return True

if __name__ == "__main__":
    sys.exit(0 if verificar_secrets() else 1)

# Output: OK: 2 secret(s) verificado(s)
