from typing import List
import time

from PyQt6.QtWidgets import (
    QMainWindow,
    QStackedWidget,
    QMessageBox,
    QGraphicsOpacityEffect,
)

from PyQt6.QtCore import (
    QPropertyAnimation,
    QEasingCurve,
    QSequentialAnimationGroup,
)

from ui.pages import (
    menu, input, sequence, matrix, forecast, results, detail,
)

from core.CadenaMarkov import CadenaMarkov
from core.Estado import Estado
from core.HistorialClima import HistorialClima
from core.MatrizTransicion import MatrizTransicion
from core.Calculos import multiplicarMatrizVector


class ModernMainMenu(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Simulador de Clima")
        self.resize(900, 450)
        self.setMinimumSize(900, 450)

        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        self.page_menu = menu.build(self)
        self.page_input = input.build(self)
        self.page_sequence = sequence.build(self)
        self.page_matrix = matrix.build(self)
        self.page_forecast = forecast.build(self)
        self.page_results = results.build(self)
        self.page_detail = detail.build(self)

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

    def generar_simulacion(self, n: int) -> None:
        semilla = int(time.time() * 1000)
        historial = HistorialClima(n, semilla)
        matriz = MatrizTransicion(historial.secuencia).matriz

        self.current_sequence = historial.secuencia
        self.current_matrix = matriz

        sequence.populate(self, self.current_sequence)
        self.crossfade(self.page_sequence)

    def pronosticar(self, dias: int) -> None:
        if dias < 1:
            QMessageBox.warning(self, "Valor inválido", "Debes ingresar un número ≥ 1.")
            return

        results.populate(self, dias)
        self.crossfade(self.page_results)

    def detalle_dia(self, dia: int) -> None:
        cm = CadenaMarkov(self.current_matrix)
        matriz_pot = cm.potenciaMatriz(dia)

        v0 = [0.0] * len(Estado.NOMBRES)
        v0[Estado.indice(self.current_sequence[-1])] = 1.0
        v_day = multiplicarMatrizVector(matriz_pot, v0)

        detail.populate_detalle(self, dia, matriz_pot, v_day)
        self.crossfade(self.page_detail)

    def mostrar_estacionario(self) -> None:
        if not self.current_matrix:
            QMessageBox.warning(self, "Sin matriz", "Genera primero una simulación.")
            return
        cm = CadenaMarkov(self.current_matrix)
        vect_pi = cm.vectorEstacionario()
        detail.populate_estacionario(self, vect_pi)
        self.crossfade(self.page_detail)

    def crossfade(self, to_widget) -> None:
        effect = QGraphicsOpacityEffect(self.stack)
        self.stack.setGraphicsEffect(effect)

        fade_out = QPropertyAnimation(effect, b"opacity", self)
        fade_out.setDuration(600)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.Type.InOutQuad)

        fade_in = QPropertyAnimation(effect, b"opacity", self)
        fade_in.setDuration(600)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.Type.InOutQuad)

        seq = QSequentialAnimationGroup(self)
        seq.addAnimation(fade_out)
        fade_out.finished.connect(lambda: self.stack.setCurrentWidget(to_widget))
        seq.addAnimation(fade_in)
        seq.start()
