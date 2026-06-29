# exemplos/cap-01/diagnostico_pontos_de_falha.py
import time

def diagnosticar_agente(agente_fn) -> dict:
    """
    Testa um agente contra os 5 pontos de falha comuns.
    agente_fn: função que recebe (diff: str) e retorna resposta
    Retorna: dicionário com resultado de cada teste
    """
    resultados = {}

    # Ponto 1: Contexto vago — o output tem estrutura definida?
    resposta_normal = agente_fn("def soma(a, b):\n    return a - b")
    resultados["output_estruturado"] = "sim" if isinstance(resposta_normal, dict) else "nao"

    # Ponto 2: Sem validação de input
    try:
        resposta = agente_fn("")
        resultados["valida_input_vazio"] = "nao" if resposta else "sim"
    except (ValueError, TypeError):
        resultados["valida_input_vazio"] = "sim"

    # Ponto 3: Sem retry — o que acontece com input grande?
    input_grande = "x = " + "1 + " * 10_000 + "0\n"
    try:
        agente_fn(input_grande)
        resultados["tem_limite_de_tamanho"] = "nao"
    except Exception as e:
        resultados["tem_limite_de_tamanho"] = "sim" if "tamanho" in str(e).lower() else "excecao_generica"

    return resultados

resultado = diagnosticar_agente(revisar_codigo)
# Output esperado para agent_fragil:
# {"output_estruturado": "nao", "valida_input_vazio": "nao", "tem_limite_de_tamanho": "nao"}
