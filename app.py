from PySide2 import QtCore, QtWidgets, QtGui
import random


class Converter(QtWidgets.QWidget):
    config = {
      'title': 'Currency Converter',
      'bgColor': '#333',
      'uiColor': '#FFFFFF',
      'uiMaxWidth': 150,
      'width': 800,
      'height': 220,
    }
    currencies = []
    buttonInverter = None
    currentCurrency = {
      'amount': 1,
      'code': 'EUR',
      'input': None,
      'select': None,
    }
    targetCurrency = {
      'amount': None,
      'code': 'USD',
      'input': None,
      'select': None,
    }
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.config['title'])
        self.setMinimumSize(self.config['width'], self.config['height'])

