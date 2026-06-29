# exemplos/cap-04/tool_result.py
from dataclasses import dataclass
from typing import Any
from tool_validation import LerArquivoParams

@dataclass
class ToolResult:
    sucesso: bool
    dados: Any
    erro: str | None = None

    def para_texto(self) -> str:
        if self.sucesso:
            if isinstance(self.dados, str):
                return f"OK:\n{self.dados}"
            return f"OK: {self.dados}"
        return f"ERRO: {self.erro}"

def ler_arquivo(caminho: str, linhas: list[int] | None = None) -> ToolResult:
    params = LerArquivoParams(caminho=caminho, linhas=linhas)
    try:
        with open(params.caminho, "r", encoding="utf-8") as f:
            conteudo = f.readlines()
        if params.linhas:
            selecionadas = [conteudo[l - 1] for l in params.linhas if 1 <= l <= len(conteudo)]
            return ToolResult(sucesso=True, dados="".join(selecionadas))
        return ToolResult(sucesso=True, dados="".join(conteudo))
    except FileNotFoundError:
        return ToolResult(sucesso=False, dados=None, erro=f"arquivo não encontrado: {params.caminho}")
    except PermissionError:
        return ToolResult(sucesso=False, dados=None, erro=f"sem permissão de leitura: {params.caminho}")

# Output para arquivo existente:
# ToolResult(sucesso=True, dados="def soma(a, b):\n    return a + b\n", erro=None)
# Output para arquivo inexistente:
# ToolResult(sucesso=False, dados=None, erro="arquivo não encontrado: src/soma.py")
