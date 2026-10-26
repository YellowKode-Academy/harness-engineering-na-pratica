import json

import pytest

from {{ cookiecutter.__pacote }}.security import (
    AuditLog,
    BudgetEnforcer,
    BudgetExcedidoError,
    Permissao,
    PermissaoNegadaError,
    RateLimiter,
    RateLimitLocalError,
)
from {{ cookiecutter.__pacote }}.tools import executar_tool

OK = '{"problemas": []}'


def test_budget_interrompe_antes_de_estourar():
    budget = BudgetEnforcer(limite_por_execucao=1000)
    budget.registrar_consumo(600, 300)
    with pytest.raises(BudgetExcedidoError):
        budget.verificar_antes_de_chamar(200)


def test_entrada_maior_que_o_budget_nem_chama_o_modelo(cliente_mock, agente):
    client = cliente_mock(OK)
    ag = agente(client)
    ag.security.budget.limite_por_execucao = 1500
    with pytest.raises(BudgetExcedidoError):
        ag.executar({"texto": "x" * 8000})
    client.messages.create.assert_not_called()


def test_rate_limiter_bloqueia_a_chamada_alem_do_limite():
    limiter = RateLimiter(max_chamadas=3, janela_segundos=60)
    for _ in range(3):
        limiter.verificar()
    with pytest.raises(RateLimitLocalError):
        limiter.verificar()


def test_audit_log_so_acrescenta_linhas(tmp_path):
    audit = AuditLog(tmp_path / "audit.jsonl")
    audit.registrar("primeiro", "a1", {"x": 1})
    audit.registrar("segundo", "a2", {"x": 2})
    linhas = (tmp_path / "audit.jsonl").read_text(encoding="utf-8").splitlines()
    assert [json.loads(linha)["evento"] for linha in linhas] == ["primeiro", "segundo"]


def test_execucao_fica_registrada_no_audit(cliente_mock, agente, tmp_path):
    agente(cliente_mock(OK)).executar({"texto": "def f(): pass"})
    eventos = [json.loads(linha)["evento"] for linha in (tmp_path / "audit.jsonl").read_text(encoding="utf-8").splitlines()]
    assert eventos == ["execucao_concluida"]


def test_permissao_fora_do_escopo_e_negada(cliente_mock, agente):
    ag = agente(cliente_mock(OK))
    with pytest.raises(PermissaoNegadaError):
        ag.security.verificar_permissao(Permissao.PUBLICAR, ag.permissoes)


def test_tool_sem_permissao_responde_erro_claro():
    resultado = executar_tool("contar_palavras", {"texto": "a b"}, frozenset())
    assert not resultado.sucesso and "permissão" in resultado.erro


def test_tool_inexistente_responde_erro_claro():
    resultado = executar_tool("apagar_tudo", {}, frozenset({Permissao.LER}))
    assert not resultado.sucesso and "não existe" in resultado.erro


def test_tool_com_parametro_invalido_responde_erro_claro():
    resultado = executar_tool("contar_palavras", {"texto": ""}, frozenset({Permissao.LER}))
    assert not resultado.sucesso and "inválidos" in resultado.erro


def test_tool_valida_executa():
    resultado = executar_tool("contar_palavras", {"texto": "revisar o PR 42"}, frozenset({Permissao.LER}))
    assert resultado.sucesso and resultado.dados == 4
