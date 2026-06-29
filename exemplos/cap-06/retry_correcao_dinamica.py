# exemplos/cap-06/retry_correcao_dinamica.py
from pydantic import ValidationError
import json

def construir_mensagem_correcao(resposta_bruta: str, erro: Exception) -> str:
    """
    Constrói uma mensagem de correção específica baseada no erro.
    Inclui o valor inválido, o campo afetado e os valores aceitos.
    """
    if isinstance(erro, ValidationError):
        detalhes = []
        for falha in erro.errors():
            campo = ".".join(str(p) for p in falha["loc"])
            valor_invalido = falha.get("input", "desconhecido")
            msg_erro = falha["msg"]
            detalhes.append(f"Campo '{campo}': {msg_erro}. Valor recebido: '{valor_invalido}'")

        instrucao = "No output anterior, encontrei erros de validação:\n"
        instrucao += "\n".join(f"- {d}" for d in detalhes)
        instrucao += "\n\nCorrija apenas esses campos e retorne o JSON completo novamente."
        return instrucao

    # Fallback para erros de formato genéricos
    try:
        json.loads(resposta_bruta)
        return "O JSON é válido mas não segue o schema esperado. Revise os campos obrigatórios."
    except json.JSONDecodeError as json_err:
        return f"O output não é JSON válido: {json_err}. Retorne apenas JSON, sem texto adicional."

# Exemplo de uso:
# erro = ValidationError(...)
# mensagem = construir_mensagem_correcao(resposta_bruta, erro)
# Output: "No output anterior, encontrei erros de validação:
#          - Campo 'problemas[0].severidade': value is not a valid enum member.
#            Valor recebido: 'CRÍTICA'
#          Corrija apenas esses campos e retorne o JSON completo novamente."
