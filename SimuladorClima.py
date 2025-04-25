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
        dias = self._leerEntero("Ingrese N (20-40): ", 20, 40)

        SEMILLA_FIJA = 30
        historial = HistorialClima(dias, SEMILLA_FIJA)

        ImpresoraConsola.encabezado(f"Últimos {dias} días (hoy es el DÍA 1)")
        print("Secuencia:")
        print(" -> ".join(historial.secuencia))

        matrizTransicion = MatrizTransicion(historial.secuencia).matriz
        ImpresoraConsola.encabezado("Matriz de transición A")
        ImpresoraConsola.mostrarMatriz(matrizTransicion)

        pasosPronosticar = self._leerEntero("¿Cuántos días quieres pronosticar? (≥1): ", 1)
        vectorInicial = [0.0] * len(Estado.NOMBRES)
        vectorInicial[Estado.indice(historial.secuencia[-1])] = 1.0

        cm = CadenaMarkov(matrizTransicion)
        for paso in range(1, pasosPronosticar + 1):
            ImpresoraConsola.encabezado(f"Pronóstico para el día {paso}")

            print(f"Paso 1: calcular A^{paso}")
            matrizPotencia = cm.potenciaMatriz(paso)
            ImpresoraConsola.mostrarMatriz(matrizPotencia)

            print("\nPaso 2: multiplicar por vector inicial")
            print(f"Vector inicial = {vectorInicial}\n")
            vectorPaso = multiplicarMatrizVector(matrizPotencia, vectorInicial)

            ImpresoraConsola.encabezado("Vector de probabilidades")
            ImpresoraConsola.mostrarVector(vectorPaso)

            mejor_estado = Estado.NOMBRES[vectorPaso.index(max(vectorPaso))]
            prob = max(vectorPaso) * 100
            print(f"\nEstado más probable → {mejor_estado} con {prob:.1f}%\n")

        ImpresoraConsola.encabezado("Distribución estacionaria (largo plazo)")
        ImpresoraConsola.mostrarVector(cm.vectorEstacionario())