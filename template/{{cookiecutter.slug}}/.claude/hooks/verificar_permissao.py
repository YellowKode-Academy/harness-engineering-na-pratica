# .claude/hooks/verificar_permissao.py
# Hook PreToolUse (cap. 13): bloqueia comandos destrutivos antes de o agente executar.
# O livro mostra a saída em JSON com "decision". Para bloquear em qualquer versão do Claude Code,
# este hook sai com código 2: o comando não roda e o motivo (stderr) volta para o agente.
import json
import sys

sys.stderr.reconfigure(encoding="utf-8")

BLOQUEADOS = [
    "rm -rf",
    "git push --force",
    "git push -f",
    "DROP TABLE",
    "DELETE FROM",
    "git checkout main",
]

evento = json.loads(sys.stdin.read() or "{}")
tool_input = json.dumps(evento.get("tool_input", ""), ensure_ascii=False)

for comando in BLOQUEADOS:
    if comando.lower() in tool_input.lower():
        print(f"comando bloqueado por política de segurança: '{comando}'", file=sys.stderr)
        sys.exit(2)

sys.exit(0)
