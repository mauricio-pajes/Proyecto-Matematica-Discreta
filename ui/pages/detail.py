# ui/pages/detail.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QHeaderView, QSpacerItem,
    QSizePolicy, QStackedLayout
)
from PyQt6.QtGui import QFont, QColor, QPixmap
from PyQt6.QtCore import Qt

from core.Estado import Estado
from ..icon_map import BACKGROUND_MAP, TEXT_MAP


# ---------------------------------------------------------------------------
# WIDGET FACTORY
# ---------------------------------------------------------------------------
def build(mw):
    contenedor = QWidget()
    contenedor.setContentsMargins(0, 0, 0, 0)

    # StackedLayout correctamente configurado
    stacked = QStackedLayout(contenedor)
    stacked.setStackingMode(QStackedLayout.StackingMode.StackAll)
    stacked.setContentsMargins(0, 0, 0, 0)

    # Fondo (imagen en QLabel)
    fondo = QLabel()
    fondo.setPixmap(QPixmap(BACKGROUND_MAP["NU"]))
    fondo.setScaledContents(True)
    fondo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    # Overlay con transparencia (importante establecer explícitamente el tamaño y layout)
    overlay = QWidget()
    overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
    overlay.setStyleSheet("background-color: rgba(255, 255, 255, 0.25);")
    overlay_layout = QVBoxLayout(overlay)
    overlay_layout.setContentsMargins(16, 16, 16, 16)
    overlay_layout.setSpacing(12)

    # Widgets agregados al stacked layout
    stacked.addWidget(fondo)      # Debajo
    stacked.addWidget(overlay)    # Encima (contenido visible)

    # **Forzar tamaño**
    stacked.setCurrentWidget(overlay)  # Para asegurar que overlay sea considerado para tamaño

    # Guardar referencias
    mw.bg_label = fondo
    mw.detail_layout = overlay_layout

    return contenedor


