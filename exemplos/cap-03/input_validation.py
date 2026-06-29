# exemplos/cap-03/input_validation.py
from pydantic import BaseModel, field_validator

class CodeReviewInput(BaseModel):
    diff: str
    linguagem: str = "python"
    pr_numero: int

    @field_validator("diff")
    @classmethod
    def diff_nao_pode_ser_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("diff não pode ser vazio")
        return v

    @field_validator("diff")
    @classmethod
    def diff_nao_pode_ser_muito_grande(cls, v: str) -> str:
        limite = 50_000
        if len(v) > limite:
            raise ValueError(f"diff de {len(v)} chars excede limite de {limite}")
        return v

    @field_validator("linguagem")
    @classmethod
    def linguagem_suportada(cls, v: str) -> str:
        suportadas = {"python", "javascript", "typescript", "go"}
        if v.lower() not in suportadas:
            raise ValueError(f"linguagem '{v}' não suportada. Use: {suportadas}")
        return v.lower()

# Teste: CodeReviewInput(diff="", linguagem="python", pr_numero=42)
# Lança: ValidationError: 1 validation error for CodeReviewInput
#   diff: diff não pode ser vazio (type=value_error)
