from typing import List
from .Calculos import (
    multiplicarMatrizVector,
    multiplicarMatrices,
    calcularVectorEstacionario,
)
class CadenaMarkov:
    def __init__(self, matrizTransicion: List[List[float]]):
        self.matrizTransicion = matrizTransicion

    def potenciaMatriz(self, exponente: int) -> List[List[float]]:
        n = len(self.matrizTransicion)
        resultado = [[float(i == j) for j in range(n)] for i in range(n)]
        for _ in range(exponente):
            resultado = multiplicarMatrices(self.matrizTransicion, resultado)
        return resultado

    def vectorProbabilidadEnPaso(self, vectorInicial: List[float], paso: int) -> List[float]:
        return multiplicarMatrizVector(self.potenciaMatriz(paso), vectorInicial)

    def vectorEstacionario(self) -> List[float]:
        return calcularVectorEstacionario(self.matrizTransicion)