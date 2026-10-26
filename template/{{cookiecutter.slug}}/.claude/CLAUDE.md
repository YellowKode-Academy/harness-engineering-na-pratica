# {{ cookiecutter.slug }}

<!-- PARA MANTENEDORES: este arquivo é lido pelo Claude Code a cada sessão.
     Versione cada mudança com o motivo: "acrescenta restrição X por causa do incidente Y". -->

## O projeto
{{ cookiecutter.descricao }}

Agente em Python com as seis camadas de harness. Ponto de entrada: `{{ cookiecutter.__pacote }}/agent.py` (`HarnessAgent`).

## Onde mexer
- Contrato do agente: `{{ cookiecutter.__pacote }}/context_manager.py` (`build_system_prompt`)
- Ferramentas: `{{ cookiecutter.__pacote }}/tools.py` (schema, executor e permissão de cada tool)
- Formato da resposta: `{{ cookiecutter.__pacote }}/guardrails.py` (`OutputModel`)
- Orçamento e limites por ambiente: `{{ cookiecutter.__pacote }}/config.py`

## Regras
- Toda mudança em guardrail, budget ou permissão vem com teste em `tests/unit/`.
- Rode `pytest tests/unit` antes de dar o trabalho por terminado.
- Não remova uma camada do harness para "simplificar". Se uma camada atrapalha, registre o motivo em `DECISIONS.md`.
- Nunca leia nem escreva `.env` ou arquivos de credencial.
