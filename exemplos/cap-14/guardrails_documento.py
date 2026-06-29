# exemplos/cap-14/guardrails_documento.py
from pydantic import BaseModel, field_validator

class ProblemaDoc(BaseModel):
    secao: str
    tipo: str
    descricao: str

    @field_validator("tipo")
    @classmethod
    def tipo_valido(cls, v: str) -> str:
        validos = {"clareza", "precisao", "completude"}
        if v not in validos:
            raise ValueError(f"tipo '{v}' inválido. Use: {validos}")
        return v

class DocumentReviewOutput(BaseModel):
    problemas: list[ProblemaDoc]
