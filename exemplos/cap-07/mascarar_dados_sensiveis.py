# exemplos/cap-07/mascarar_dados_sensiveis.py
import re
import hashlib

def mascarar_para_log(texto: str, max_chars: int = 200) -> str:
    """
    Prepara texto para logging: mascara dados sensíveis e limita tamanho.
    Nunca logue texto sensível diretamente.
    """
    # Remove tokens de API (padrão Anthropic: sk-ant-...)
    texto = re.sub(r"sk-ant-[a-zA-Z0-9\-_]+", "[TOKEN_MASCARADO]", texto)

    # Remove tokens GitHub (ghp_... ou github_pat_...)
    texto = re.sub(r"gh[ps]_[a-zA-Z0-9]+", "[TOKEN_GITHUB_MASCARADO]", texto)

    # Remove padrões de CPF
    texto = re.sub(r"\d{3}\.\d{3}\.\d{3}-\d{2}", "[CPF_MASCARADO]", texto)

    # Remove emails (opcional, depende do contexto)
    # texto = re.sub(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", "[EMAIL]", texto)

    # Limita tamanho
    if len(texto) > max_chars:
        texto = texto[:max_chars] + f"... [truncado: {len(texto)} chars total]"

    return texto

def hash_para_referencia(conteudo: str) -> str:
    """Gera hash curto para referenciar conteúdo sem logá-lo."""
    return hashlib.sha256(conteudo.encode()).hexdigest()[:8]

# Uso correto:
# log.info("diff_recebido",
#     diff_hash=hash_para_referencia(diff),  # referência sem expor conteúdo
#     diff_tamanho=len(diff),
#     pr_numero=pr_numero,
# )
#
# Uso incorreto (nunca fazer):
# log.info("diff_recebido", diff=diff)  # expõe conteúdo completo
# log.info("api_key", key=api_key)      # expõe credencial


if __name__ == "__main__":
    # Testes sem necessidade de API key
    casos = [
        ("Token Anthropic", "chave=sk-ant-api03-AbCdEfGh1234567890 no config", "[TOKEN_MASCARADO]"),
        ("Token GitHub ghp", "auth: ghp_AbCd1234EfGh5678IjKl", "[TOKEN_GITHUB_MASCARADO]"),
        ("Token GitHub ghs", "session: ghs_XyZ9876abcDEF", "[TOKEN_GITHUB_MASCARADO]"),
        ("CPF", "cpf do usuario: 123.456.789-09 no cadastro", "[CPF_MASCARADO]"),
        ("Texto limpo", "revisão do PR #42 concluída com 3 problemas", None),
    ]

    print("=== Testes mascarar_para_log ===\n")
    for nome, entrada, esperado in casos:
        resultado = mascarar_para_log(entrada, max_chars=500)
        ok = (esperado is None and entrada == resultado) or (esperado and esperado in resultado)
        status = "OK" if ok else "FALHOU"
        print(f"[{status}] {nome}")
        print(f"  entrada:   {entrada}")
        print(f"  resultado: {resultado}\n")

    print("=== Teste hash_para_referencia ===\n")
    diff = "def foo(): return 42"
    h = hash_para_referencia(diff)
    print(f"hash de '{diff}': {h} (len={len(h)})")
    assert len(h) == 8, "hash deve ter 8 chars"
    assert hash_para_referencia(diff) == h, "hash deve ser determinístico"
    print("OK — hash determinístico e tamanho correto\n")

    print("=== Teste truncamento ===\n")
    longo = "x" * 300
    truncado = mascarar_para_log(longo, max_chars=200)
    assert "[truncado:" in truncado
    print(f"OK — texto de 300 chars truncado para {len(truncado)} chars (com sufixo)\n")
