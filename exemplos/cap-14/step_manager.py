# exemplos/cap-14/step_manager.py
class StepManager:
    def __init__(self, max_steps: int = 10):
        self.max_steps = max_steps
        self.steps_executados = 0

    def proximo_step(self) -> bool:
        if self.steps_executados >= self.max_steps:
            raise RuntimeError(f"Limite de {self.max_steps} steps atingido")
        self.steps_executados += 1
        return True

# Uso: if step_manager.proximo_step(): continuar o loop
