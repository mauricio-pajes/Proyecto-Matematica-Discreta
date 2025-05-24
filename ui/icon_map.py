from pathlib import Path

# =====================
# 📁 Directorios base
# =====================
BASE_DIR = Path(__file__).resolve().parent
ICON_DIR = BASE_DIR / "icons"
BG_DIR = BASE_DIR / "backgrounds"  # ← NUEVO para fondos de clima

# =====================
# 🔧 Helpers
# =====================
def _img(name: str) -> str:
    path = ICON_DIR / name
    if not path.exists():
        print(f"[ADVERTENCIA] Ícono no encontrado: {path}")
    return str(path)

def _bg(name: str) -> str:
    path = BG_DIR / name
    if not path.exists():
        print(f"[ADVERTENCIA] Fondo no encontrado: {path}")
    return str(path)

# =====================
# 🌤️ Íconos del clima
# =====================
ICON_MAP = {
    "NU": _img("nublado.png"),
    "PN": _img("parcialmente-nublado.png"),
    "PS": _img("parcialmente-soleado.png"),
    "SOL": _img("soleado.png"),
}

# =====================
# 🌄 Fondos del clima
# =====================
BACKGROUND_MAP = {
    "NU": _bg("bg_nublado.png"),
    "PN": _bg("bg_parcialmente-nublado.png"),
    "PS": _bg("bg_parcialmente-soleado.png"),
    "SOL": _bg("bg_soleado.png"),
}

# =====================
# 📝 Texto legible
# =====================
TEXT_MAP = {
    "SOL": "Soleado",
    "PS": "P. Soleado",
    "PN": "P. Nublado",
    "NU": "Nublado",
}

# =====================
# 🏫 Logo institucional
# =====================
UPC_LOGO = _img("UPC_logo_transparente.png")
