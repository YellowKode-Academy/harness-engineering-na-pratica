# exemplos/cap-09/sistema_permissoes.py
from enum import Enum
from dataclasses import dataclass

class Permissao(Enum):
    LER_ARQUIVO = "ler_arquivo"
    LER_PR_INFO = "ler_pr_info"
    POSTAR_COMENTARIO = "postar_comentario"
    SOLICITAR_MUDANCAS = "solicitar_mudancas"
    APROVAR_PR = "aprovar_pr"
    FECHAR_PR = "fechar_pr"
    FAZER_MERGE = "fazer_merge"

# Cada tipo de tarefa tem um conjunto fixo de permissões
ESCOPOS_POR_TIPO = {
    "revisao_estilo": frozenset({
        Permissao.LER_ARQUIVO,
        Permissao.LER_PR_INFO,
        Permissao.POSTAR_COMENTARIO,
    }),
    "revisao_codigo": frozenset({
        Permissao.LER_ARQUIVO,
        Permissao.LER_PR_INFO,
        Permissao.POSTAR_COMENTARIO,
        Permissao.SOLICITAR_MUDANCAS,
    }),
    "revisao_seguranca": frozenset({
        Permissao.LER_ARQUIVO,
        Permissao.LER_PR_INFO,
        Permissao.POSTAR_COMENTARIO,
        Permissao.SOLICITAR_MUDANCAS,
        Permissao.FECHAR_PR,  # segurança pode fechar PR imediatamente
    }),
}
