# exemplos/cap-05/guardrail_layer.py
import json
from pydantic import BaseModel, field_validator, ValidationError

class Problema(BaseModel):
    linha: int
    severidade: str
    descricao: str

    @field_validator("severidade")
    @classmethod
    def severidade_deve_ser_valida(cls, v: str) -> str:
        validos = {"alta", "media", "baixa"}
        if v.lower() not in validos:
            raise ValueError(f"severidade '{v}' inválida. Use: {validos}")
        return v.lower()

    @field_validator("descricao")
    @classmethod
    def descricao_nao_pode_ser_vazia(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("descrição não pode ser vazia")
        return v.strip()

class CodeReviewOutput(BaseModel):
    problemas: list[Problema]
