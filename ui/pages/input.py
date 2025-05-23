from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QFont, QIntValidator
from PyQt6.QtCore import Qt


def build(mw):
    w = QWidget()
    w.setStyleSheet("background:white;")
    lay = QVBoxLayout(w)
    lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lay.setSpacing(20)

    instr = QLabel("Ingrese N (20–40):")
    instr.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
    instr.setStyleSheet("color: #222222; font-family: 'Segoe UI', 'Arial', sans-serif;")
    lay.addWidget(instr, alignment=Qt.AlignmentFlag.AlignCenter)

    inp = QLineEdit()
    inp.setObjectName("inputN")
    inp.setFixedWidth(120)
    inp.setFont(QFont("Segoe UI", 12))
    inp.setPlaceholderText("20–40")
    inp.setValidator(QIntValidator(20, 40, w))
    inp.setStyleSheet(
        "QLineEdit { border:2px solid #CCC; border-radius:6px; padding:4px 8px; color: #222222; }"
        "QLineEdit:focus { border-color:#4A90E2; }"
    )
    lay.addWidget(inp, alignment=Qt.AlignmentFlag.AlignCenter)

    btn_accept = QPushButton("Aceptar")
    btn_accept.setFixedHeight(35)
    btn_accept.setFont(QFont("Segoe UI", 12))
    btn_accept.setStyleSheet(
        "QPushButton { background:#50E3C2; color:white; border:none; border-radius:8px; padding:0 20px; }"
        "QPushButton:hover { background:#3BB89F; }"
    )
    btn_accept.clicked.connect(lambda: _on_accept(mw))
    lay.addWidget(btn_accept, alignment=Qt.AlignmentFlag.AlignCenter)

    btn_back = QPushButton("← Volver al menú")
    btn_back.setFixedHeight(30)
    btn_back.setFont(QFont("Segoe UI", 11))
    btn_back.setStyleSheet(
        "QPushButton { background:#E0E0E0; color:#333333; border:none; border-radius:6px; padding:6px 12px; }"
        "QPushButton:hover { background:#CCCCCC; }"
    )
    btn_back.clicked.connect(lambda: mw.crossfade(mw.page_menu))
    lay.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

    return w


def _on_accept(mw):
    n_text = mw.page_input.findChild(QLineEdit, "inputN").text().strip()
    if n_text.isdigit():
        mw.generar_simulacion(int(n_text))
