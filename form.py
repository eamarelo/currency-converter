from currency_converter import RateNotFoundError, CurrencyConverter as CurrencyConverter_
from PySide2 import QtCore
from PySide2.QtWidgets import QDialog, QLineEdit, QPushButton, QHBoxLayout, QComboBox


class Convert():
    def __init__(self, parent=None):
        super(Convert, self).__init__(parent)
        self.currencies()
    
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
        amount1 = parseToFloat(amount1, -1)
        amount2 = parseToFloat(amount2, -1)

        if action == 'inverse':
            self.initCurrencies(self.currentAmount['select'], currency2)
            self.initCurrencies(self.targetCurrency['select'], currency1)

        if action == 'update_target' and (force or amount1 != parseToFloat(self.currentAmount['amount'])):
            if amount1 < 0:
                self.targetCurrency['input'].setText(str(''))
                return

            nextValue = parseToFloat(
                self.convert(amount1, currency1, currency2))
            self.currentAmount['amount'] = amount1
            self.targetCurrency['amount'] = nextValue
            self.targetCurrency['input'].setText(str(nextValue))

        if action == 'update_current' and (force or amount2 != parseToFloat(self.targetCurrency['amount'])):
            if amount2 < 0:
                self.currentAmount['input'].setText(str(''))
                return

            nextValue = parseToFloat(
                self.convert(amount2, currency2, currency1))
            self.targetCurrency['amount'] = amount2
            self.currentAmount['amount'] = nextValue
            self.currentAmount['input'].setText(str(nextValue))

    def initDefaultValues(self):
        self.onChange('update_target', True)

    def onCurrentAmountChange(self):
        self.onChange('update_target')

    def onTargetAmountChange(self):
        self.onChange('update_current')

    def oncurrentAmountChange(self):
        self.onChange('update_target', True)

    def onTargetCurrencyChange(self):
        self.onChange('update_current', True)

    def onClickInverter(self):
        self.onChange('inverse')
