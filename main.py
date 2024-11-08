import sys
from PyQt6.QtWidgets import QApplication
from ui_main import TaskManager

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TaskManager()
    window.show()
    sys.exit(app.exec())