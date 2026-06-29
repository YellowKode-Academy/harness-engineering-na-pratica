# exemplos/cap-08/otel_tracing.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor

def configurar_tracing():
    provider = TracerProvider()
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)

tracer = trace.get_tracer("code-review-agent", "1.0.0")

def revisar_com_trace(diff: str, pr_numero: int) -> dict:
    with tracer.start_as_current_span("code_review") as span:
        span.set_attribute("pr.numero", pr_numero)
        span.set_attribute("diff.tamanho", len(diff))

        with tracer.start_as_current_span("chamar_modelo") as span_modelo:
            span_modelo.set_attribute("modelo", "claude-sonnet-4-6")
            resposta = chamar_api_com_retry(...)
            span_modelo.set_attribute("tokens.output", len(resposta) // 4)

        with tracer.start_as_current_span("validar_output"):
            resultado = validar_output_code_review(resposta)

        span.set_attribute("problemas.count", len(resultado.problemas))
        return resultado.model_dump()
