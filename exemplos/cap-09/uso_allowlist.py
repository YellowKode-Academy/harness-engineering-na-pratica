# exemplos/cap-09/uso_allowlist.py
from allowlist_dinamica import ContextoDeExecucao
from sistema_permissoes import Permissao

# Contexto normal de revisão de código
ctx = ContextoDeExecucao(tipo="revisao_codigo", exec_id="exec-2847")

# Permissão adicional concedida para este incidente específico
ctx.adicionar_permissao_temporaria(
    Permissao.FECHAR_PR,
    motivo="incidente SEC-2024-089: PR contém credencial exposta",
    concedido_por="joao.silva@empresa.com",
)

# O agente agora pode fechar o PR, mas o log registra quem autorizou e por quê
print(ctx.permissoes_efetivas())
# Output: frozenset({Permissao.LER_ARQUIVO, Permissao.LER_PR_INFO,
#          Permissao.POSTAR_COMENTARIO, Permissao.SOLICITAR_MUDANCAS,
#          Permissao.FECHAR_PR})
