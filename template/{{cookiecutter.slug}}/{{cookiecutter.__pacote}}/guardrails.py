# {{ cookiecutter.__pacote }}/guardrails.py
# Guardrail Layer (cap. 5): nenhuma resposta do modelo vira resultado sem passar pelo OutputModel,
# e nenhuma ação sem volta acontece sem aprovação.
import json
import re

from pydantic import BaseModel, ValidationError, field_validator


class GuardrailError(Exception):
    def __init__(self, motivo: str, output_bruto: str):
        self.motivo = motivo
        self.output_bruto = output_bruto
        super().__init__(f"Guardrail falhou: {motivo}")


# IMPLEMENTE: troque pelo formato de saída do seu agente.
class Problema(BaseModel):
    descricao: str
    severidade: str

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


class OutputModel(BaseModel):
    problemas: list[Problema]


_CERCA = re.compile(r"^```(?:json)?\s*(.*?)\s*```$", re.DOTALL)


class GuardrailLayer:
    def __init__(self, modelo: type[BaseModel] = OutputModel):
        self.modelo = modelo

    def validar(self, output_bruto: str) -> dict:
        texto = output_bruto.strip()
        cerca = _CERCA.match(texto)  # modelos às vezes cercam o JSON com ```json
        if cerca:
            texto = cerca.group(1)
        try:
            dados = json.loads(texto)
        except json.JSONDecodeError as e:
            raise GuardrailError(f"output não é JSON válido: {e}", output_bruto) from e
        try:
            return self.modelo(**dados).model_dump()
        except (ValidationError, TypeError) as e:
            raise GuardrailError(f"schema inválido: {e}", output_bruto) from e


class AprovacaoNecessariaError(Exception):
    pass


# Ações que não têm volta. Ajuste para o seu agente.
ACOES_IRREVERSIVEIS = frozenset({"apagar", "enviar", "pagar", "publicar", "fazer_merge"})


def exigir_aprovacao(acao: str, aprovado_por: str | None = None) -> None:
    """Guardrail de ação: ação irreversível só passa com o nome de quem aprovou."""
    if acao in ACOES_IRREVERSIVEIS and not aprovado_por:
        raise AprovacaoNecessariaError(f"a ação '{acao}' não tem volta e precisa de aprovação humana")
