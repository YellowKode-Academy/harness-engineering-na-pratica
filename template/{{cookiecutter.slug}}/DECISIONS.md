# Decisões de harness: {{ cookiecutter.slug }}

Registre aqui o que alguém vai perguntar daqui a 6 meses: "por que isso foi feito assim?" (cap. 14).

## Valores iniciais (gerados pelo template)
- **Budget de produção: {{ cookiecutter.budget_tokens_por_exec }} tokens por execução.** Ponto de partida. Calibre com 20 execuções reais: p95 de tokens vezes 2.
- **Limite de {{ cookiecutter.max_chamadas_por_minuto }} chamadas por minuto em produção.** Divida o limite da sua conta da API pelo número de agentes rodando em paralelo.
- **Desenvolvimento e staging usam 50% e 80% desses valores,** para um erro em teste nunca gastar o orçamento cheio.
- **Até 3 novas tentativas em erro transitório da API,** com espera de 1 s, 2 s e 4 s. Erro que não é transitório sobe na hora.
- **Uma correção de formato:** se a resposta não passar no `OutputModel`, o modelo recebe o motivo e tenta mais uma vez.

## Decisões deste projeto
<!-- Ex.: "Budget 15.000 e não 10.000: diffs de refatoração chegam a 8.000 tokens de entrada e precisamos de margem para 2 retries." -->
