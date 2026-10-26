from unittest.mock import MagicMock

import anthropic
import pytest

from {{ cookiecutter.__pacote }}.guardrails import GuardrailError

OK = '{"problemas": []}'


def _rate_limit():
    return anthropic.RateLimitError("rate limit", response=MagicMock(status_code=429), body={})


def test_tres_rate_limits_seguidos_e_sucesso_na_quarta(cliente_mock, agente):
    client = cliente_mock(_rate_limit(), _rate_limit(), _rate_limit(), OK)
    resultado = agente(client).executar({"texto": "def f(): pass"})
    assert resultado == {"problemas": []}
    assert client.messages.create.call_count == 4


def test_retry_desiste_depois_do_limite(cliente_mock, agente):
    client = cliente_mock(*[_rate_limit() for _ in range(4)])
    with pytest.raises(anthropic.RateLimitError):
        agente(client).executar({"texto": "def f(): pass"})


def test_espera_dobra_a_cada_tentativa(cliente_mock, agente):
    esperas = []
    ag = agente(cliente_mock(_rate_limit(), _rate_limit(), OK))
    ag.dormir = esperas.append
    ag.executar({"texto": "def f(): pass"})
    assert esperas == [1.0, 2.0]


def test_formato_errado_recebe_instrucao_de_correcao(cliente_mock, agente):
    client = cliente_mock("Aqui está:", OK)
    resultado = agente(client).executar({"texto": "def f(): pass"})
    assert resultado == {"problemas": []}
    segunda = client.messages.create.call_args_list[1].kwargs["messages"]
    assert "Formato incorreto" in segunda[-1]["content"]


def test_formato_errado_duas_vezes_falha_com_guardrail_error(cliente_mock, agente):
    with pytest.raises(GuardrailError):
        agente(cliente_mock("texto solto", "outro texto solto")).executar({"texto": "def f(): pass"})


def test_erro_que_nao_e_transitorio_nao_tem_retry(cliente_mock, agente):
    client = cliente_mock(ValueError("bug no código"), OK)
    with pytest.raises(ValueError):
        agente(client).executar({"texto": "def f(): pass"})
    assert client.messages.create.call_count == 1
