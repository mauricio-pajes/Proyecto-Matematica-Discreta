from typing import Optional
from Estado import Estado
from HistorialClima import HistorialClima
from MatrizTransicion import MatrizTransicion
from CadenaMarkov import CadenaMarkov
from ImpresoraConsola import ImpresoraConsola
from Calculos import multiplicarMatrizVector

class SimuladorClima:
    @staticmethod
    def _leerEntero(prompt: str, minimo: int, maximo: Optional[int] = None) -> int:
        while True:
            try:
                valor = int(input(prompt))
                if valor >= minimo and (maximo is None or valor <= maximo):
                    return valor
            except ValueError:
                pass
            print("Valor inválido.")

    def ejecutar(self):
        print("Simulador de clima con Cadenas de Márkov\n")
        dias = int(input("Ingrese N (20‑40): "))
        if not 20 <= dias <= 40:
            raise ValueError("N debe estar entre 20 y 40")

        SEMILLA_FIJA = 42  # ← valor hard‑codeado
        historial = HistorialClima(dias, SEMILLA_FIJA)
        matrizTransicion = MatrizTransicion(historial.secuencia).matriz
        cadena = CadenaMarkov(matrizTransicion)

        ImpresoraConsola.encabezado("Serie generada (DÍA 1 = hoy)")
        print(" ".join(reversed(historial.secuencia)))

        ImpresoraConsola.encabezado("Matriz de transición A")
        ImpresoraConsola.mostrarMatriz(matrizTransicion)

        pasosPronosticar = self._leerEntero("Pronosticar ¿cuántos días? (≥1): ", 1)
        vectorInicial = [0.0] * len(Estado.NOMBRES)
        vectorInicial[Estado.indice(historial.secuencia[-1])] = 1.0

        for paso in range(1, pasosPronosticar + 1):
            ImpresoraConsola.encabezado(f"Pronostico para el dia {paso}")
            matrizPotencia = cadena.potenciaMatriz(paso)
            vectorPaso = multiplicarMatrizVector(matrizPotencia, vectorInicial)
            ImpresoraConsola.mostrarMatriz(matrizPotencia)
            print("\nVector de probabilidades:")
            ImpresoraConsola.mostrarVector(vectorPaso)
            print(f"Estado más probable → {Estado.NOMBRES[vectorPaso.index(max(vectorPaso))]}\n")

        ImpresoraConsola.encabezado("Distribución estacionaria (largo plazo)")
        ImpresoraConsola.mostrarVector(cadena.vectorEstacionario())