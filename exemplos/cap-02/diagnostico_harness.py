# exemplos/cap-02/diagnostico_harness.py
def diagnosticar_harness(config: dict) -> dict:
    """
    config: dict com booleans descrevendo o estado atual do agente
    Retorna: camadas ausentes com prioridade de implementação
    """
    camadas = {
        "Context": config.get("tem_system_prompt_estruturado", False),
        "Tools": config.get("tem_schemas_completos", False),
        "Guardrails": config.get("valida_output_antes_de_aceitar", False),
        "Observabilidade": config.get("tem_logs_estruturados", False),
        "Segurança": config.get("tem_limites_de_permissao_e_budget", False),
        "CI/CD": config.get("tem_testes_automatizados", False),
    }

    ausentes = [nome for nome, presente in camadas.items() if not presente]
    implementadas = [nome for nome, presente in camadas.items() if presente]

    return {
        "implementadas": implementadas,
        "ausentes": ausentes,
        "prioridade_imediata": ausentes[:2] if ausentes else [],
        "cobertura": f"{len(implementadas)}/6 camadas",
    }
