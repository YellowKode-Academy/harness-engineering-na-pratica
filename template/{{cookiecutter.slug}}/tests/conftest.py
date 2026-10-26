import os
from unittest.mock import MagicMock

import pytest

from {{ cookiecutter.__pacote }}.agent import criar_agente


def pytest_collection_modifyitems(config, items):
    """Sem ANTHROPIC_API_KEY, os testes de integração são pulados em vez de falhar."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        return
    pular = pytest.mark.skip(reason="defina ANTHROPIC_API_KEY para rodar os testes de integração")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(pular)


def criar_mock_response(texto: str, input_tokens: int = 150, output_tokens: int = 80):
    response = MagicMock()
    response.content = [MagicMock()]
    response.content[0].text = texto
    response.usage.input_tokens = input_tokens
    response.usage.output_tokens = output_tokens
    return response


@pytest.fixture
def cliente_mock():
    """Cliente Anthropic falso que devolve as respostas da lista, na ordem."""
    def fabricar(*respostas):
        client = MagicMock()
        client.messages.create.side_effect = [
            r if isinstance(r, Exception) else criar_mock_response(r) for r in respostas
        ]
        return client
    return fabricar


@pytest.fixture
def agente(tmp_path):
    """Agente de desenvolvimento com audit log numa pasta temporária e sem espera real entre retries."""
    def fabricar(client, **kwargs):
        ag = criar_agente("desenvolvimento", client=client, arquivo_audit=str(tmp_path / "audit.jsonl"), **kwargs)
        ag.dormir = lambda _s: None
        return ag
    return fabricar
