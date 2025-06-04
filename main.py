from PyQt6.QtWidgets import QApplication
import sys
# comentario prueba 1
from ui.main_window import ModernMainMenu

def main() -> None:
    app = QApplication(sys.argv)
    win = ModernMainMenu()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
