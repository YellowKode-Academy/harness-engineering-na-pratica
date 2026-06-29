# .claude/hooks/audit_tool_call.py
import sys
import json
import datetime

evento = json.loads(sys.stdin.read())

registro = {
    "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    "ferramenta": evento.get("tool_name"),
    "input_resumo": str(evento.get("tool_input", ""))[:200],
    "output_resumo": str(evento.get("tool_response", ""))[:200],
}

with open(".claude/audit.jsonl", "a") as f:
    f.write(json.dumps(registro, ensure_ascii=False) + "\n")
