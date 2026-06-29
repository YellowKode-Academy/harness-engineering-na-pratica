# exemplos/cap-03/context_manager_uso.py
# importado de context_manager.py
from context_manager import ContextManager

code_review_context = ContextManager(
    role="revisor automatizado de código Python do time de backend",
    tools=["ler_arquivo", "postar_comentario"],
    output_format='JSON: {"problemas": [{"linha": int, "severidade": "alta|media|baixa", "descricao": str}]}',
    constraints=[
        "analise apenas arquivos .py — ignore configuração e arquivos gerados",
        "não reescreva o código — apenas aponte o problema",
        "não aprove PRs com problemas de alta severidade",
        "se não houver problemas, retorne {\"problemas\": []}",
    ],
)

system_prompt = code_review_context.build_system_prompt()
# Resultado: string estruturada com papel, capacidades, limitações, formato
# Idêntica em cada chamada — sem variância dependente de como você escreveu
