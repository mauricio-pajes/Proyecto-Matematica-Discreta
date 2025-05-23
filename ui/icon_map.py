from pathlib import Path

ICON_DIR = Path(__file__).resolve().parent / "icons"

def _img(name: str) -> str:
    path = ICON_DIR / name
    if not path.exists():
        print(f"[ADVERTENCIA] Imagen no encontrada: {path}")
    return str(path)

ICON_MAP = {
    "NU": _img("nublado.png"),
    "PN": _img("parcialmente-nublado.png"),
    "PS": _img("parcialmente-soleado.png"),
    "SOL": _img("soleado.png"),
}

TEXT_MAP = {
    "SOL": "Soleado",
    "PS": "P. Soleado",
    "PN": "P. Nublado",
    "NU": "Nublado",
}

UPC_LOGO = _img("UPC_logo_transparente.png")
