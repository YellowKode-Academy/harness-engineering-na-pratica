import pytest

from {{ cookiecutter.__pacote }}.guardrails import (
    AprovacaoNecessariaError,
    GuardrailError,
    GuardrailLayer,
    exigir_aprovacao,
)


def test_output_valido_passa():
    resultado = GuardrailLayer().validar('{"problemas": [{"descricao": "x", "severidade": "ALTA"}]}')
    assert resultado == {"problemas": [{"descricao": "x", "severidade": "alta"}]}


def test_json_cercado_por_crases_e_aceito():
    resultado = GuardrailLayer().validar('```json\n{"problemas": []}\n```')
    assert resultado == {"problemas": []}


def test_output_que_nao_e_json_tem_motivo_e_output_bruto():
    with pytest.raises(GuardrailError) as erro:
        GuardrailLayer().validar("Claro! Aqui está a revisão:")
    assert "JSON" in erro.value.motivo
    assert erro.value.output_bruto == "Claro! Aqui está a revisão:"


def test_severidade_invalida_e_rejeitada():
    with pytest.raises(GuardrailError) as erro:
        GuardrailLayer().validar('{"problemas": [{"descricao": "x", "severidade": "CRITICA"}]}')
    assert "schema" in erro.value.motivo


def test_campo_obrigatorio_ausente_e_rejeitado():
    with pytest.raises(GuardrailError):
        GuardrailLayer().validar('{"itens": []}')


def test_acao_irreversivel_sem_aprovacao_e_bloqueada():
    with pytest.raises(AprovacaoNecessariaError):
        exigir_aprovacao("apagar")


def test_acao_irreversivel_com_aprovacao_passa():
    exigir_aprovacao("apagar", aprovado_por="tech lead")


def test_acao_comum_nao_exige_aprovacao():
    exigir_aprovacao("ler")
