from typing import List, Optional
import random
from .Estado import Estado

class HistorialClima:
    def __init__(self, dias: int, semilla: Optional[int] = None):
        self.secuencia: List[str] = self.generarSecuencia(dias, semilla)

    def generarSecuencia(self, dias: int, semilla: Optional[int]) -> List[str]:
        rng = random.Random(semilla)
        nombres = Estado.NOMBRES
        secuencia: List[str] = []

        for _ in range(dias):
            if not secuencia:
                clima = rng.choice(nombres)
            else:
                idx_ant = Estado.indice(secuencia[-1])
                pesos = [1.0] * len(nombres)
                pesos[idx_ant] += 1.8
                clima = rng.choices(nombres, weights=pesos, k=1)[0]
            secuencia.append(clima)

        return secuencia