# exemplos/cap-09/verificar_permissao.py
import structlog
from sistema_permissoes import Permissao, ESCOPOS_POR_TIPO

log = structlog.get_logger()

def verificar_e_executar_ferramenta(
    nome: str, parametros: dict, permissoes: frozenset
) -> str:
    permissao_necessaria = Permissao(nome)

    if permissao_necessaria not in permissoes:
        log.warning("permissao_negada",
            ferramenta=nome,
            permissoes_ativas=[p.value for p in permissoes],
        )
        raise PermissionError(
            f"ferramenta '{nome}' não permitida neste contexto. "
            f"Permissões ativas: {[p.value for p in permissoes]}"
        )

    log.info("ferramenta_autorizada", ferramenta=nome)
    return executar_ferramenta(nome, parametros)

# Teste: verificar_e_executar_ferramenta("fazer_merge", {}, ESCOPOS_POR_TIPO["revisao_codigo"])
# Lança: PermissionError("ferramenta 'fazer_merge' não permitida neste contexto...")
