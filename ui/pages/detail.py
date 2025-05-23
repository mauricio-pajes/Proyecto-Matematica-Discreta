from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QHeaderView
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

from core.Estado import Estado
from . import forecast


def build(mw):
    w = QWidget()
    w.setStyleSheet("background:#F0F0F0;")
    mw.detail_layout = QVBoxLayout(w)
    mw.detail_layout.setContentsMargins(16, 16, 16, 16)
    mw.detail_layout.setSpacing(12)
    return w


def populate_detalle(mw, day: int, matriz, vector):
    lay = mw.detail_layout
    _clear(lay)

    # Header label
    header = QLabel(f"Matriz A^{day} y vector de probabilidades")
    header.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
    header.setStyleSheet("color: #222222;")
    lay.addWidget(header, alignment=Qt.AlignmentFlag.AlignCenter)

    _tabla_matriz(lay, matriz)

    # Vector label
    vec_lbl = QLabel("Vector de probabilidades vₙ = v₀·Aⁿ")
    vec_lbl.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
    vec_lbl.setStyleSheet("color: #222222;")
    lay.addWidget(vec_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

    # Vector values
    vec_container = QWidget()
    hl = QHBoxLayout(vec_container)
    hl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    hl.setSpacing(12)
    for name, val in zip(Estado.NOMBRES, vector):
        lbl = QLabel(f"{name}: {val*100:.1f}%")
        lbl.setFont(QFont("Segoe UI", 11))
        lbl.setStyleSheet("color: #222222;")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setFixedWidth(90)
        hl.addWidget(lbl)
    lay.addWidget(vec_container)

    _boton_volver(mw)


def populate_estacionario(mw, vector):
    lay = mw.detail_layout
    _clear(lay)

    # Estacionaria header
    hdr = QLabel("Distribución estacionaria (largo plazo)")
    hdr.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
    hdr.setStyleSheet("color: #222222;")
    lay.addWidget(hdr, alignment=Qt.AlignmentFlag.AlignCenter)

    # Table of stationary distribution
    tbl = QTableWidget(1, len(Estado.NOMBRES))
    tbl.setHorizontalHeaderLabels(Estado.NOMBRES)
    tbl.setVerticalHeaderLabels([""])
    tbl.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    tbl.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
    tbl.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    tbl.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    tbl.setStyleSheet(
        "QTableWidget { background:white; color:#222222; border:1px solid #CCC; border-radius:6px; gridline-color:#EEE; }"
        "QHeaderView::section { background:#F5F5F5; padding:6px; border:none; font-weight:bold; color:#222222; }"
    )
    for j, val in enumerate(vector):
        cell = QTableWidgetItem(f"{val*100:.1f}%")
        cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        cell.setForeground(QColor("#222222"))
        tbl.setItem(0, j, cell)

    lay.addWidget(tbl, stretch=1)

    _boton_volver(mw)


def _clear(lay):
    while lay.count():
        it = lay.takeAt(0)
        if it.widget():
            it.widget().deleteLater()


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
    tbl.setStyleSheet(
        "QTableWidget { background:white; color:#222222; border:1px solid #CCC; border-radius:6px; gridline-color:#EEE; }"
        "QHeaderView::section { background:#F5F5F5; padding:6px; border:none; font-weight:bold; color:#222222; }"
    )
    for i in range(n):
        for j in range(n):
            item = QTableWidgetItem(f"{matriz[i][j]*100:.1f}%")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setForeground(QColor("#222222"))
            tbl.setItem(i, j, item)
    lay.addWidget(tbl, stretch=1)


def _boton_volver(mw):
    btn_back = QPushButton("← Volver a Resultados")
    btn_back.setFixedHeight(32)
    btn_back.setFont(QFont("Segoe UI", 11))
    btn_back.setStyleSheet(
        "QPushButton { background:#E0E0E0; color:#333333; border:none; border-radius:6px; padding:6px 12px; }"
        "QPushButton:hover { background:#CCCCCC; }"
    )
    btn_back.clicked.connect(lambda: mw.crossfade(mw.page_results))
    mw.detail_layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)