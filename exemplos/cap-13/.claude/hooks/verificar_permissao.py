# .claude/hooks/verificar_permissao.py
import sys
import json

evento = json.loads(sys.stdin.read())
tool_name = evento.get("tool_name", "")
tool_input = str(evento.get("tool_input", ""))

# Comandos que nunca devem ser executados pelo agente automaticamente
BLOQUEADOS = [
    "rm -rf",
    "git push --force",
    "DROP TABLE",
    "DELETE FROM",
    "git checkout main",  # não deve mudar de branch
]

for cmd_bloqueado in BLOQUEADOS:
    if cmd_bloqueado in tool_input:
        print(json.dumps({
            "decision": "block",
            "reason": f"comando bloqueado por política de segurança: '{cmd_bloqueado}'"
        }))
        sys.exit(0)

print(json.dumps({"decision": "allow"}))
# Output (quando bloqueado): {"decision": "block", "reason": "comando bloqueado: 'rm -rf'"}
# Output (quando permitido): {"decision": "allow"}
