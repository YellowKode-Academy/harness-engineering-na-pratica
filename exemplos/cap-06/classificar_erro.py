# exemplos/cap-06/classificar_erro.py
import anthropic
from enum import Enum

class TipoErro(Enum):
    TRANSITORIO = "transitorio"
    ESTRUTURAL = "estrutural"

def classificar_erro(erro: Exception) -> TipoErro:
    """
    Classifica um erro como transitório ou estrutural.
    Transitório: retry pode resolver.
    Estrutural: retry não vai ajudar, precisa de intervenção.
    """
    # Rate limit: transitório, mas precisa de backoff
    if isinstance(erro, anthropic.RateLimitError):
        return TipoErro.TRANSITORIO

    # Servidor indisponível: transitório
    if isinstance(erro, anthropic.InternalServerError):
        return TipoErro.TRANSITORIO

    # Falha de conexão: transitório
    if isinstance(erro, anthropic.APIConnectionError):
        return TipoErro.TRANSITORIO

    # Erro de autenticação: estrutural (chave inválida não muda)
    if isinstance(erro, anthropic.AuthenticationError):
        return TipoErro.ESTRUTURAL

    # Contexto muito longo: estrutural (tokens não diminuem com retry)
    if isinstance(erro, anthropic.BadRequestError):
        if "prompt is too long" in str(erro).lower():
            return TipoErro.ESTRUTURAL

    # Permissão negada: estrutural
    if isinstance(erro, anthropic.PermissionDeniedError):
        return TipoErro.ESTRUTURAL

    # Padrão conservador: tratar como estrutural se não reconhecido
    return TipoErro.ESTRUTURAL

# Uso no loop de retry:
# tipo = classificar_erro(e)
# if tipo == TipoErro.ESTRUTURAL:
#     raise  # não adianta tentar de novo
