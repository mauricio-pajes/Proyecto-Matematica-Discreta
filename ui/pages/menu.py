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
    font = QFont()
    font.setPointSize(16)
    font.setWeight(QFont.Weight.Bold)
    title.setFont(font)
    cl.addWidget(title)

    btn = QPushButton("➤ Nueva simulación")
    btn.setFixedHeight(40)
    btn.setFont(QFont("", 12))  # Usa la fuente predeterminada del sistema
    btn.setStyleSheet("""
        QPushButton {
            background-color: #4A90E2;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #357ABD;
        }
    """)
    btn.clicked.connect(lambda: mw.crossfade(mw.page_input))
    cl.addWidget(btn)

    exit_btn = QPushButton("✖ Salir")
    exit_btn.setFixedHeight(30)
    exit_btn.setFont(QFont("", 11))
    exit_btn.setStyleSheet("""
        QPushButton {
            background: transparent;
            color: #666666;
            border: none;
        }
        QPushButton:hover {
            color: #000000;
        }
    """)
    exit_btn.clicked.connect(mw.close)
    cl.addWidget(exit_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    lay.addWidget(card)
    return w
