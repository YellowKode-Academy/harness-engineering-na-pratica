# {{ cookiecutter.__pacote }}/agent.py
# O HarnessAgent do capítulo 14: as seis camadas conectadas num único ponto de entrada.
import time
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

import anthropic

from .config import MAX_TOKENS_RESPOSTA, MODELO_PRINCIPAL, carregar_config
from .context_manager import ContextManager
from .guardrails import GuardrailError, GuardrailLayer
from .observability import ObservabilityLayer
from .security import (
    ESCOPOS_POR_TIPO,
    AuditLog,
    BudgetEnforcer,
    RateLimiter,
    SecurityLayer,
)

# Erros transitórios da API: vale tentar de novo. Qualquer outro erro sobe na hora.
ERROS_TRANSITORIOS = (anthropic.RateLimitError, anthropic.APIConnectionError, anthropic.InternalServerError)


@dataclass
class HarnessAgent:
    context_manager: ContextManager
    guardrail_layer: GuardrailLayer
    observability: ObservabilityLayer
    security: SecurityLayer
    permissoes: frozenset
    client: Any = None
    modelo: str = MODELO_PRINCIPAL
    max_retries: int = 3
    delay_inicial: float = 1.0
    dormir: Callable[[float], None] = field(default=time.sleep, repr=False)

    def executar(self, tarefa: dict) -> dict:
        execution_id = str(uuid.uuid4())[:8]
        self.observability.iniciar(execution_id, tarefa)

        try:
            self.security.verificar_rate_limit()
            self.security.verificar_budget_estimado(tarefa)

            contexto = self.context_manager.montar(tarefa)
            with self.observability.span("chamada_modelo"):
                resultado = self._chamar_com_correcao_de_formato(contexto)

            self.observability.registrar_sucesso(execution_id, resultado)
            self.security.registrar_no_audit("execucao_concluida", execution_id, {"tamanho_entrada": len(str(tarefa))})
            return resultado

        except Exception as e:
            self.observability.registrar_erro(execution_id, e)
            self.security.registrar_no_audit("execucao_falhou", execution_id, {"erro": str(e)})
            raise

    def _chamar_com_correcao_de_formato(self, contexto: dict) -> dict:
        """Retry de formato (cap. 6): na segunda tentativa, o modelo recebe o motivo do erro."""
        mensagens = list(contexto["messages"])
        for tentativa in range(2):
            resposta_bruta = self._chamar_modelo_com_retry({**contexto, "messages": mensagens})
            try:
                return self.guardrail_layer.validar(resposta_bruta)
            except GuardrailError as e:
                if tentativa == 1:
                    raise
                self.observability.registrar_retry(tentativa + 1, f"formato: {e.motivo[:120]}")
                mensagens = mensagens + [
                    {"role": "assistant", "content": resposta_bruta},
                    {"role": "user", "content": f"Formato incorreto: {e.motivo}. Responda só com o JSON do formato de saída."},
                ]
        raise RuntimeError("inalcançável")

    def _chamar_modelo_com_retry(self, contexto: dict) -> str:
        # IMPLEMENTE (se precisar): modelo, tools e max_tokens específicos do seu agente.
        if self.client is None:
            self.client = anthropic.Anthropic()
        delay = self.delay_inicial
        for tentativa in range(self.max_retries + 1):
            try:
                self.security.budget.verificar_antes_de_chamar(MAX_TOKENS_RESPOSTA)
                resposta = self.client.messages.create(
                    model=self.modelo,
                    max_tokens=MAX_TOKENS_RESPOSTA,
                    system=contexto["system"],
                    messages=contexto["messages"],
                )
                self.security.registrar_consumo(resposta.usage.input_tokens, resposta.usage.output_tokens)
                self.observability.registrar_tokens(resposta.usage.input_tokens, resposta.usage.output_tokens)
                return resposta.content[0].text
            except ERROS_TRANSITORIOS as e:
                if tentativa == self.max_retries:
                    raise
                self.observability.registrar_retry(tentativa + 1, type(e).__name__)
                self.dormir(delay)
                delay *= 2
        raise RuntimeError("inalcançável")


def criar_agente(ambiente: str | None = None, tipo_tarefa: str = "leitura", client: Any = None,
                 arquivo_audit: str = "audit.jsonl") -> HarnessAgent:
    config = carregar_config(ambiente)
    return HarnessAgent(
        context_manager=ContextManager(),
        guardrail_layer=GuardrailLayer(),
        observability=ObservabilityLayer(),
        security=SecurityLayer(
            budget=BudgetEnforcer(limite_por_execucao=config["budget_tokens"]),
            rate_limiter=RateLimiter(max_chamadas=config["max_chamadas_por_minuto"]),
            audit=AuditLog(arquivo_audit),
            reserva_resposta=MAX_TOKENS_RESPOSTA,
        ),
        permissoes=ESCOPOS_POR_TIPO[tipo_tarefa],
        client=client,
        max_retries=config["max_retries"],
    )
