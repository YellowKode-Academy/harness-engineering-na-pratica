# exemplos/cap-04/tool_validation.py
from pydantic import BaseModel, field_validator
import os

class LerArquivoParams(BaseModel):
    caminho: str
    linhas: list[int] | None = None

    @field_validator("caminho")
    @classmethod
    def caminho_deve_ser_relativo(cls, v: str) -> str:
        if os.path.isabs(v):
            raise ValueError(f"caminho deve ser relativo ao repositório, não absoluto: {v}")
        if ".." in v.split("/"):
            raise ValueError(f"caminho não pode navegar para fora do repositório: {v}")
        return v

class PostarComentarioParams(BaseModel):
    pr_numero: int
    linha: int
    severidade: str
    descricao: str

    @field_validator("linha")
    @classmethod
    def linha_deve_ser_positiva(cls, v: int) -> int:
        if v <= 0:
            raise ValueError(f"linha deve ser positiva, recebido: {v}")
        return v

    @field_validator("descricao")
    @classmethod
    def descricao_nao_pode_ser_muito_longa(cls, v: str) -> str:
        if len(v) > 200:
            raise ValueError(f"descrição de {len(v)} chars excede limite de 200")
        return v
