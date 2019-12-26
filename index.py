import sys
import random
from PySide2 import QtWidgets
from app import Converter

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    converter = Converter()
    converter.show()
    sys.exit(app.exec_())