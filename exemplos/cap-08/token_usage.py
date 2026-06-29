# exemplos/cap-08/token_usage.py
import anthropic

cliente = anthropic.Anthropic()

def revisar_com_token_tracking(diff: str) -> tuple[dict, dict]:
    resposta = cliente.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": diff}],
    )
    uso = {
        "tokens_input": resposta.usage.input_tokens,
        "tokens_output": resposta.usage.output_tokens,
        "tokens_total": resposta.usage.input_tokens + resposta.usage.output_tokens,
    }
    return resposta.content[0].text, uso

# _, uso = revisar_com_token_tracking(diff_grande)
# Output: {"tokens_input": 4200, "tokens_output": 380, "tokens_total": 4580}
