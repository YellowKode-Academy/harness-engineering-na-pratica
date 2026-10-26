# {{ cookiecutter.__pacote }}/security.py
# Segurança (cap. 9 e 10): permissões por tarefa, orçamento de tokens, limite de chamadas e audit log append-only.
import datetime
import json
import time
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class Permissao(Enum):
    LER = "ler"
    ESCREVER = "escrever"
    PUBLICAR = "publicar"


# Cada tipo de tarefa recebe só o que precisa. Nada de crachá mestre.
ESCOPOS_POR_TIPO = {
    "leitura": frozenset({Permissao.LER}),
    "edicao": frozenset({Permissao.LER, Permissao.ESCREVER}),
}


class PermissaoNegadaError(Exception):
    pass


class BudgetExcedidoError(Exception):
    def __init__(self, consumido: int, limite: int):
        self.consumido = consumido
        self.limite = limite
        super().__init__(f"Budget excedido: {consumido} tokens consumidos de {limite} permitidos")


@dataclass
class BudgetEnforcer:
    limite_por_execucao: int = {{ cookiecutter.budget_tokens_por_exec }}
    tokens_consumidos: int = 0

    def verificar_antes_de_chamar(self, tokens_estimados: int):
        projecao = self.tokens_consumidos + tokens_estimados
        if projecao > self.limite_por_execucao:
            raise BudgetExcedidoError(projecao, self.limite_por_execucao)

    def registrar_consumo(self, tokens_input: int, tokens_output: int):
        self.tokens_consumidos += tokens_input + tokens_output

    def percentual_consumido(self) -> float:
        return self.tokens_consumidos / self.limite_por_execucao


class RateLimitLocalError(Exception):
    def __init__(self, chamadas_na_janela: int, limite: int, janela_s: int):
        super().__init__(f"Rate limit local: {chamadas_na_janela} chamadas em {janela_s}s (limite: {limite})")


@dataclass
class RateLimiter:
    max_chamadas: int = {{ cookiecutter.max_chamadas_por_minuto }}
    janela_segundos: int = 60
    chamadas: deque = field(default_factory=deque)

    def verificar(self):
        agora = time.monotonic()
        while self.chamadas and agora - self.chamadas[0] > self.janela_segundos:
            self.chamadas.popleft()
        if len(self.chamadas) >= self.max_chamadas:
            raise RateLimitLocalError(len(self.chamadas), self.max_chamadas, self.janela_segundos)
        self.chamadas.append(agora)


class AuditLog:
    """Uma linha JSON por evento, sempre em modo append. Nunca reescrever o arquivo."""

    def __init__(self, arquivo: str | Path = "audit.jsonl"):
        self.arquivo = Path(arquivo)

    def registrar(self, evento: str, execution_id: str, dados: dict):
        registro = {
            "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
            "evento": evento,
            "execution_id": execution_id,
            **dados,
        }
        with open(self.arquivo, "a", encoding="utf-8") as f:
            f.write(json.dumps(registro, ensure_ascii=False, default=str) + "\n")
            f.flush()


def estimar_tokens(texto: str) -> int:
    """Estimativa conservadora: cerca de 4 caracteres por token."""
    return len(texto) // 4 + 1


@dataclass
class SecurityLayer:
    budget: BudgetEnforcer
    rate_limiter: RateLimiter
    audit: AuditLog
    reserva_resposta: int = 1024

    def verificar_rate_limit(self):
        self.rate_limiter.verificar()

    def verificar_budget_estimado(self, tarefa: dict):
        texto = json.dumps(tarefa, ensure_ascii=False, default=str)
        self.budget.verificar_antes_de_chamar(estimar_tokens(texto) + self.reserva_resposta)

    def registrar_consumo(self, tokens_input: int, tokens_output: int):
        self.budget.registrar_consumo(tokens_input, tokens_output)

    def verificar_permissao(self, exigida: Permissao, permissoes: frozenset):
        if exigida not in permissoes:
            raise PermissaoNegadaError(f"permissão '{exigida.value}' fora do escopo desta tarefa")

    def registrar_no_audit(self, evento: str, execution_id: str, dados: dict):
        self.audit.registrar(evento, execution_id, dados)
