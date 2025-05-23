from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt

from ui.icon_map import ICON_MAP
from ui.FlowLayout import FlowLayout
from core.Estado import Estado
from core.CadenaMarkov import CadenaMarkov
from core.Calculos import multiplicarMatrizVector


def build(mw):
    w = QWidget()
    w.setStyleSheet("background:white;")
    lay = QVBoxLayout(w)
    lay.setAlignment(Qt.AlignmentFlag.AlignTop)
    lay.setContentsMargins(20, 20, 20, 20)
    lay.setSpacing(16)

    title = QLabel("Pronóstico por día")
    title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
    lay.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

    flow_container = QWidget()
    flow_container.setSizePolicy(
        flow_container.sizePolicy().Policy.Expanding,
        flow_container.sizePolicy().Policy.Preferred,
    )
    flow = FlowLayout(flow_container, margin=0, spacing=12)
    flow_container.setLayout(flow)
    mw.results_flow = flow
    lay.addWidget(flow_container)

    # botones
    btn_back = QPushButton("← Volver")
    btn_back.setFixedHeight(32)
    btn_back.setFont(QFont("Segoe UI", 11))
    btn_back.setStyleSheet(
        "QPushButton { background:#E0E0E0; color:#333; border:none; border-radius:6px; padding:6px 14px; }"
        "QPushButton:hover { background:#CCC; }"
    )
    btn_back.clicked.connect(lambda: mw.crossfade(mw.page_forecast))

    btn_stationary = QPushButton("Ver estado estacionario")
    btn_stationary.setFixedHeight(32)
    btn_stationary.setFont(QFont("Segoe UI", 11))
    btn_stationary.setStyleSheet(
        "QPushButton { background:#4A90E2; color:white; border:none; border-radius:6px; padding:6px 14px; }"
        "QPushButton:hover { background:#357ABD; }"
    )
    btn_stationary.clicked.connect(mw.mostrar_estacionario)

    hb = QHBoxLayout()
    hb.setSpacing(16)
    hb.setAlignment(Qt.AlignmentFlag.AlignCenter)
    hb.addWidget(btn_back)
    hb.addWidget(btn_stationary)
    lay.addLayout(hb)

    return w


# ------------- LÓGICA ------------- #
def populate(mw, days: int):
    flow = mw.results_flow
    while flow.count():
        it = flow.takeAt(0)
        if it.widget():
            it.widget().deleteLater()

    vec0 = [0.0] * len(Estado.NOMBRES)
    vec0[Estado.indice(mw.current_sequence[-1])] = 1.0
    cadena = CadenaMarkov(mw.current_matrix)

    day_font = QFont("Segoe UI", 10, QFont.Weight.Bold)
    ICON = 64

    for d in range(1, days + 1):
        vec_p = multiplicarMatrizVector(cadena.potenciaMatriz(d), vec0)
        idx = vec_p.index(max(vec_p))
        state = Estado.NOMBRES[idx]

        pix = QPixmap(ICON_MAP[state]).scaled(
            ICON,
            ICON,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        lbl_icon = QLabel()
        lbl_icon.setPixmap(pix)
        lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_day = QLabel(f"Día {d}")
        lbl_day.setFont(day_font)
        lbl_day.setAlignment(Qt.AlignmentFlag.AlignCenter)

        cont = QWidget()
        vl = QVBoxLayout(cont)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.setSpacing(4)
        vl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vl.addWidget(lbl_icon)
        vl.addWidget(lbl_day)

        cont.mousePressEvent = lambda ev, day=d: mw.detalle_dia(day)
        flow.addWidget(cont)
