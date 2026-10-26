# Capítulo 13: Claude Code como plataforma de harness

Os arquivos do capítulo, prontos para copiar para a raiz do seu projeto:

| Arquivo | O que é |
|---|---|
| `.claude/CLAUDE.md` | O contrato do Code Review Agent |
| `.claude/CLAUDE-v2.1.md` | A versão comentada para mantenedores |
| `.claude/settings.json` | Permissões e hooks combinados |
| `.claude/settings.hooks.json` | Só os hooks (PreToolUse e PostToolUse) |
| `.claude/settings.permissoes.json` | Só o sistema de permissões |
| `.claude/hooks/verificar_permissao.py` | Bloqueia comandos destrutivos |
| `.claude/hooks/audit_tool_call.py` | Registra cada ferramenta usada em `.claude/audit.jsonl` |
| `.claude/workflows/code-review.md` | O workflow de revisão de PR |
| `.mcp.json` | Os servidores MCP (GitHub e filesystem) |

Duas diferenças em relação ao texto impresso, para funcionar na versão atual do Claude Code:

1. **Servidores MCP ficam em `.mcp.json`**, na raiz do projeto, e não dentro do `.claude/settings.json`. Por isso o `settings.json` combinado daqui não traz o bloco `mcpServers`.
2. **O hook de bloqueio sai com código 2** em vez de imprimir `{"decision": "block"}`. Código 2 bloqueia a ferramenta em qualquer versão, e a mensagem de stderr volta para o agente explicando o motivo.

O mesmo `.claude/` já vem pronto em todo projeto gerado pelo template (`template/`, capítulo 14).
