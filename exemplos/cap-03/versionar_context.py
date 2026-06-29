# exemplos/cap-03/versionar_context.py
from pathlib import Path
import hashlib

PROMPTS_DIR = Path("prompts")

def carregar_system_prompt(nome: str) -> tuple[str, str]:
    """
    Carrega o system prompt do arquivo e retorna o texto + hash.
    O hash identifica a versão exata do prompt em uso nos logs.
    """
    caminho = PROMPTS_DIR / f"{nome}.txt"
    texto = caminho.read_text(encoding="utf-8")
    versao_hash = hashlib.sha256(texto.encode()).hexdigest()[:8]
    return texto, versao_hash

# Uso:
system_prompt, versao = carregar_system_prompt("code_review_agent")
# versao = "a3f8c21b"  — identificador do prompt nos logs

# Nos logs estruturados (capítulo 7):
# {"event": "agent_run", "prompt_version": versao, "pr_numero": 42, ...}
