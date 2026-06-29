# exemplos/cap-06/fallback_escopo.py
import anthropic

client = anthropic.Anthropic()

def _revisar_diff_completo(diff: str, pr_numero: int) -> dict:
    """Chama a API para revisar o diff completo."""
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": f"Revise o diff do PR #{pr_numero}:\n\n{diff}",
            }
        ],
    )
    return {"problemas": [], "resultado": response.content[0].text}

def revisar_com_fallback_de_escopo(diff: str, pr_numero: int) -> dict:
    try:
        return _revisar_diff_completo(diff, pr_numero)
    except Exception:
        # Fallback: dividir em partes de 5000 chars e revisar cada parte
        partes = [diff[i:i+5000] for i in range(0, min(len(diff), 25000), 5000)]
        todos_problemas = []
        for i, parte in enumerate(partes):
            try:
                resultado = _revisar_diff_completo(parte, pr_numero)
                todos_problemas.extend(resultado.get("problemas", []))
            except Exception:
                pass  # ignora falha de parte individual — revisão parcial é melhor que nada
        return {
            "problemas": todos_problemas,
            "aviso": f"revisão parcial — diff muito grande ({len(diff)} chars)",
        }
