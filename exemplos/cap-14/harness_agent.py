# exemplos/cap-14/harness_agent.py
import sys
import os
import uuid
from dataclasses import dataclass

# Permite importar exemplos de outros capítulos do repo companion
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

@dataclass
class HarnessAgent:
    context_manager: "ContextManager"
    guardrail_layer: "GuardrailLayer"
    observability: "ObservabilityLayer"
    security: "SecurityLayer"
    permissoes: frozenset

    def executar(self, tarefa: dict) -> dict:
        execution_id = str(uuid.uuid4())[:8]
        log = self.observability.iniciar(execution_id, tarefa)

        try:
            self.security.verificar_rate_limit()
            self.security.verificar_budget_estimado(tarefa)

            contexto = self.context_manager.montar(tarefa)
            resposta_bruta = self._chamar_modelo_com_retry(contexto)
            resultado = self.guardrail_layer.validar(resposta_bruta)

            self.observability.registrar_sucesso(execution_id, resultado)
            self.security.registrar_no_audit("execucao_concluida", execution_id, tarefa)
            return resultado

        except Exception as e:
            self.observability.registrar_erro(execution_id, e)
            self.security.registrar_no_audit("execucao_falhou", execution_id, {"erro": str(e)})
            raise

    def _chamar_modelo_com_retry(self, contexto: dict) -> str:
        raise NotImplementedError("implementar _chamar_modelo_com_retry")
