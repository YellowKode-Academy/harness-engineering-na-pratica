# exemplos/cap-07/configurar_structlog.py
import structlog
import logging

def configurar_logs_estruturados():
    # Processadores: o que acontece com cada evento antes de ser escrito
    processadores = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.JSONRenderer(),  # saída em JSON
    ]

    structlog.configure(
        processors=processadores,
        wrapper_class=structlog.BoundLogger,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )

    # Configurar o stdlib logging para capturar avisos de bibliotecas externas
    logging.basicConfig(format="%(message)s", level=logging.WARNING)

configurar_logs_estruturados()
log = structlog.get_logger()

# Uso básico:
log.info("execucao_iniciada", pr_numero=142, diff_tamanho=3800)
# Output: {"timestamp": "2026-06-27T22:43:00.123Z", "level": "info",
#           "event": "execucao_iniciada", "pr_numero": 142, "diff_tamanho": 3800}
