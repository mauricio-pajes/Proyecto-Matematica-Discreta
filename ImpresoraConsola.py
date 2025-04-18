from typing import List
from Estado import Estado

class ImpresoraConsola:
    @staticmethod
    def encabezado(titulo: str):
        print(f"\n{titulo}\n" + "=" * len(titulo))

    @staticmethod
    def mostrarMatriz(matriz: List[List[float]]):
        for fila in matriz:
            print(" ".join(f"{valor:6.3f}" for valor in fila))

    @staticmethod
    def mostrarVector(vector: List[float]):
        for nombre, prob in zip(Estado.NOMBRES, vector):
            print(f"  {nombre}: {prob * 100:5.1f}%")