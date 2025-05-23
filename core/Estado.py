class Estado:
    NOMBRES = ["NU", "PN", "PS", "SOL"]

    @classmethod
    def indice(cls, nombre: str) -> int:
        return cls.NOMBRES.index(nombre)