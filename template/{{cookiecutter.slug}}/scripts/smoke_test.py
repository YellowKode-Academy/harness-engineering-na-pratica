# scripts/smoke_test.py
# Teste de fumaça: monta o agente com todas as camadas e faz uma execução de ponta a ponta,
# com um cliente falso, sem rede e sem chave. Se uma camada não estiver conectada, falha aqui.
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def main() -> int:
    from {{ cookiecutter.__pacote }}.agent import criar_agente

    resposta = MagicMock()
    resposta.content = [MagicMock(text='{"problemas": []}')]
    resposta.usage.input_tokens, resposta.usage.output_tokens = 100, 20
    client = MagicMock()
    client.messages.create.return_value = resposta

    with tempfile.TemporaryDirectory() as pasta:
        audit = Path(pasta) / "audit.jsonl"
        agente = criar_agente("producao", client=client, arquivo_audit=str(audit))
        resultado = agente.executar({"texto": "smoke test"})
        assert resultado == {"problemas": []}, resultado
        assert audit.read_text(encoding="utf-8").count("\n") == 1, "audit log não registrou a execução"
        assert agente.security.budget.tokens_consumidos == 120, "consumo de tokens não foi registrado"
    print("smoke test ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
