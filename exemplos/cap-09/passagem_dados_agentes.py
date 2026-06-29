# exemplos/cap-09/passagem_dados_agentes.py
from dataclasses import dataclass

@dataclass
class RelatorioAnalise:
    problemas: list[dict]
    severidade_maxima: str
    linhas_afetadas: list[int]

def pipeline_review(pr_numero: int, diff: str) -> str:
    # Sub-agente 1: analisa com permissões de leitura apenas
    relatorio = agente_analise(diff, ctx=analisador_ctx)

    # Orquestrador decide o que fazer com o relatório
    if relatorio.severidade_maxima == "critica":
        return agente_reporter(relatorio, ctx=reporter_ctx)

    return "nenhum problema crítico encontrado"
# O agente_reporter só recebe o RelatorioAnalise, não acesso ao diff original
# O agente_analise nunca vê o ctx do reporter (que tem permissão de postar)
