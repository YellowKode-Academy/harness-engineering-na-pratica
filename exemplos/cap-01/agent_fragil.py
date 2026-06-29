# exemplos/cap-01/agent_fragil.py
import anthropic

client = anthropic.Anthropic()

def revisar_codigo(diff: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Revise este código e aponte problemas:\n\n{diff}"
            }
        ]
    )
    return response.content[0].text

# Output: texto livre com comentários do modelo
# Pode ser: parágrafo, lista, JSON, markdown, ou qualquer outra coisa
