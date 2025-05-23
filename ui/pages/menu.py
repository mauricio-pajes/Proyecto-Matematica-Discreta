from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QLabel, QPushButton, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QFont, QColor, QPixmap
from PyQt6.QtCore import Qt
from ui.icon_map import UPC_LOGO

def build(mw):
    w = QWidget()
    w.setStyleSheet(
        "QWidget { background: qlineargradient(x1:0 y1:0, x2:1 y2:1,"
        " stop:0 #4A90E2, stop:1 #50E3C2); }"
    )
    lay = QVBoxLayout(w)
    lay.setAlignment(Qt.AlignmentFlag.AlignCenter)

    card = QFrame()
    card.setFixedSize(350, 300)
    card.setStyleSheet("background:white; border-radius:12px;")
    shadow = QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=5)
    shadow.setColor(QColor(0, 0, 0, 80))
    card.setGraphicsEffect(shadow)

    cl = QVBoxLayout(card)
    cl.setContentsMargins(30, 30, 30, 30)
    cl.setSpacing(15)
    cl.setAlignment(Qt.AlignmentFlag.AlignTop)

    logo = QLabel()
    logo.setFixedSize(100, 100)
    logo.setPixmap(QPixmap(UPC_LOGO).scaled(
        100, 100, Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation
    ))
    cl.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)

    title = QLabel("Simulador de Clima\nCadenas de Márkov")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
    cl.addWidget(title)

    btn = QPushButton("➤ Nueva simulación")
    btn.setFixedHeight(40)
    btn.setFont(QFont("Segoe UI", 12))
    btn.setStyleSheet(
        "QPushButton { background:#4A90E2; color:white; border:none; border-radius:8px; }"
        "QPushButton:hover { background:#357ABD; }"
    )
    btn.clicked.connect(lambda: mw.crossfade(mw.page_input))
    cl.addWidget(btn)

    exit_btn = QPushButton("✖ Salir")
    exit_btn.setFixedHeight(30)
    exit_btn.setFont(QFont("Segoe UI", 11))
    exit_btn.setStyleSheet("background:transparent; color:#666666; border:none;")
    exit_btn.clicked.connect(mw.close)
    cl.addWidget(exit_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    lay.addWidget(card)
    return w
