# exemplos/cap-08/custo_execucao.py
# Preços claude-sonnet-4-6 (USD por 1M tokens, jun/2026)
PRECO_INPUT_POR_TOKEN = 3.00 / 1_000_000
PRECO_OUTPUT_POR_TOKEN = 15.00 / 1_000_000
CAMBIO_USD_BRL = 5.20

def calcular_custo(tokens_input: int, tokens_output: int) -> dict:
    custo_usd = (
        tokens_input * PRECO_INPUT_POR_TOKEN
        + tokens_output * PRECO_OUTPUT_POR_TOKEN
    )
    return {
        "custo_usd": round(custo_usd, 6),
        "custo_brl": round(custo_usd * CAMBIO_USD_BRL, 5),
    }

# calcular_custo(tokens_input=4200, tokens_output=380)
# Output: {"custo_usd": 0.018360, "custo_brl": 0.09547}
