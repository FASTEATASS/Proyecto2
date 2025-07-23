from abc import ABC, abstractmethod

class Maleta(ABC):
    def __init__(self, peso: float):
        self.peso = peso

    @abstractmethod
    def calcularCosto(self) -> float:
        pass
