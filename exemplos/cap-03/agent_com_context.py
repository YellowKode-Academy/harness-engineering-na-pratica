# exemplos/cap-03/agent_com_context.py
import anthropic
# importado de context_manager.py
from context_manager import ContextManager, code_review_context
# importado de input_validation.py
from input_validation import CodeReviewInput

client = anthropic.Anthropic()

def revisar_codigo(diff: str, linguagem: str, pr_numero: int) -> str:
    # validação: vai lançar ValidationError se input inválido
    entrada = CodeReviewInput(diff=diff, linguagem=linguagem, pr_numero=pr_numero)

    system_prompt = code_review_context.build_system_prompt()
    mensagens = [{"role": "user", "content": code_review_context.build_task_message(entrada.diff, entrada.pr_numero)}]

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=system_prompt,
        messages=mensagens,
    )
    return response.content[0].text

# O que mudou:
# 1. Inputs inválidos são rejeitados com erro claro antes de chegar ao modelo
# 2. O sistema prompt é um contrato estruturado, não texto livre
# 3. O formato de output está especificado — violações são detectáveis
