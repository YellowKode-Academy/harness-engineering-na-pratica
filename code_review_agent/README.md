# code_review_agent

Este pacote é o agente de revisão de código construído ao longo do livro
**Harness Engineering na Prática com Python**.

O template completo de `HarnessAgent` — incluindo a orquestração das seis camadas
(Context, Tool, Guardrail, Observabilidade, Segurança e CI/CD) — está em:

```
exemplos/cap-14/harness_agent.py
```

Para criar um novo agente a partir do template, consulte o Capítulo 14 do livro
e use o cookiecutter disponível no repositório:

```bash
pip install cookiecutter
cookiecutter gh:YellowKode-Academy/harness-engineering-na-pratica --directory template
```
