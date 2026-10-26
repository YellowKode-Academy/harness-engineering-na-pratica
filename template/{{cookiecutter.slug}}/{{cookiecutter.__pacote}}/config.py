# {{ cookiecutter.__pacote }}/config.py
# Configuração por ambiente (Apêndice C). Produção usa os valores escolhidos ao gerar o projeto;
# desenvolvimento e staging ficam abaixo, para que um erro em teste nunca custe o orçamento cheio.
# Calibração: rode o agente 20 vezes com entradas reais e use o p95 de tokens multiplicado por 2.
import os

MODELO_PRINCIPAL = "{{ cookiecutter.modelo_principal }}"
BUDGET_PRODUCAO = {{ cookiecutter.budget_tokens_por_exec }}
CHAMADAS_POR_MINUTO_PRODUCAO = {{ cookiecutter.max_chamadas_por_minuto }}

CONFIG = {
    "desenvolvimento": {
        "budget_tokens": BUDGET_PRODUCAO // 2,
        "max_chamadas_por_minuto": max(1, CHAMADAS_POR_MINUTO_PRODUCAO // 2),
        "max_retries": 3,
        "postar_em_sistemas_reais": False,
    },
    "staging": {
        "budget_tokens": BUDGET_PRODUCAO * 8 // 10,
        "max_chamadas_por_minuto": max(1, CHAMADAS_POR_MINUTO_PRODUCAO * 8 // 10),
        "max_retries": 3,
        "postar_em_sistemas_reais": False,
    },
    "producao": {
        "budget_tokens": BUDGET_PRODUCAO,
        "max_chamadas_por_minuto": CHAMADAS_POR_MINUTO_PRODUCAO,
        "max_retries": 3,
        "postar_em_sistemas_reais": True,
    },
}

# Tokens reservados para a resposta do modelo em cada chamada.
MAX_TOKENS_RESPOSTA = 1024


def ambiente_atual() -> str:
    ambiente = os.environ.get("AGENTE_AMBIENTE", "desenvolvimento")
    if ambiente not in CONFIG:
        raise ValueError(f"AGENTE_AMBIENTE '{ambiente}' inválido. Use: {sorted(CONFIG)}")
    return ambiente


def carregar_config(ambiente: str | None = None) -> dict:
    return CONFIG[ambiente or ambiente_atual()]
