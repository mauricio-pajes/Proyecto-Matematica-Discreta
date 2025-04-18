from typing import List, Optional
import random
from Estado import Estado

class HistorialClima:
    def __init__(self, dias: int, semilla: Optional[int] = None):
        self.secuencia: List[str] = self.generarSecuencia(dias, semilla)

    def generarSecuencia(self, dias: int, semilla: Optional[int]) -> List[str]:
        if semilla is not None:
            random.seed(semilla)

        nombres = Estado.NOMBRES
        secuencia: List[str] = []

        for i in range(dias):
            if i == 0:
                clima = random.choice(nombres)
            else:
                climaAnterior = Estado.indice(secuencia[-1])
                pesos = [0.25] * 4
                pesos[climaAnterior] += 0.45
                clima = random.choices(nombres, weights=pesos)[0]
            secuencia.append(clima)

        return secuencia
