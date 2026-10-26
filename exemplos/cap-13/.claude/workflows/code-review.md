# .claude/workflows/code-review.md

## Contexto
Este workflow revisa pull requests Python no repositório atual.

## Input esperado
- PR_NUMERO: número do pull request a revisar

## Processo
1. Use o GitHub MCP para obter a lista de arquivos modificados no PR $PR_NUMERO
2. Para cada arquivo .py na lista:
   - Use o filesystem MCP para ler o conteúdo
   - Analise em busca de: bugs de lógica, problemas de segurança, violações de convenção
   - Registre cada problema com: número da linha, severidade (alta/media/baixa), descrição
3. Se houver problemas de alta severidade:
   - Use o GitHub MCP para postar comentários nos pontos específicos
   - Solicite mudanças no PR
4. Se não houver problemas de alta severidade:
   - Poste um comentário resumindo o que foi revisado
   - Aprove o PR

## Formato de resposta final
Retorne JSON com todos os problemas encontrados:
{"problemas": [{"arquivo": str, "linha": int, "severidade": str, "descricao": str}]}
