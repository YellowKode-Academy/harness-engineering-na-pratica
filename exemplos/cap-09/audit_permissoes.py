# exemplos/cap-09/audit_permissoes.py
import structlog
from sistema_permissoes import Permissao

log = structlog.get_logger()

def executar_com_auditoria(nome: str, params: dict, permissoes: frozenset, exec_id: str):
    perm_log = log.bind(execution_id=exec_id, ferramenta=nome)
    permissao = Permissao(nome)

    if permissao in permissoes:
        perm_log.info("acesso_autorizado")
        return executar_ferramenta(nome, params)
    else:
        perm_log.warning("acesso_negado",
            permissoes_ativas=[p.value for p in permissoes],
            permissao_necessaria=nome,
        )
        raise PermissionError(f"Acesso negado: {nome}")

# Se o agente tenta "fazer_merge" repetidamente e sempre recebe acesso negado,
# o padrão nos logs indica que o system prompt precisa de ajuste:
# o agente não está entendendo o escopo disponível
