from typing import List
from Estado import Estado

class ImpresoraConsola:
    @staticmethod
    def encabezado(titulo: str):
        print(f"\n{titulo}\n" + "=" * len(titulo))

    @staticmethod
    def mostrarMatriz(matriz: List[List[float]]):
        nombres = Estado.NOMBRES
        print("       " + " ".join(f"{nom:>6}" for nom in nombres))
        for i, fila in enumerate(matriz):
            print(f"{nombres[i]:>6} " + " ".join(f"{valor:6.3f}" for valor in fila))

    @staticmethod
    def mostrarVector(vector: List[float]):
        for nombre, prob in zip(Estado.NOMBRES, vector):
            print(f"  {nombre}: {prob * 100:5.1f}%")