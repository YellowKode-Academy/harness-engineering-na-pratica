# exemplos/cap-02/diagnostico_agente_fragil.py
estado_agente_fragil = {
    "tem_system_prompt_estruturado": False,
    "tem_schemas_completos": False,
    "valida_output_antes_de_aceitar": False,
    "tem_logs_estruturados": False,
    "tem_limites_de_permissao_e_budget": False,
    "tem_testes_automatizados": False,
}
resultado = diagnosticar_harness(estado_agente_fragil)
# Output: {"implementadas": [], "ausentes": ["Context", "Tools", "Guardrails",
#           "Observabilidade", "Segurança", "CI/CD"],
#           "prioridade_imediata": ["Context", "Tools"], "cobertura": "0/6 camadas"}