# ---------------------------------------------------------------------------
# DETALLE DE UN DÍA n
# ---------------------------------------------------------------------------
def populate_detalle(mw, day: int, matriz, vector):
    lay = mw.detail_layout
    _clear(lay)

    # Estado predominante
    idx_max = vector.index(max(vector))
    estado_max = Estado.NOMBRES[idx_max]
    mw.bg_label.setPixmap(QPixmap(BACKGROUND_MAP.get(estado_max, BACKGROUND_MAP["NU"])))

    # Título + subtítulo
    header = QLabel(f"Matriz A^{day} y vector de probabilidades")
    header.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
    header.setStyleSheet("color: #222222;")
    lay.addWidget(header, alignment=Qt.AlignmentFlag.AlignCenter)

    subt = QLabel(f"Clima predominante: {TEXT_MAP.get(estado_max, estado_max)}")
    subt.setFont(QFont("Segoe UI", 13))
    subt.setStyleSheet("color: #333333;")
    lay.addWidget(subt, alignment=Qt.AlignmentFlag.AlignCenter)

    # Tabla A^n
    _tabla_matriz(lay, matriz)

    # Vector
    vec_lbl = QLabel("Vector de probabilidades vₙ = v₀·Aⁿ")
    vec_lbl.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
    vec_lbl.setStyleSheet("color: #222222;")
    lay.addWidget(vec_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

    vec_container = QWidget()
    hl = QHBoxLayout(vec_container)
    hl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    hl.setSpacing(12)

    for name, val in zip(Estado.NOMBRES, vector):
        lbl = QLabel(f"{name}: {val * 100:.1f}%")
        lbl.setFont(QFont("Segoe UI", 11))
        lbl.setStyleSheet("color: #222222;")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setFixedWidth(90)
        lbl.setToolTip(f"{TEXT_MAP.get(name, name)} — {val*100:.1f}%")
        hl.addWidget(lbl)

    lay.addWidget(vec_container)
    lay.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
    _boton_volver(mw)


# ---------------------------------------------------------------------------
# DISTRIBUCIÓN ESTACIONARIA
# ---------------------------------------------------------------------------
def populate_estacionario(mw, vector):
    lay = mw.detail_layout
    _clear(lay)

    # Estado predominante (el de mayor probabilidad)
    idx_max = vector.index(max(vector))
    estado_max = Estado.NOMBRES[idx_max]
    mw.bg_label.setPixmap(QPixmap(BACKGROUND_MAP.get(estado_max, BACKGROUND_MAP["NU"])))

    hdr = QLabel("Distribución estacionaria (largo plazo)")
    hdr.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
    hdr.setStyleSheet("color: #222222;")
    lay.addWidget(hdr, alignment=Qt.AlignmentFlag.AlignCenter)

    tbl = QTableWidget(1, len(Estado.NOMBRES))
    tbl.setHorizontalHeaderLabels(Estado.NOMBRES)
    tbl.setVerticalHeaderLabels([""])
    tbl.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    tbl.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
    tbl.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    tbl.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    tbl.setAlternatingRowColors(False)
    tbl.setStyleSheet("""
        QTableWidget {
            background: transparent;
            border: none;
            gridline-color: rgba(0, 0, 0, 0.2);
        }

        QTableWidget::item {
            background-color: rgba(255, 255, 255, 0.4);  /* ← Uniforme en todas las celdas */
            color: #222;
            border: 1px solid rgba(0, 0, 0, 0.05);
            padding: 6px;
        }

        QTableWidget::item:alternate {
            background-color: rgba(255, 255, 255, 0.4);  /* ← Evita blanco más fuerte */
        }

        QHeaderView::section {
            background-color: rgba(255, 255, 255, 0.4);
            border: 1px solid rgba(0, 0, 0, 0.1);
            color: #222;
            font-weight: bold;
            padding: 4px;
        }
    """)

    for j, val in enumerate(vector):
        cell = QTableWidgetItem(f"{val * 100:.1f}%")
        cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        cell.setForeground(QColor("#222222"))
        tbl.setItem(0, j, cell)

    lay.addWidget(tbl, stretch=1)
    _boton_volver(mw)


# ---------------------------------------------------------------------------
# UTILIDADES
# ---------------------------------------------------------------------------
def _tabla_matriz(lay, matriz):
    n = len(Estado.NOMBRES)
    tbl = QTableWidget(n, n)
    tbl.setHorizontalHeaderLabels(Estado.NOMBRES)
    tbl.setVerticalHeaderLabels(Estado.NOMBRES)
    tbl.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    tbl.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
    tbl.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    tbl.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    tbl.setAlternatingRowColors(False)

    tbl.setStyleSheet("""
        QTableWidget {
            background: transparent;
            border: none;
            gridline-color: rgba(0, 0, 0, 0.2);
        }

        QTableWidget::item {
            background-color: rgba(255, 255, 255, 0.4);  /* ← Uniforme en todas las celdas */
            color: #222;
            border: 1px solid rgba(0, 0, 0, 0.05);
            padding: 6px;
        }

        QTableWidget::item:alternate {
            background-color: rgba(255, 255, 255, 0.4);  /* ← Evita blanco más fuerte */
        }

        QHeaderView::section {
            background-color: rgba(255, 255, 255, 0.4);
            border: 1px solid rgba(0, 0, 0, 0.1);
            color: #222;
            font-weight: bold;
            padding: 4px;
        }
    """)

    for i in range(n):
        for j in range(n):
            val = matriz[i][j]
            item = QTableWidgetItem(f"{val * 100:.1f}%")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setForeground(QColor("#222222"))
            item.setToolTip(
                f"De {TEXT_MAP.get(Estado.NOMBRES[i], Estado.NOMBRES[i])}"
                f" → {TEXT_MAP.get(Estado.NOMBRES[j], Estado.NOMBRES[j])}"
            )
            tbl.setItem(i, j, item)

    lay.addWidget(tbl, stretch=1)


def _boton_volver(mw):
    btn = QPushButton("← Volver a Resultados")
    btn.setFixedHeight(36)
    btn.setFont(QFont("Segoe UI", 11))
    btn.setStyleSheet("""
        QPushButton { background:#4A90E2; color:white; border:none; border-radius:6px; padding:8px 16px; }
        QPushButton:hover { background:#357ABD; }
    """)
    btn.clicked.connect(lambda: mw.crossfade(mw.page_results))
    mw.detail_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)


def _clear(lay):
    while lay.count():
        item = lay.takeAt(0)
        if item and item.widget():
            item.widget().deleteLater()
