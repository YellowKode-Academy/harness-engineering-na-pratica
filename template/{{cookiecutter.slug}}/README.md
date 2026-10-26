# {{ cookiecutter.slug }}

{{ cookiecutter.descricao }}

Gerado com o template do livro *Harness Engineering na Prática com Python* (YellowKode Academy). Autor: {{ cookiecutter.autor }}.

## Começar

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
pytest tests/unit -v           # ou: make test
```

Os testes unitários passam sem chave de API: eles provam que o harness está conectado, não que o agente é inteligente.

Para rodar o agente de verdade:

```bash
export ANTHROPIC_API_KEY=sua_chave_aqui
echo "def dividir(a, b): return a / b" | python -m {{ cookiecutter.__pacote }}
```

## O que você implementa
1. `{{ cookiecutter.__pacote }}/context_manager.py`: `build_system_prompt()`, o contrato do agente.
2. `{{ cookiecutter.__pacote }}/tools.py`: schema, executor e permissão de cada ferramenta.
3. `{{ cookiecutter.__pacote }}/guardrails.py`: o `OutputModel` com as regras de negócio da resposta.
4. `{{ cookiecutter.__pacote }}/agent.py`: `_chamar_modelo_com_retry()`, se o seu agente usar tools ou outro `max_tokens`.

O resto já funciona: logs JSON com `execution_id`, budget, rate limit, audit log append-only, retry com espera crescente, correção de formato, CI e Docker.

## Ambientes
`AGENTE_AMBIENTE=desenvolvimento|staging|producao` (padrão: desenvolvimento). Valores em `{{ cookiecutter.__pacote }}/config.py`.

## Claude Code
`.claude/settings.json` traz permissões e dois hooks: `verificar_permissao.py` bloqueia comandos destrutivos e `audit_tool_call.py` registra cada ferramenta usada em `.claude/audit.jsonl`. Servidores MCP do projeto vão em `.mcp.json`, não no `settings.json`.

## Antes de produção
Rode o checklist de 42 itens do Apêndice A do livro e registre os itens pendentes em `DECISIONS.md`.
