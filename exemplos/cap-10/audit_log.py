# exemplos/cap-10/audit_log.py
import json
import datetime
from pathlib import Path
from dataclasses import dataclass

@dataclass
class EntradaAudit:
    evento: str
    execution_id: str
    usuario: str
    dados: dict

class AuditLog:
    def __init__(self, arquivo: str = "audit.jsonl"):
        self.arquivo = Path(arquivo)

    def registrar(self, entrada: EntradaAudit):
        registro = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "evento": entrada.evento,
            "execution_id": entrada.execution_id,
            "usuario": entrada.usuario,
            **entrada.dados,
        }
        with open(self.arquivo, "a", encoding="utf-8") as f:
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")
            f.flush()  # garante escrita imediata

audit = AuditLog("audit.jsonl")

def _executar_post_github(pr: int, linha: int, texto: str) -> bool:
    """Placeholder para a chamada real à API do GitHub."""
    return True

def postar_comentario_com_audit(pr: int, linha: int, texto: str,
                                 execution_id: str, usuario: str) -> bool:
    audit.registrar(EntradaAudit(
        evento="comentario_postado",
        execution_id=execution_id,
        usuario=usuario,
        dados={"pr": pr, "linha": linha, "texto_resumo": texto[:100]},
    ))
    return _executar_post_github(pr, linha, texto)

# Output em audit.jsonl (uma linha por registro):
# {"timestamp": "2026-06-27T22:43:11Z", "evento": "comentario_postado",
#  "execution_id": "a1b2c3d4", "usuario": "sistema", "pr": 142, ...}
