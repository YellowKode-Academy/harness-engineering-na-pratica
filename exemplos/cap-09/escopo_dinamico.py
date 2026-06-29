# exemplos/cap-09/escopo_dinamico.py
from dataclasses import dataclass, field
from sistema_permissoes import Permissao, ESCOPOS_POR_TIPO

@dataclass
class ContextoDeExecucao:
    tipo: str
    allowlist_extra: set = field(default_factory=set)
    blocklist: set = field(default_factory=set)

    def permissoes_efetivas(self) -> frozenset:
        base = ESCOPOS_POR_TIPO.get(self.tipo, frozenset())
        resultado = set(base)
        resultado.update(self.allowlist_extra)
        resultado -= self.blocklist
        return frozenset(resultado)

# Revisão normal com acesso temporário para fechar PR urgente
contexto_urgente = ContextoDeExecucao(
    tipo="revisao_codigo",
    allowlist_extra={Permissao.FECHAR_PR},
)
# permissoes_efetivas(): {LER_ARQUIVO, LER_PR_INFO, POSTAR_COMENTARIO, SOLICITAR_MUDANCAS, FECHAR_PR}

# Período de congelamento: bloquear merge mesmo para revisão que normalmente permitiria
contexto_freeze = ContextoDeExecucao(
    tipo="revisao_seguranca",
    blocklist={Permissao.FECHAR_PR},
)
# permissoes_efetivas(): {LER_ARQUIVO, LER_PR_INFO, POSTAR_COMENTARIO, SOLICITAR_MUDANCAS}
