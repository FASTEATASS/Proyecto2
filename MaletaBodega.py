from Maleta import Maleta
class MaletaBodega(Maleta):
    def calcularCosto(self) -> float:
        return self.peso * 1000
