from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
)
from PyQt6.QtGui import QFont, QIntValidator
from PyQt6.QtCore import Qt


def build(mw):
    w = QWidget()
    w.setStyleSheet("background:white;")
    lay = QVBoxLayout(w)
    lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lay.setContentsMargins(20, 20, 20, 20)
    lay.setSpacing(20)

    lbl = QLabel("¿Cuántos días quieres pronosticar? (≥1):")
    lbl.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
    lay.addWidget(lbl, alignment=Qt.AlignmentFlag.AlignCenter)

    inp = QLineEdit()
    inp.setObjectName("daysInput")
    inp.setFixedWidth(120)
    inp.setFont(QFont("Segoe UI", 12))
    inp.setPlaceholderText(">= 1")
    inp.setValidator(QIntValidator(1, 9999, w))
    inp.setStyleSheet(
        "QLineEdit { border:2px solid #CCC; border-radius:6px; padding:4px 8px; }"
        "QLineEdit:focus { border-color:#4A90E2; }"
    )
    lay.addWidget(inp, alignment=Qt.AlignmentFlag.AlignCenter)

    vec_lbl = QLabel("Vector inicial:")
    vec_lbl.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
    lay.addWidget(vec_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

    vec_container = QWidget()
    vec_container.setObjectName("vecContainer")
    hl = QHBoxLayout(vec_container)
    hl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    hl.setSpacing(8)
    lay.addWidget(vec_container)

    btn_back = QPushButton("← Volver a Matriz")
    btn_back.setFixedHeight(30)
    btn_back.setFont(QFont("Segoe UI", 11))
    btn_back.setStyleSheet(
        "QPushButton { background:#E0E0E0; color:#333; border:none; border-radius:6px; padding:6px 12px; }"
        "QPushButton:hover { background:#CCCCCC; }"
    )
    btn_back.clicked.connect(lambda: mw.crossfade(mw.page_matrix))

    btn_go = QPushButton("▶ Continuar")
    btn_go.setFixedHeight(35)
    btn_go.setFont(QFont("Segoe UI", 12))
    btn_go.setStyleSheet(
        "QPushButton { background:#50E3C2; color:white; border:none; border-radius:8px; padding:0 20px; }"
        "QPushButton:hover { background:#3BB89F; }"
    )
    btn_go.clicked.connect(lambda: _on_accept(mw))

    hb = QHBoxLayout()
    hb.setSpacing(20)
    hb.setAlignment(Qt.AlignmentFlag.AlignCenter)
    hb.addWidget(btn_back)
    hb.addWidget(btn_go)
    lay.addLayout(hb)

    return w


def _on_accept(mw):
    txt = mw.page_forecast.findChild(QLineEdit, "daysInput").text().strip()
    if txt.isdigit():
        mw.pronosticar(int(txt))


def populate_vector_inicial(mw, seq):
    from core.Estado import Estado
    vec_container = mw.page_forecast.findChild(QWidget, "vecContainer")
    layout = vec_container.layout()
    while layout.count():
        it = layout.takeAt(0)
        if it.widget():
            it.widget().deleteLater()

    last = seq[-1]
    vec = [0.0] * len(Estado.NOMBRES)
    vec[Estado.indice(last)] = 1.0

    for name, val in zip(Estado.NOMBRES, vec):
        lbl = QLabel(f"{name}: {val:.1f}")
        lbl.setFont(QFont("Segoe UI", 11))
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setFixedWidth(80)
        layout.addWidget(lbl)