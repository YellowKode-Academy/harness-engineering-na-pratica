# exemplos/cap-10/rate_limiter.py
import time
from collections import deque
from dataclasses import dataclass, field

class RateLimitLocalError(Exception):
    def __init__(self, chamadas_na_janela: int, limite: int, janela_s: int):
        super().__init__(
            f"Rate limit local: {chamadas_na_janela} chamadas em {janela_s}s "
            f"(limite: {limite})"
        )

@dataclass
class RateLimiter:
    max_chamadas: int = 10
    janela_segundos: int = 60
    chamadas: deque = field(default_factory=deque)

    def verificar(self):
        agora = time.monotonic()
        # Remove chamadas fora da janela
        while self.chamadas and agora - self.chamadas[0] > self.janela_segundos:
            self.chamadas.popleft()

        if len(self.chamadas) >= self.max_chamadas:
            raise RateLimitLocalError(len(self.chamadas), self.max_chamadas, self.janela_segundos)

        self.chamadas.append(agora)

    def chamadas_na_janela(self) -> int:
        agora = time.monotonic()
        return sum(1 for t in self.chamadas if agora - t <= self.janela_segundos)

limiter = RateLimiter(max_chamadas=10, janela_segundos=60)
# Nas primeiras 10 chamadas em 60 segundos: OK
# Na 11ª: RateLimitLocalError
