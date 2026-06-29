# exemplos/cap-05/guardrail_aplicar.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import json
from pydantic import ValidationError
from guardrail_layer import CodeReviewOutput

class GuardrailError(Exception):
    def __init__(self, motivo: str, output_bruto: str):
        self.motivo = motivo
        self.output_bruto = output_bruto
        super().__init__(f"Guardrail falhou: {motivo}")

def validar_output_code_review(output_bruto: str) -> CodeReviewOutput:
    # Passo 1: JSON parsing
    try:
        dados = json.loads(output_bruto)
    except json.JSONDecodeError as e:
        raise GuardrailError(f"output não é JSON válido: {e}", output_bruto) from e

    # Passo 2: Schema validation com Pydantic
    try:
        return CodeReviewOutput(**dados)
    except ValidationError as e:
        raise GuardrailError(f"schema inválido: {e}", output_bruto) from e

# Teste com severidade inválida:
# validar_output_code_review('{"problemas": [{"linha": 42, "severidade": "CRÍTICA", "descricao": "SQL injection"}]}')
# Lança: GuardrailError("Guardrail falhou: schema inválido: ...")
