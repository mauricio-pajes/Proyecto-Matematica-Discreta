from typing import List

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt

from ui.icon_map import ICON_MAP, TEXT_MAP
from ui.FlowLayout import FlowLayout
from . import matrix

def build(mw):
    w = QWidget()
    w.setStyleSheet("background:white;")
    layout = QVBoxLayout(w)
    layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(16)

    lbl = QLabel("Secuencia histórica:")
    lbl.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
    lbl.setStyleSheet("color: #222222; font-family: 'Segoe UI', 'Arial', sans-serif;")
    layout.addWidget(lbl, alignment=Qt.AlignmentFlag.AlignCenter)

    flow_container = QWidget()
    flow = FlowLayout(flow_container, margin=0, spacing=8)
    flow_container.setLayout(flow)
    mw.seq_flow = flow
    layout.addWidget(flow_container)

    btn_matrix = QPushButton("▶ Ver Matriz")
    btn_matrix.setFixedHeight(30)
    btn_matrix.setFont(QFont("Segoe UI", 11))
    btn_matrix.setStyleSheet(
        "QPushButton { background:#50E3C2; color:white; border:none; "
        "border-radius:6px; padding:6px 12px; }"
        "QPushButton:hover { background:#3BB89F; }"
    )
    btn_matrix.clicked.connect(
        lambda: (
            matrix.populate(
                mw,
                len(mw.current_sequence),
                mw.current_matrix,
            ),
            mw.crossfade(mw.page_matrix),
        )
    )

    btn_back = QPushButton("← Nueva simulación")
    btn_back.setFixedHeight(30)
    btn_back.setFont(QFont("Segoe UI", 11))
    btn_back.setStyleSheet(
        "QPushButton { background:#E0E0E0; color:#333333; border:none; "
        "border-radius:6px; padding:6px 12px; }"
        "QPushButton:hover { background:#CCCCCC; }"
    )
    btn_back.clicked.connect(lambda: mw.crossfade(mw.page_input))

    hl = QHBoxLayout()
    hl.setSpacing(20)
    hl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    hl.addWidget(btn_back)
    hl.addWidget(btn_matrix)
    layout.addLayout(hl)

    return w


def populate(mw, seq: List[str]) -> None:
    flow = mw.seq_flow
    while flow.count():
        it = flow.takeAt(0)
        if it.widget():
            it.widget().deleteLater()

    ICON = 50
    arrow_font = QFont("Segoe UI", 12, QFont.Weight.Bold)

    for idx, state in enumerate(seq):
        cont = QWidget()
        vl = QVBoxLayout(cont)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.setSpacing(4)
        vl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pix = QPixmap(ICON_MAP[state]).scaled(
            ICON,
            ICON,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        lbl_icon = QLabel()
        lbl_icon.setPixmap(pix)
        lbl_icon.setFixedSize(ICON, ICON)
        vl.addWidget(lbl_icon, alignment=Qt.AlignmentFlag.AlignCenter)

        lbl_txt = QLabel(TEXT_MAP[state])
        lbl_txt.setFont(QFont("Segoe UI", 10))
        lbl_txt.setStyleSheet("color: #222222; font-family: 'Segoe UI', 'Arial', sans-serif;")
        lbl_txt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vl.addWidget(lbl_txt, alignment=Qt.AlignmentFlag.AlignCenter)

        flow.addWidget(cont)

        if idx < len(seq) - 1:
            arr = QLabel("→")
            arr.setFont(arrow_font)
            arr.setStyleSheet("color: #222222;")
            arr.setFixedWidth(ICON // 3)
            arr.setAlignment(Qt.AlignmentFlag.AlignCenter)
            flow.addWidget(arr)