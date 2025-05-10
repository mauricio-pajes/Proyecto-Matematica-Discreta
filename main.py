import sys
import time
from typing import List

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QToolButton,
    QPushButton,
    QFrame,
    QStackedWidget,
    QGraphicsOpacityEffect,
    QGraphicsDropShadowEffect,
    QLineEdit,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QLayout,
    QSizePolicy,
    QHeaderView
)
from PyQt6.QtGui import (
    QFont,
    QColor,
    QPixmap,
    QIcon,
    QIntValidator
)
from PyQt6.QtCore import (
    Qt,
    QSize,
    QPropertyAnimation,
    QSequentialAnimationGroup,
    QEasingCurve,
    QRect,
    QPoint, pyqtSignal
)

from CadenaMarkov import CadenaMarkov
from Calculos import multiplicarMatrizVector
from Estado import Estado
from FlowLayout import FlowLayout
from HistorialClima import HistorialClima
from MatrizTransicion import MatrizTransicion


class ModernMainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador de Clima")
        self.resize(900, 450)
        self.setMinimumSize(900, 450)

        self.icon_map = {
            'NU': 'nublado.png',
            'PN': 'parcialmente-nublado.png',
            'PS': 'parcialmente-soleado.png',
            'SOL': 'soleado.png'
        }

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.page_menu = self.build_menu_page()
        self.page_input = self.build_input_page()
        self.page_sequence = self.build_sequence_page()
        self.page_matrix = self.build_matrix_page()
        self.page_forecast = self.build_forecast_page()
        self.page_results = self.build_results_page()
        self.page_detail = self.build_detail_page()

        for page in (
                self.page_menu,
                self.page_input,
                self.page_sequence,
                self.page_matrix,
                self.page_forecast,
                self.page_results,
                self.page_detail,
        ):
            self.stack.addWidget(page)

        self.current_sequence: List[str] = []
        self.current_matrix: List[List[float]] = []

    def build_menu_page(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4A90E2, stop:1 #50E3C2
                );
            }
        """)
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
        pix = QPixmap("UPC_logo_transparente.png").scaled(
            100, 100,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        logo.setPixmap(pix)
        cl.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Simulador de Clima\nCadenas de Márkov")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        cl.addWidget(title)

        btn = QPushButton("➤ Nueva simulación")
        btn.setFixedHeight(40)
        btn.setFont(QFont("Segoe UI", 12))
        btn.setStyleSheet("""
            QPushButton { background:#4A90E2; color:white; border:none; border-radius:8px; }
            QPushButton:hover { background:#357ABD; }
        """)
        btn.clicked.connect(lambda: self.crossfade(self.page_input))
        cl.addWidget(btn)

        exit_btn = QPushButton("✖ Salir")
        exit_btn.setFixedHeight(30)
        exit_btn.setFont(QFont("Segoe UI", 11))
        exit_btn.setStyleSheet("background:transparent; color:#666666; border:none;")
        exit_btn.clicked.connect(self.close)
        cl.addWidget(exit_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        lay.addWidget(card)
        return w

    def build_input_page(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background:white;")
        lay = QVBoxLayout(w)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setSpacing(20)

        instr = QLabel("Ingrese N (20–40):")
        instr.setFont(QFont("Segoe UI", 14))
        lay.addWidget(instr, alignment=Qt.AlignmentFlag.AlignCenter)

        self.input_n = QLineEdit()
        self.input_n.setFixedWidth(120)
        self.input_n.setFont(QFont("Segoe UI", 12))
        self.input_n.setPlaceholderText("20–40")
        self.input_n.setValidator(QIntValidator(20, 40, self))
        self.input_n.setStyleSheet("""
            QLineEdit { border:2px solid #CCC; border-radius:6px; padding:4px 8px; }
            QLineEdit:focus { border-color:#4A90E2; }
        """)
        lay.addWidget(self.input_n, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_accept = QPushButton("Aceptar")
        btn_accept.setFixedHeight(35)
        btn_accept.setFont(QFont("Segoe UI", 12))
        btn_accept.setStyleSheet("""
            QPushButton { background:#50E3C2; color:white; border:none; border-radius:8px; padding:0 20px; }
            QPushButton:hover { background:#3BB89F; }
        """)
        btn_accept.clicked.connect(self.on_n_accepted)
        lay.addWidget(btn_accept, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_back = QPushButton("← Volver al menú")
        btn_back.setFixedHeight(30)
        btn_back.setFont(QFont("Segoe UI", 11))
        btn_back.setStyleSheet("""
            QPushButton { background:#E0E0E0; color:#333333; border:none; border-radius:6px; padding:6px 12px; }
            QPushButton:hover { background:#CCCCCC; }
        """)
        btn_back.clicked.connect(lambda: self.crossfade(self.page_menu))
        lay.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

        return w

    def build_sequence_page(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background:white;")
        layout = QVBoxLayout(w)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        lbl = QLabel("Secuencia histórica:")
        lbl.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        flow_container = QWidget()
        flow = FlowLayout(flow_container, margin=0, spacing=8)
        flow_container.setLayout(flow)
        self.seq_flow = flow
        layout.addWidget(flow_container)

        btn_matrix = QPushButton("▶ Ver Matriz")
        btn_matrix.setFixedHeight(30)
        btn_matrix.setFont(QFont("Segoe UI", 11))
        btn_matrix.setStyleSheet("""
            QPushButton { 
                background:#50E3C2; color:white; 
                border:none; border-radius:6px; 
                padding:6px 12px; 
            }
            QPushButton:hover { background:#3BB89F; }
        """)
        btn_matrix.clicked.connect(lambda: (
            self.populate_matrix_page(len(self.current_sequence), self.current_matrix),
            self.crossfade(self.page_matrix)
        ))

        btn_back = QPushButton("← Nueva simulación")
        btn_back.setFixedHeight(30)
        btn_back.setFont(QFont("Segoe UI", 11))
        btn_back.setStyleSheet("""
            QPushButton { 
                background:#E0E0E0; color:#333; 
                border:none; border-radius:6px; 
                padding:6px 12px; 
            }
            QPushButton:hover { background:#CCCCCC; }
        """)
        btn_back.clicked.connect(lambda: self.crossfade(self.page_input))

        hl = QHBoxLayout()
        hl.setSpacing(20)
        hl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hl.addWidget(btn_back)
        hl.addWidget(btn_matrix)
        layout.addLayout(hl)

        return w

    def build_matrix_page(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background: #F0F0F0;")
        self.mat_layout = QVBoxLayout(w)
        self.mat_layout.setContentsMargins(16, 16, 16, 16)
        self.mat_layout.setSpacing(12)
        return w

    def on_n_accepted(self) -> None:
        text = self.input_n.text().strip()
        if not text.isdigit():
            QMessageBox.warning(self, "Valor inválido", "Ingresa un número entre 20 y 40.")
            return

        n = int(text)
        if n < 20 or n > 40:
            QMessageBox.warning(self, "Fuera de rango", "El valor debe estar entre 20 y 40.")
            return

        semilla = int(time.time() * 1000)
        historial = HistorialClima(n, semilla)
        matriz = MatrizTransicion(historial.secuencia).matriz

        self.current_sequence = historial.secuencia
        self.current_matrix = matriz

        self.populate_sequence_page(self.current_sequence)
        self.crossfade(self.page_sequence)
    def populate_sequence_page(self, seq: List[str]):
        """
        Muestra la secuencia histórica con iconos de 64×64px fijos y texto,
        para que su tamaño no cambie entre navegaciones.
        """
        # 1) Limpiar ítems previos
        while self.seq_flow.count():
            item = self.seq_flow.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        text_map = {
            'SOL': 'Soleado',
            'PS': 'P. Soleado',
            'PN': 'P. Nublado',
            'NU': 'Nublado'
        }

        ICON = 50
        arrow_font = QFont("Segoe UI", 12, QFont.Weight.Bold)

        for idx, state in enumerate(seq):
            # Contenedor vertical
            cont = QWidget()
            vl = QVBoxLayout(cont)
            vl.setContentsMargins(0, 0, 0, 0)
            vl.setSpacing(4)
            vl.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Ícono 64×64
            pix = QPixmap(self.icon_map[state]).scaled(
                ICON, ICON,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            lbl_icon = QLabel()
            lbl_icon.setPixmap(pix)
            lbl_icon.setFixedSize(ICON, ICON)
            vl.addWidget(lbl_icon, alignment=Qt.AlignmentFlag.AlignCenter)

            # Texto
            lbl_txt = QLabel(text_map[state])
            lbl_txt.setFont(QFont("Segoe UI", 10))
            lbl_txt.setAlignment(Qt.AlignmentFlag.AlignCenter)
            vl.addWidget(lbl_txt, alignment=Qt.AlignmentFlag.AlignCenter)

            self.seq_flow.addWidget(cont)

            # Flecha salvo al final
            if idx < len(seq) - 1:
                arr = QLabel("→")
                arr.setFont(arrow_font)
                arr.setFixedWidth(ICON // 3)
                arr.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.seq_flow.addWidget(arr)

    def populate_matrix_page(self, dias: int, matriz):
        """
        Rellena la página con la cabecera, la tabla visual,
        el botón para volver y un botón para ir al pronóstico.
        """
        # 1) Limpiar el layout existente
        while self.mat_layout.count():
            item = self.mat_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # 2) Título centrado
        header = QLabel(f"Matriz de transición A (últimos {dias} días)")
        header.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.mat_layout.addWidget(header, alignment=Qt.AlignmentFlag.AlignCenter)

        # 3) Construir tabla
        estados = Estado.NOMBRES
        n = len(estados)
        table = QTableWidget(n, n)
        table.setHorizontalHeaderLabels(estados)
        table.setVerticalHeaderLabels(estados)

        # Desactivar edición y selección
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Configurar encabezados para estirar
        from PyQt6.QtWidgets import QHeaderView
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Estilo "card" para la tabla
        table.setStyleSheet(
            "QTableWidget {"
            " background-color: white;"
            " border: 1px solid #CCC;"
            " border-radius: 6px;"
            " gridline-color: #EEE;"
            " }"
            "QHeaderView::section {"
            " background-color: #F5F5F5;"
            " padding: 6px;"
            " border: none;"
            " font-weight: bold;"
            " }"
        )

        # Rellenar datos
        for i in range(n):
            for j in range(n):
                item = QTableWidgetItem(f"{matriz[i][j]:.3f}")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(i, j, item)

        # 4) Añadir tabla con stretch para ocupar espacio
        self.mat_layout.addWidget(table, stretch=1)

        # 5) Botón para volver a la secuencia
        btn_back = QPushButton("← Volver a Secuencia")
        btn_back.setFixedHeight(32)
        btn_back.setFont(QFont("Segoe UI", 11))
        btn_back.setStyleSheet(
            "QPushButton {"
            " background-color: #E0E0E0;"
            " color: #333333;"
            " border: none;"
            " border-radius: 6px;"
            " padding: 6px 12px;"
            " }"
            "QPushButton:hover { background-color: #CCCCCC; }"
        )
        btn_back.clicked.connect(lambda: self.crossfade(self.page_sequence))
        self.mat_layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignLeft)

        # 6) Botón para ir al pronóstico
        btn_forecast = QPushButton("▶ Pronosticar")
        btn_forecast.setFixedHeight(32)
        btn_forecast.setFont(QFont("Segoe UI", 11))
        btn_forecast.setStyleSheet(
            "QPushButton {"
            " background-color: #4A90E2;"
            " color: white;"
            " border: none;"
            " border-radius: 6px;"
            " padding: 6px 12px;"
            " }"
            "QPushButton:hover { background-color: #357ABD; }"
        )
        btn_forecast.clicked.connect(
            lambda: (
                self.populate_forecast_page(self.current_sequence),
                self.crossfade(self.page_forecast)
            )
        )
        self.mat_layout.addWidget(btn_forecast, alignment=Qt.AlignmentFlag.AlignRight)

    def build_forecast_page(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background: white;")
        lay = QVBoxLayout(w)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(20)

        lbl = QLabel("¿Cuántos días quieres pronosticar? (≥1):")
        lbl.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        lay.addWidget(lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        self.input_forecast = QLineEdit()
        self.input_forecast.setFixedWidth(120)
        self.input_forecast.setFont(QFont("Segoe UI", 12))
        self.input_forecast.setPlaceholderText(">= 1")
        self.input_forecast.setValidator(QIntValidator(1, 9999, self))
        self.input_forecast.setStyleSheet("""
            QLineEdit {
                border: 2px solid #CCC;
                border-radius: 6px;
                padding: 4px 8px;
            }
            QLineEdit:focus {
                border-color: #4A90E2;
            }
        """)
        lay.addWidget(self.input_forecast, alignment=Qt.AlignmentFlag.AlignCenter)

        # 3) Vector inicial
        vec_lbl = QLabel("Vector inicial:")
        vec_lbl.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        lay.addWidget(vec_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        self.vec_container = QWidget()
        hl = QHBoxLayout(self.vec_container)
        hl.setSpacing(8)
        hl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self.vec_container)

        # 4) Botones
        btn_back = QPushButton("← Volver a Matriz")
        btn_back.setFixedHeight(30)
        btn_back.setFont(QFont("Segoe UI", 11))
        btn_back.setStyleSheet("""
            QPushButton {
                background: #E0E0E0;
                color: #333333;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background: #CCCCCC;
                color: #333333;
            }
        """)
        btn_back.clicked.connect(lambda: self.crossfade(self.page_matrix))

        btn_go = QPushButton("▶ Continuar")
        btn_go.setFixedHeight(35)
        btn_go.setFont(QFont("Segoe UI", 12))
        btn_go.setStyleSheet("""
            QPushButton {
                background: #50E3C2;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background: #3BB89F;
                color: white;
            }
        """)
        btn_go.clicked.connect(self.on_forecast_accepted)

        h_btns = QHBoxLayout()
        h_btns.setSpacing(20)
        h_btns.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h_btns.addWidget(btn_back)
        h_btns.addWidget(btn_go)
        lay.addLayout(h_btns)

        return w

    def populate_forecast_page(self, seq: List[str]):
        # Generar vector inicial
        last = seq[-1]
        vec = [0.0] * len(Estado.NOMBRES)
        vec[Estado.indice(last)] = 1.0

        # Limpiar lo previo
        layout = self.vec_container.layout()
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        # Mostrar cada componente
        for name, val in zip(Estado.NOMBRES, vec):
            lbl = QLabel(f"{name}: {val:.1f}")
            lbl.setFont(QFont("Segoe UI", 11))
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setFixedWidth(80)
            layout.addWidget(lbl)

    def build_results_page(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background:white;")

        lay = QVBoxLayout(w)
        lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(16)

        # Título
        title = QLabel("Pronóstico por día")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        lay.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        # FlowLayout de iconos
        flow_container = QWidget()
        flow_container.setSizePolicy(  # ← ancho expansivo
            QSizePolicy.Policy.Expanding,  # horizontal
            QSizePolicy.Policy.Preferred  # vertical
        )
        flow = FlowLayout(flow_container, margin=0, spacing=12)
        flow_container.setLayout(flow)
        self.results_flow = flow

        lay.addWidget(flow_container)  # ← sin AlignHCenter

        # Botones parte inferior
        btn_back = QPushButton("← Volver")
        btn_back.setFixedHeight(32)
        btn_back.setFont(QFont("Segoe UI", 11))
        btn_back.setStyleSheet(
            "QPushButton { background:#E0E0E0; color:#333; border:none; border-radius:6px; padding:6px 14px; }"
            "QPushButton:hover { background:#CCC; }"
        )
        btn_back.clicked.connect(lambda: self.crossfade(self.page_forecast))

        btn_stationary = QPushButton("Ver estado estacionario")
        btn_stationary.setFixedHeight(32)
        btn_stationary.setFont(QFont("Segoe UI", 11))
        btn_stationary.setStyleSheet(
            "QPushButton { background:#4A90E2; color:white; border:none; border-radius:6px; padding:6px 14px; }"
            "QPushButton:hover { background:#357ABD; }"
        )
        btn_stationary.clicked.connect(self.show_stationary_distribution)

        h_btns = QHBoxLayout()
        h_btns.setSpacing(16)
        h_btns.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h_btns.addWidget(btn_back)
        h_btns.addWidget(btn_stationary)
        lay.addLayout(h_btns)

        return w

    def on_forecast_accepted(self) -> None:
        text = self.input_forecast.text().strip()
        if not text.isdigit() or int(text) < 1:
            QMessageBox.warning(
                self, "Valor inválido",
                "Por favor ingresa un número de días válido (>= 1)."
            )
            return

        days = int(text)
        self.populate_forecast_page(self.current_sequence)  # A
        self.populate_results_page(days)  # B
        self.crossfade(self.page_results)  # C

    def populate_results_page(self, days: int) -> None:
        """Genera un bloque (icono + “Día n”) por cada día pronosticado."""
        # 1) Limpiar anteriores
        while self.results_flow.count():
            item = self.results_flow.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 2) Vector inicial y cadena
        vec0 = [0.0] * len(Estado.NOMBRES)
        vec0[Estado.indice(self.current_sequence[-1])] = 1.0
        cadena = CadenaMarkov(self.current_matrix)

        day_font = QFont("Segoe UI", 10, QFont.Weight.Bold)
        ICON = 64  # tamaño fijo → evita problemas de anchura 0

        for d in range(1, days + 1):
            # Estado más probable al día d
            vec_p = multiplicarMatrizVector(cadena.potenciaMatriz(d), vec0)
            state_idx = vec_p.index(max(vec_p))
            state = Estado.NOMBRES[state_idx]

            # Ícono
            pix = QPixmap(self.icon_map[state]).scaled(
                ICON, ICON,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            lbl_icon = QLabel()
            lbl_icon.setPixmap(pix)
            lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Texto “Día n”
            lbl_day = QLabel(f"Día {d}")
            lbl_day.setFont(day_font)
            lbl_day.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Contenedor
            cont = QWidget()
            vl = QVBoxLayout(cont)
            vl.setContentsMargins(0, 0, 0, 0)
            vl.setSpacing(4)
            vl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            vl.addWidget(lbl_icon)
            vl.addWidget(lbl_day)

            # Click → página detalle
            cont.mousePressEvent = lambda ev, day=d, st=state: self.on_day_button_clicked(day, st)

            self.results_flow.addWidget(cont)

    def build_detail_page(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background: #F0F0F0;")
        self.detail_layout = QVBoxLayout(w)
        self.detail_layout.setContentsMargins(16, 16, 16, 16)
        self.detail_layout.setSpacing(12)
        return w

    def populate_detail_page(self, day: int, matriz, vector):
        # 1) Limpiar
        while self.detail_layout.count():
            item = self.detail_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 2) Encabezado
        header = QLabel(f"Matriz A^{day} y vector de probabilidades")
        header.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.detail_layout.addWidget(header, alignment=Qt.AlignmentFlag.AlignCenter)

        # 3) Tabla de la matriz (idéntico estilo)
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
            "QHeaderView::section { background:#F5F5F5; padding:6px; border:none; font-weight:bold; }"
        )
        for i in range(n):
            for j in range(n):
                item = QTableWidgetItem(f"{matriz[i][j]:.3f}")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(i, j, item)
        self.detail_layout.addWidget(table, stretch=1)

        # 4) Vector de probabilidades
        vec_lbl = QLabel("Vector de probabilidades vₙ = v₀·Aⁿ")
        vec_lbl.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.detail_layout.addWidget(vec_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        vec_container = QWidget()
        hl = QHBoxLayout(vec_container)
        hl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hl.setSpacing(12)
        for name, val in zip(Estado.NOMBRES, vector):
            lbl = QLabel(f"{name}: {val:.3f}")
            lbl.setFont(QFont("Segoe UI", 11))
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setFixedWidth(90)
            hl.addWidget(lbl)
        self.detail_layout.addWidget(vec_container)

        # 5) Botón volver
        btn_back = QPushButton("← Volver a Resultados")
        btn_back.setFixedHeight(32)
        btn_back.setFont(QFont("Segoe UI", 11))
        btn_back.setStyleSheet(
            "QPushButton { background:#E0E0E0; color:#333; border:none; border-radius:6px; padding:6px 12px; }"
            "QPushButton:hover { background:#CCC; }"
        )
        btn_back.clicked.connect(lambda: self.crossfade(self.page_results))
        self.detail_layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

    def on_day_button_clicked(self, day: int, state: str):
        cm = CadenaMarkov(self.current_matrix)
        matriz_pot = cm.potenciaMatriz(day)

        v0 = [0.0] * len(Estado.NOMBRES)
        v0[Estado.indice(self.current_sequence[-1])] = 1.0
        v_day = multiplicarMatrizVector(matriz_pot, v0)

        # Mostrar en la página de detalle
        self.populate_detail_page(day, matriz_pot, v_day)
        self.crossfade(self.page_detail)

    def populate_stationary_page(self, vector):

        # Limpiar layout
        while self.detail_layout.count():
            it = self.detail_layout.takeAt(0)
            if it.widget():
                it.widget().deleteLater()

        # Encabezado
        hdr = QLabel("Distribución estacionaria  (largo plazo)")
        hdr.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.detail_layout.addWidget(hdr, alignment=Qt.AlignmentFlag.AlignCenter)

        # Tabla 1×N
        estados = Estado.NOMBRES
        n = len(estados)
        tbl = QTableWidget(1, n)
        tbl.setHorizontalHeaderLabels(estados)
        tbl.setVerticalHeaderLabels([""])
        tbl.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tbl.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        tbl.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tbl.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tbl.setStyleSheet(
            "QTableWidget { background:white; border:1px solid #CCC; border-radius:6px; gridline-color:#EEE; }"
            "QHeaderView::section { background:#F5F5F5; padding:6px; border:none; font-weight:bold; }"
        )
        for j, val in enumerate(vector):
            cell = QTableWidgetItem(f"{val:.3f}")
            cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            tbl.setItem(0, j, cell)

        self.detail_layout.addWidget(tbl, stretch=1)

        # Botón volver
        back = QPushButton("← Volver a Resultados")
        back.setFixedHeight(32)
        back.setFont(QFont("Segoe UI", 11))
        back.setStyleSheet(
            "QPushButton { background:#E0E0E0; color:#333; border:none; border-radius:6px; padding:6px 12px; }"
            "QPushButton:hover { background:#CCC; }"
        )
        back.clicked.connect(lambda: self.crossfade(self.page_results))
        self.detail_layout.addWidget(back, alignment=Qt.AlignmentFlag.AlignCenter)

    def show_stationary_distribution(self):
        if not self.current_matrix:
            QMessageBox.warning(self, "Sin matriz", "Primero genera una simulación.")
            return

        cm = CadenaMarkov(self.current_matrix)
        vect_pi = cm.vectorEstacionario()
        self.populate_stationary_page(vect_pi)
        self.crossfade(self.page_detail)

    def crossfade(self, to_widget: QWidget):
        stack = self.stack
        effect = QGraphicsOpacityEffect(stack)
        stack.setGraphicsEffect(effect)

        fade_out = QPropertyAnimation(effect, b"opacity")
        fade_out.setDuration(600)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.Type.InOutQuad)

        fade_in = QPropertyAnimation(effect, b"opacity")
        fade_in.setDuration(600)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.Type.InOutQuad)

        seq = QSequentialAnimationGroup(self)
        seq.addAnimation(fade_out)
        fade_out.finished.connect(lambda: stack.setCurrentWidget(to_widget))
        seq.addAnimation(fade_in)
        seq.start()


def main():
    app = QApplication(sys.argv)
    window = ModernMainMenu()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
