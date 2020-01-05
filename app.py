from currency_converter import RateNotFoundError, CurrencyConverter as CurrencyConverter_
from PySide2 import QtCore
from PySide2.QtWidgets import QDialog, QLineEdit, QPushButton, QHBoxLayout, QComboBox


class Converter(QDialog):
    c = CurrencyConverter_()
    params = {
        'title': 'Currency Converter',
        'background': 'black',
        'uiColor': 'white',
        'layoutWidth': 150
    }
    currentAmount = {
        'amount': 1,
        'code': 'EUR'
    }
    targetCurrency = {
        'amount': None,
        'code': 'USD'
    }

    def __init__(self, parent=None):
        super(Converter, self).__init__(parent)
        self.setWindowTitle(self.params['title'])
        self.setStyleSheet(
            ''.join(['background-color:', self.params['background'], ';']))
        self.currencies()
        self.form()

    def form(self):
        # init layout
        layout = QHBoxLayout()
        self.currentAmount['input'] = QLineEdit()
        self.currentAmount['select'] = QComboBox()
        self.targetCurrency['input'] = QLineEdit()
        self.targetCurrency['select'] = QComboBox()
        self.buttonInverter = QPushButton('Inverser devises')

        # Modification  style
        self.currentAmount['input'].setFixedWidth(self.params['layoutWidth'])
        self.currentAmount['select'].setFixedWidth(
            self.params['layoutWidth'])
        self.targetCurrency['input'].setFixedWidth(self.params['layoutWidth'])
        self.targetCurrency['select'].setFixedWidth(self.params['layoutWidth'])
        self.buttonInverter.setFixedWidth(self.params['layoutWidth'])

        style = ''.join(['color:', self.params['uiColor'], ';'])
        self.currentAmount['input'].setStyleSheet(style)
        self.currentAmount['select'].setStyleSheet(style)
        self.targetCurrency['input'].setStyleSheet(style)
        self.targetCurrency['select'].setStyleSheet(style)
        self.buttonInverter.setStyleSheet(style)

        # Add data
        self.currentAmount['select'].addItems(self.currencies)
        self.targetCurrency['select'].addItems(self.currencies)
        self.initCurrencies(
            self.currentAmount['select'], self.currentAmount['code'])
        self.initCurrencies(
            self.targetCurrency['select'], self.targetCurrency['code'])
        self.currentAmount['input'].setText(
            str(self.currentAmount['amount']))
        self.initValues()

        # add event
        self.currentAmount['select'].currentIndexChanged.connect(
            self.onCurrentAmount)
        self.targetCurrency['select'].currentIndexChanged.connect(
            self.onTargetCurrency)
        self.currentAmount['input'].textChanged.connect(
            self.onCurrentAmount)
        self.targetCurrency['input'].textChanged.connect(
            self.onTargetAmount)
        self.buttonInverter.clicked.connect(self.invertActions)

        # add layout on interface
        layout.addWidget(self.currentAmount['select'])
        layout.addWidget(self.currentAmount['input'])
        layout.addWidget(self.targetCurrency['select'])
        layout.addWidget(self.targetCurrency['input'])
        layout.addWidget(self.buttonInverter)
        self.setLayout(layout)

    def currencies(self):
        self.currencies = sorted(self.c.currencies)

    def initCurrencies(self, selec, code):
        index = selec.findText(code, QtCore.Qt.MatchFixedString)
        if index >= 0:
            selec.setCurrentIndex(index)

    def convert(self, amount, currentDevice, targetDevice):
        result = None
        try:
            result = self.c.convert(amount, currentDevice, targetDevice)
        except RateNotFoundError:
            '''
            Devise impossible a convertir
            '''
        return result

    def onChange(self, action, force=False):
        currency1 = self.currentAmount['select'].currentText()
        currency2 = self.targetCurrency['select'].currentText()
        amount1 = self.currentAmount['input'].text()
        amount2 = self.targetCurrency['input'].text()

        if action == 'inverse':
            self.initCurrencies(self.currentAmount['select'], currency2)
            self.initCurrencies(self.targetCurrency['select'], currency1)

        if action == 'update_target' and (force or amount1 != self.currentAmount['amount']):
            if float(amount1) < 0:
                self.targetCurrency['input'].setText(str(''))
                return

            nextValue = self.convert(amount1, currency1, currency2)
            self.currentAmount['amount'] = amount1
            self.targetCurrency['amount'] = nextValue
            self.targetCurrency['input'].setText(str(nextValue))

        if action == 'update_current' and (force or amount2 != self.targetCurrency['amount']):
            nextValue = self.convert(amount2, currency2, currency1)
            self.targetCurrency['amount'] = amount2
            self.currentAmount['amount'] = nextValue
            self.currentAmount['input'].setText(str(nextValue))

    def initValues(self):
        self.onChange('update_target', True)

    def onCurrentAmount(self):
        self.onChange('update_target')

    def onTargetAmount(self):
        self.onChange('update_current')

    def onCurrentAmount(self):
        self.onChange('update_target', True)

    def onTargetCurrency(self):
        self.onChange('update_current', True)

    def invertActions(self):
        self.onChange('inverse')
