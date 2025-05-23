from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from core.Estado import Estado
from . import forecast


def build(mw):
    w = QWidget()
    w.setStyleSheet("background:#F0F0F0;")
    mw.mat_layout = QVBoxLayout(w)
    mw.mat_layout.setContentsMargins(16, 16, 16, 16)
    mw.mat_layout.setSpacing(12)
    return w


def populate(mw, dias: int, matriz) -> None:
    lay = mw.mat_layout

    # limpiar layout
    while lay.count():
        it = lay.takeAt(0)
        if it.widget():
            it.widget().deleteLater()

    # encabezado
    header = QLabel(f"Matriz de transición A (últimos {dias} días)")
    header.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
    header.setStyleSheet("color: #222222; font-family: 'Segoe UI', 'Arial', sans-serif;")
    lay.addWidget(header, alignment=Qt.AlignmentFlag.AlignCenter)

    estados = Estado.NOMBRES
    n = len(estados)
    table = QTableWidget(n, n)
    table.setHorizontalHeaderLabels(estados)
    table.setVerticalHeaderLabels(estados)
    table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
    table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    table.setStyleSheet(
        "QTableWidget { background:white; border:1px solid #CCC; border-radius:6px; gridline-color:#EEE; }"
        "QHeaderView::section { background:#F5F5F5; padding:6px; border:none; font-weight:bold; color: #222222; }"
    )

    for i in range(n):
        for j in range(n):
            item = QTableWidgetItem(f"{matriz[i][j]*100:.1f}%")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(i, j, item)

    lay.addWidget(table, stretch=1)

    # botón volver
    btn_back = QPushButton("← Volver a Secuencia")
    btn_back.setFixedHeight(32)
    btn_back.setFont(QFont("Segoe UI", 11))
    btn_back.setStyleSheet(
        "QPushButton { background:#E0E0E0; color:#333333; border:none; border-radius:6px; padding:6px 12px; }"
        "QPushButton:hover { background:#CCCCCC; }"
    )
    btn_back.clicked.connect(lambda: mw.crossfade(mw.page_sequence))
    lay.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignLeft)

    # botón pronosticar
    btn_forecast = QPushButton("▶ Pronosticar")
    btn_forecast.setFixedHeight(32)
    btn_forecast.setFont(QFont("Segoe UI", 11))
    btn_forecast.setStyleSheet(
        "QPushButton { background:#4A90E2; color:white; border:none; border-radius:6px; padding:6px 12px; }"
        "QPushButton:hover { background:#357ABD; }"
    )
    btn_forecast.clicked.connect(
        lambda: (
            forecast.populate_vector_inicial(mw, mw.current_sequence),
            mw.crossfade(mw.page_forecast),
        )
    )
    lay.addWidget(btn_forecast, alignment=Qt.AlignmentFlag.AlignRight)
