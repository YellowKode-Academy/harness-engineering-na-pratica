# Harness Engineering na Prática com Python

Repositório companion do livro **Harness Engineering na Prática com Python** — Livro 6 da série *IA na Prática*, de Kelvin Baumhardt Biffi (YellowKode Academy).

## O que é Harness Engineering?

> **Agente = Modelo + Harness**

O modelo você conhece. O harness é o sistema ao redor: contexto, tools, guardrails, observabilidade, segurança e CI/CD. Sem harness projetado, até o melhor modelo entrega resultados inconsistentes em produção.

Este repositório contém todos os exemplos de código do livro, organizados por capítulo, e o Code Review Agent completo — o projeto fio condutor construído ao longo dos 14 capítulos.

## Estrutura

```
exemplos/
├── cap-01/    Context: o agente frágil e os 5 pontos de falha
├── cap-02/    Harness: diagnóstico das 6 camadas
├── cap-03/    Context Layer: system prompts como contratos, input validation
├── cap-04/    Tool Layer: schemas Pydantic, ToolResult, executores
├── cap-05/    Guardrails: output validation, GuardrailError tipado
├── cap-06/    Retry Layer: backoff, detecção de loop, fallback
├── cap-07/    Observabilidade: structlog, ContextVar, mascaramento
├── cap-08/    Métricas: tokens, latência, custo, OpenTelemetry, alertas
├── cap-09/    Segurança: permissões, escopos, audit, pipeline multi-agente
├── cap-10/    Budget, Rate Limiter, Audit Log JSONL
├── cap-11/    Testes: unit, integration, adversarial, golden
├── cap-12/    CI/CD: GitHub Actions, smoke test, deploy
├── cap-13/    Claude Code: CLAUDE.md, settings.json, hooks e .mcp.json
├── cap-14/    HarnessAgent: template com as 6 camadas integradas
└── _shared/   Stubs e utilities compartilhados entre capítulos
code_review_agent/  Ponto de partida do Code Review Agent (gere o projeto completo com o template)
template/           Cookiecutter do cap. 14 e do Apêndice C: projeto novo com as 6 camadas prontas
```

## Instalação

```bash
git clone https://github.com/YellowKode-Academy/harness-engineering-na-pratica.git
cd harness-engineering-na-pratica
pip install -r requirements.txt
```

Variáveis de ambiente necessárias para exemplos com API:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export GITHUB_TOKEN="ghp_..."     # opcional, para exemplos de GitHub
```

## Template para um agente novo (cap. 14 e Apêndice C)

```bash
pip install cookiecutter
cookiecutter gh:YellowKode-Academy/harness-engineering-na-pratica --directory template
cd <slug>
pip install -r requirements.txt
pytest tests/unit -v
```

O projeto gerado já passa nos testes unitários, no lint e no teste de fumaça em Docker. Você implementa o `build_system_prompt`, as tools, o `OutputModel` e, se precisar, o `_chamar_modelo_com_retry`.

## Testes

### Sem API key (roda localmente):

```bash
pytest
```

Sem `ANTHROPIC_API_KEY`, os testes de integração são pulados (aparecem como `s`), não reprovados.

### Com API key (testes de integração):

```bash
pytest exemplos/cap-11/tests/integration/ -v -m integration
```

## Exemplos por capítulo

### Cap-03 — Context Layer

```python
from exemplos.cap_03.input_validation import CodeReviewInput
from pydantic import ValidationError

try:
    inp = CodeReviewInput(diff="", pr_numero=1, linguagem="python", repositorio="org/repo")
except ValidationError as e:
    print(e)  # diff não pode ser vazio
```

### Cap-05 — Guardrails

```python
from exemplos.cap_05.guardrail_aplicar import validar_output_code_review, GuardrailError

try:
    resultado = validar_output_code_review('{"problemas": []}')
    print(f"OK: {len(resultado.problemas)} problemas")
except GuardrailError as e:
    print(f"Output inválido: {e}")
```

### Cap-10 — Budget Enforcer

```python
from exemplos.cap_10.budget_enforcer import BudgetEnforcer, BudgetExcedidoError

budget = BudgetEnforcer(limite_por_execucao=10_000)
budget.verificar_antes_de_chamar(3_000)
budget.registrar_consumo(tokens_input=2_500, tokens_output=500)
print(f"Consumido: {budget.percentual_consumido():.0%}")
```

## Licença

MIT. Código livre para uso em projetos pessoais e comerciais.
