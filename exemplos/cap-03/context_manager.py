# exemplos/cap-03/context_manager.py
from dataclasses import dataclass, field

@dataclass
class ContextManager:
    role: str
    tools: list[str]
    output_format: str
    constraints: list[str]
    linguagem: str = "Python"

    def build_system_prompt(self) -> str:
        ferramentas = "\n".join(f"- {t}" for t in self.tools)
        restricoes = "\n".join(f"- {c}" for c in self.constraints)
        return (
            f"Papel: {self.role}\n\n"
            f"Capacidades disponíveis:\n{ferramentas}\n\n"
            f"Limitações:\n{restricoes}\n\n"
            f"Formato de saída obrigatório:\n{self.output_format}"
        )

    def build_task_message(self, diff: str, pr_numero: int) -> str:
        return f"Revise este diff do PR #{pr_numero}:\n\n```diff\n{diff}\n```"
