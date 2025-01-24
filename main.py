from PyQt5.QtWidgets import QApplication
from ui_main import ToDoApp
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec_())