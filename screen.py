import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QVBoxLayout, QLabel

class MyWidget(QtWidgets.QWidget):
    _L1 = 0
    _L2 = 0
    _R1 = 0
    _R2 = 0
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        layout = QVBoxLayout()
        
        self.text =QtWidgets.QLabel("yo")

        label = QLabel('label:')
        layout.addWidget(label)

        self.button = QtWidgets.QPushButton("Click me!")
        L1 =QtWidgets.QLabel("L1")
        _L1 = QtWidgets.QLabel("Hello World")
        L2 =QtWidgets.QLabel("L2")
        _L2 = QtWidgets.QLabel("Hello World")
        R1 =QtWidgets.QLabel("R1")
        _R1 = QtWidgets.QLabel("Hello World")
        R2 =QtWidgets.QLabel("R2")
        _R2 = QtWidgets.QLabel("Hello World")
        layout.addWidget(_L1) 


        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(_L1)
        self.layout.addWidget(L2)
        self.layout.addWidget(_L2)
        self.layout.addWidget(R1)
        self.layout.addWidget(_R1)
        self.layout.addWidget(R2)
        self.layout.addWidget(_R2)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText("a A 1")
        # _L2.setText("i I %")
        # _R1.setText("d D 5")
        # _R2.setText("e E 8")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(500, 300)
    widget.show()

    sys.exit(app.exec())