from typing import List


def multiplicarMatrizVector(matriz: List[List[float]], vector: List[float]) -> List[float]:
    return [sum(matriz[fila][j] * vector[j] for j in range(len(vector)))
            for fila in range(len(matriz))]

def multiplicarMatrices(matriz_a: List[List[float]], matriz_b: List[List[float]]) -> List[List[float]]:
    n = len(matriz_a)
    resultado = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            resultado[i][j] = sum(matriz_a[i][k] * matriz_b[k][j] for k in range(n))
    return resultado

def calcularVectorEstacionario(matriz: List[List[float]], tolerancia: float = 1e-10, iteracionesMax: int = 10_000) -> List[float]:
    n = len(matriz)
    vectorActual = [1.0 / n] * n
    for _ in range(iteracionesMax):
        vectorSiguiente = multiplicarMatrizVector(matriz, vectorActual)
        if sum(abs(vectorSiguiente[i] - vectorActual[i]) for i in range(n)) < tolerancia:
            break
        vectorActual = vectorSiguiente
    suma = sum(vectorActual)
    return [x / suma for x in vectorActual]

