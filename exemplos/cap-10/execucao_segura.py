# exemplos/cap-10/execucao_segura.py
import uuid
import structlog
from budget_enforcer import BudgetEnforcer, BudgetExcedidoError
from rate_limiter import RateLimiter, RateLimitLocalError
from audit_log import AuditLog, EntradaAudit
from chamar_com_budget import chamar_modelo_com_budget

log = structlog.get_logger()

audit = AuditLog("audit.jsonl")
limiter = RateLimiter(max_chamadas=10, janela_segundos=60)

def _revisar_com_budget(diff: str, pr: int, budget: BudgetEnforcer, exec_log) -> dict:
    """Executa a revisão com controle de budget."""
    system = "Você é um revisor de código. Retorne JSON com o campo 'problemas'."
    mensagens = [{"role": "user", "content": diff}]
    output = chamar_modelo_com_budget(mensagens, system, budget)
    import json
    return json.loads(output)

def revisar_com_seguranca_completa(
    diff: str, pr: int, usuario: str
) -> dict:
    execution_id = str(uuid.uuid4())[:8]
    exec_log = log.bind(execution_id=execution_id, pr=pr, usuario=usuario)

    # 1. Rate limit: verificar frequência de chamadas
    try:
        limiter.verificar()
    except RateLimitLocalError as e:
        exec_log.warning("rate_limit_local", erro=str(e))
        raise

    # 2. Audit: registrar início
    audit.registrar(EntradaAudit("revisao_iniciada", execution_id, usuario, {"pr": pr}))

    # 3. Budget: criar por execução
    budget = BudgetEnforcer(limite_por_execucao=10_000)

    try:
        resultado = _revisar_com_budget(diff, pr, budget, exec_log)
        audit.registrar(EntradaAudit("revisao_concluida", execution_id, usuario,
            {"pr": pr, "problemas": len(resultado.get("problemas", []))}))
        return resultado

    except BudgetExcedidoError as e:
        exec_log.error("budget_excedido",
            consumido=e.consumido, limite=e.limite,
            percentual=round(e.consumido / e.limite, 2))
        audit.registrar(EntradaAudit("revisao_cancelada_budget", execution_id, usuario,
            {"pr": pr, "tokens_consumidos": e.consumido}))
        raise
