#!/bin/bash
# exemplos/cap-12/rollback.sh

VERSAO_ATUAL=$(docker ps --filter "name=code-review-agent" --format "{{.Image}}")
VERSAO_ANTERIOR=$(docker images code-review-agent --format "{{.Tag}}" | \
    grep -v "latest" | head -n 2 | tail -n 1)

echo "Versão atual: $VERSAO_ATUAL"
echo "Versão anterior: code-review-agent:$VERSAO_ANTERIOR"

if [ -z "$VERSAO_ANTERIOR" ]; then
    echo "ERRO: Nenhuma versão anterior encontrada"
    exit 1
fi

echo "Fazendo rollback..."
docker stop code-review-agent-prod 2>/dev/null || true
docker run -d \
    --name code-review-agent-prod \
    --env-file .env.producao \
    "code-review-agent:$VERSAO_ANTERIOR"

# Verificar que o rollback funcionou
sleep 5
python scripts/smoke_test.py "$PRODUCAO_URL" && echo "Rollback OK" || echo "Rollback FALHOU"
