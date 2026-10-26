# .claude/hooks/audit_tool_call.py
# Hook PostToolUse (cap. 13): uma linha por chamada de ferramenta em .claude/audit.jsonl, só acrescentando.
import datetime
import json
import sys
from pathlib import Path

evento = json.loads(sys.stdin.read() or "{}")

registro = {
    "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
    "ferramenta": evento.get("tool_name"),
    "input_resumo": str(evento.get("tool_input", ""))[:200],
    "output_resumo": str(evento.get("tool_response", ""))[:200],
}

arquivo = Path(".claude/audit.jsonl")
with open(arquivo, "a", encoding="utf-8") as f:
    f.write(json.dumps(registro, ensure_ascii=False) + "\n")
