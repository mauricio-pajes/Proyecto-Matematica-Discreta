from typing import List
from Estado import Estado

class MatrizTransicion:
    def __init__(self, secuencia: List[str]):
        self.matriz: List[List[float]] = self.construirMatriz(secuencia)

    def construirMatriz(self, secuencia: List[str]) -> List[List[float]]:
        k = len(Estado.NOMBRES)
        conteos = [[0] * k for _ in range(k)]
        for hoy, manana in zip(secuencia[:-1], secuencia[1:]):
            col = Estado.indice(hoy)
            fila = Estado.indice(manana)
            conteos[fila][col] += 1

        matriz = [[0.0] * k for _ in range(k)]
        for col in range(k):
            suma = sum(conteos[fila][col] for fila in range(k))
            if suma == 0:
                for fila in range(k):
                    matriz[fila][col] = 1.0 / k
            else:
                for fila in range(k):
                    matriz[fila][col] = conteos[fila][col] / suma
        return matriz