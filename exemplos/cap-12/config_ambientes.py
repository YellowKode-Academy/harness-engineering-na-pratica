# exemplos/cap-12/config_ambientes.py
import os

AMBIENTE = os.getenv("AMBIENTE", "desenvolvimento")

CONFIGS = {
    "desenvolvimento": {
        "budget_tokens_por_exec": 5_000,
        "api_key_env": "ANTHROPIC_API_KEY",
        "postar_em_github_real": False,
        "log_level": "DEBUG",
        "rate_limit_chamadas": 5,
    },
    "staging": {
        "budget_tokens_por_exec": 8_000,
        "api_key_env": "ANTHROPIC_API_KEY_STAGING",
        "postar_em_github_real": False,   # só posta em repo de teste
        "log_level": "INFO",
        "rate_limit_chamadas": 8,
    },
    "producao": {
        "budget_tokens_por_exec": 15_000,
        "api_key_env": "ANTHROPIC_API_KEY",
        "postar_em_github_real": True,
        "log_level": "WARNING",
        "rate_limit_chamadas": 10,
    },
}

config = CONFIGS[AMBIENTE]
