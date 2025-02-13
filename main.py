from PySide6 import QtWidgets, QtCore, QtGui
from css import main_css as css
from functools import partial


class CentralWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CentralWidget, self).__init__()
        self.setStyleSheet(css.central_widget)

        self.lbl_title = QtWidgets.QLabel("Título", parent=self)


class Main_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main_Window, self).__init__()
        central_widget = CentralWidget()
        self.setCentralWidget(central_widget)
        self.setStyleSheet(css.main_window)


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    main_window = Main_Window()
    main_window.showMaximized()
    app.exec()
