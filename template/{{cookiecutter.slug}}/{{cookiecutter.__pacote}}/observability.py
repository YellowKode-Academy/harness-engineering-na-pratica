# {{ cookiecutter.__pacote }}/observability.py
# Observabilidade (cap. 7 e 8): logs JSON com execution_id, duração, tokens e taxa de sucesso.
# Dados sensíveis são mascarados antes de chegar ao log.
import logging
import re
import time
from contextlib import contextmanager

import structlog

try:  # OpenTelemetry é opcional: sem o SDK configurado, os spans não custam nada
    from opentelemetry import trace
    _tracer = trace.get_tracer("{{ cookiecutter.__pacote }}")
except ImportError:  # pragma: no cover
    _tracer = None

_SENSIVEIS = [
    (re.compile(r"sk-ant-[A-Za-z0-9_-]+"), "[TOKEN_MASCARADO]"),
    (re.compile(r"sk-[A-Za-z0-9_-]{16,}"), "[TOKEN_MASCARADO]"),
    (re.compile(r"gh[pousr]_[A-Za-z0-9]{16,}"), "[TOKEN_GITHUB_MASCARADO]"),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "[EMAIL_MASCARADO]"),
]


def mascarar(texto: str) -> str:
    for padrao, troca in _SENSIVEIS:
        texto = padrao.sub(troca, texto)
    return texto


def _mascarar_evento(_, __, evento: dict) -> dict:
    return {k: mascarar(v) if isinstance(v, str) else v for k, v in evento.items()}


def configurar_logs():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            _mascarar_evento,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.BoundLogger,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )
    logging.basicConfig(format="%(message)s", level=logging.WARNING)


class ObservabilityLayer:
    def __init__(self):
        configurar_logs()
        self.log = structlog.get_logger()
        self._inicio: dict[str, float] = {}
        self.sucessos = 0
        self.erros = 0
        self.tokens_input = 0
        self.tokens_output = 0

    def iniciar(self, execution_id: str, tarefa: dict):
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(execution_id=execution_id)
        self._inicio[execution_id] = time.monotonic()
        self.log.info("execucao_iniciada", tamanho_entrada=len(str(tarefa)))
        return self.log

    def _duracao_ms(self, execution_id: str) -> int:
        return int((time.monotonic() - self._inicio.pop(execution_id, time.monotonic())) * 1000)

    def registrar_tokens(self, tokens_input: int, tokens_output: int):
        self.tokens_input += tokens_input
        self.tokens_output += tokens_output
        self.log.info("tokens_consumidos", tokens_input=tokens_input, tokens_output=tokens_output)

    def registrar_tool_call(self, nome: str, parametros: dict, resultado: str):
        self.log.info("tool_chamada", tool=nome, parametros=str(parametros), resultado=resultado[:200])

    def registrar_retry(self, tentativa: int, motivo: str):
        self.log.warning("retry", tentativa=tentativa, motivo=motivo)

    def registrar_sucesso(self, execution_id: str, resultado: dict):
        self.sucessos += 1
        self.log.info("execucao_concluida", duracao_ms=self._duracao_ms(execution_id), itens=len(resultado.get("problemas", [])))

    def registrar_erro(self, execution_id: str, erro: Exception):
        self.erros += 1
        self.log.error("execucao_falhou", duracao_ms=self._duracao_ms(execution_id), tipo_erro=type(erro).__name__, erro=str(erro))

    def taxa_sucesso(self) -> float:
        total = self.sucessos + self.erros
        return self.sucessos / total if total else 0.0

    @contextmanager
    def span(self, nome: str):
        if _tracer is None:
            yield
            return
        with _tracer.start_as_current_span(nome):
            yield
