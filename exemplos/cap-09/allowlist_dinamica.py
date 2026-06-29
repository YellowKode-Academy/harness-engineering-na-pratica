# exemplos/cap-09/allowlist_dinamica.py
import structlog
from dataclasses import dataclass, field
from sistema_permissoes import Permissao, ESCOPOS_POR_TIPO

log = structlog.get_logger()

@dataclass
class ContextoDeExecucao:
    tipo: str
    exec_id: str
    allowlist_extra: set = field(default_factory=set)
    blocklist: set = field(default_factory=set)
    motivo_allowlist: str = ""
    concedido_por: str = ""

    def adicionar_permissao_temporaria(
        self, permissao: "Permissao", motivo: str, concedido_por: str
    ):
        self.allowlist_extra.add(permissao)
        self.motivo_allowlist = motivo
        self.concedido_por = concedido_por
        log.warning("permissao_temporaria_concedida",
            exec_id=self.exec_id,
            permissao=permissao.value,
            motivo=motivo,
            concedido_por=concedido_por,
        )

    def permissoes_efetivas(self) -> frozenset:
        base = ESCOPOS_POR_TIPO.get(self.tipo, frozenset())
        resultado = set(base)
        resultado.update(self.allowlist_extra)
        resultado -= self.blocklist
        return frozenset(resultado)
