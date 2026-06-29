# exemplos/cap-09/context_com_permissoes.py
from sistema_permissoes import ESCOPOS_POR_TIPO

def build_system_prompt_com_escopo(tipo_revisao: str) -> str:
    permissoes = ESCOPOS_POR_TIPO[tipo_revisao]
    ferramentas_disponiveis = [p.value for p in permissoes]

    return (
        f"Papel: revisor automatizado de código Python.\n\n"
        f"Ferramentas disponíveis neste contexto ({tipo_revisao}):\n"
        + "\n".join(f"- {f}" for f in ferramentas_disponiveis) +
        "\n\nRestrições importantes:\n"
        "- Use apenas as ferramentas listadas acima\n"
        "- Não tente acessar recursos fora do escopo desta revisão\n"
        "- Se precisar de uma ação que não está disponível, explique o que precisaria\n\n"
        "Formato de saída: JSON com campo 'problemas'"
    )
# Para revisao_estilo: lista ler_arquivo, ler_pr_info, postar_comentario
# Para revisao_seguranca: lista também solicitar_mudancas e fechar_pr
