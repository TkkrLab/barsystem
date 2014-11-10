#!/usr/bin/python2

from __future__ import print_function
from __future__ import unicode_literals

VERSION = '2.0'

import csv
import sys
from PyQt4 import QtCore, QtGui, uic

import pprint
pp = pprint.PrettyPrinter(indent=4)

class ClickyButton(QtGui.QPushButton):
    def __init__(self, parent, id, text, position):
        super(ClickyButton, self).__init__(text, parent)
        self.id = id
        self.move(*position)
        self.resize(160, 80)

class Database(dict):
    def __init__(self, filename, filter=None):
        r = csv.DictReader(open(filename, 'r'))
        for line in r:
            line['id'] = int(line['id'])
            if filter:
                if 'whitelist' in filter:
                    refuse = False
                    for k, v in filter['whitelist'].iteritems():
                        if not line[k] in v:
                            refuse = True
                            break
                    if refuse:
                        continue
                if 'convert' in filter:
                    for k, v in filter['convert'].iteritems():
                        if k in line:
                            line[k] = v(line[k])
            self[line['id']] = line
class UserDatabase(Database):
    def __init__(self):
        super(UserDatabase, self).__init__('2014-11/currentPerson.csv', filter={
            'convert':{'token': int, 'amount': float},
            'whitelist':{'type': ['active','attendant', 'admin','special']}
        })
    def find_token(self, token):
        for user in self.itervalues():
            if user['token'] == token:
                return user
class Product(dict):
    def getPrice(self, user):
        if user['id'] == 0:
            return self['cash_price']
        return self['person_price']
class ProductDatabase(Database):
    def __init__(self):
        super(ProductDatabase, self).__init__('2014-11/currentProduct.csv', filter={
            'convert':{'cash_price': float, 'stock_value': float, 'person_price': float, 'sort': int, 'items': int},
            'whitelist':{'type': ['normal']}
        })
        for product in self:
            self[product] = Product(self[product])
    def find_barcode(self, barcode):
        for product in self.itervalues():
            if product['barcode'] == barcode:
                return product

class ProductButton(QtGui.QPushButton):
    WIDTH = 120
    HEIGHT = 80
    def __init__(self, product, parent, system):
        self.product = product
        super(ProductButton, self).__init__(self.product['name'], parent)
        self.resize(self.WIDTH, self.HEIGHT)
        self.setStyleSheet('font-size: 13pt')
        self.clicked.connect(lambda: self.system.product_clicked.emit(self.product['id']))
        self.system = system
    def reset(self, user):
        self.user = user
        self.updateText(user)
    def updateText(self, user):
       self.setText('{0}\n\u20AC{1:0.2f}'.format(self.product['name'], self.product.getPrice(user)))

class QueueWidget(QtGui.QStandardItem):
    def __init__(self, product):
        super(QueueWidget, self).__init__()
        self.product = product
        self.product_id = product['id']
        self.count = 0
        self.setSizeHint(QtCore.QSize(0, 30))

    def add(self):
        self.count += 1
    def getTotal(self, user):
        return self.product.getPrice(user) * self.count
    def update(self, user):
        self.setText('{1} x {0}: \u20AC{2:0.2f}'.format(self.product['name'], self.count, self.getTotal(user)))

class BarSystem(QtGui.QMainWindow):

    ibutton_scanned = QtCore.pyqtSignal(int)
    barcode_scanned = QtCore.pyqtSignal('QString')
    product_clicked = QtCore.pyqtSignal(int)

    def __init__(self):
        super(BarSystem, self).__init__()
        self.initUI()
        self.users = UserDatabase()
        self.products = ProductDatabase()
        # pp.pprint(self.users)
        # pp.pprint(self.products)

        self.currentUser = None

        self.ibutton_scanned.connect(self.processIbutton)
        self.barcode_scanned.connect(self.processBarcode)
        self.product_clicked.connect(self.onProductClicked)

        self.productQueue = QtGui.QStandardItemModel()
        self.lstProductQueue.setModel(self.productQueue)

        try:
            self.serial = SerialMonitor(self)
            self.serial.start()
        except Exception as err:
            print(err)
            self.serial = None

    def closeEvent(self, evnt):
        pass

    def processIbutton(self, ibutton):
        print('iButton: {}'.format(ibutton))
        user = self.users.find_token(ibutton)
        if user:
            print('User: {}'.format(user))
            if user['type'] in ('attendant', 'active', 'admin'):
                self.currentUser = user
                self.stack.setCurrentWidget(self.windowOrder)
        else:
            print('User not found')
    def processBarcode(self, barcode):
        print('Barcode: {}'.format(barcode))
        product = self.products.find_barcode(barcode)
        if product:
            print('Product: {}'.format(product))
        else:
            print('Product not found')

    def onProductClicked(self, product_id):
        # print('Product: {}'.format(product_id))
        if product_id in self.products:
            product = self.products[product_id]
            i = 0
            item = None
            while self.productQueue.item(i):
                if self.productQueue.item(i).product_id == product_id:
                    item = self.productQueue.item(i)
                    break
                i += 1
            if not item:
                item = QueueWidget(product)
                self.productQueue.appendRow(item)
            item.add()
            item.update(self.currentUser)

    def initUI(self):
        uic.loadUi('window.ui', self)
        self.stack.setCurrentWidget(self.windowWelcome)
        self.stack.currentChanged.connect(self.stackCurrentChanged)
        self.lblVersionCode.setText('Version: {}'.format(VERSION))
        self.lblImage.setPixmap(QtGui.QPixmap("Frontpage_combine.png"))
        for objname in [ objname for objname in dir(self) if 
            objname.startswith('btn') and hasattr(self, objname + 'Clicked') ]:
            getattr(self, objname).clicked.connect(getattr(self, objname + 'Clicked'))
        self.show()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.ActivationChange:
            pass # TODO: reset program to default state

    def stackCurrentChanged(self, id):
        curr = self.stack.currentWidget()
        if curr == self.windowWelcome:
            self.currentUser = None
        elif curr == self.windowOrder:
            if len(self.productFrame.children()) == 0:
                x = y = 0
                max_x = self.productFrame.width() // ProductButton.WIDTH
                for product in self.products.itervalues():
                    btn = ProductButton(product, self.productFrame, self)
                    btn.move(x * ProductButton.WIDTH, y * ProductButton.HEIGHT)
                    btn.show()
                    x += 1
                    if x >= max_x:
                        x = 0
                        y += 1
            for child in self.productFrame.children():
                child.reset(self.currentUser)

    # windowWelcome
    def btnCashOrderClicked(self):
        self.currentUser = self.users[0]
        self.stack.setCurrentWidget(self.windowOrder)
    def btnMinimizeClicked(self):
        self.setWindowState(QtCore.Qt.WindowMinimized)
        self.setWindowState(QtCore.Qt.WindowNoState)
    # windowOrder
    def btnPlaceOrderClicked(self):
        pass
    def btnCancelOrderClicked(self):
        self.productQueue.clear()
        self.stack.setCurrentWidget(self.windowWelcome)

import serial
import serial.tools.list_ports
import select
import time

class SerialMonitor(QtCore.QThread):
    def __init__(self, window, parent=None):
        super(SerialMonitor, self).__init__(parent)
        self.exiting = False

        self.window = window
        self.buffer = ''
        self.port = '/dev/ttyUSB0'
        self.serial = None
        self.reconnect()

    def __del__(self):
        self.exiting = True
        self.wait()

    def reconnect(self):
        try:
            self.serial.close()
        except:
            pass
        try:
            self.serial = serial.Serial(self.port, 19200, timeout = 0)
        except Exception as e:
            # print('Error in port {}: {}'.format(self.port, e))
            ports = list(serial.tools.list_ports.grep('ttyUSB'))
            curr_id = -1
            if len(ports) > 0:
                for i in range(len(ports)):
                    if ports[i][0] == self.port:
                        curr_id = i
                if curr_id >= 0:
                    curr_id += 1
                else:
                    curr_id = 0
                if curr_id >= len(ports):
                    curr_id = 0
                self.port = ports[i][0]
                # print('Changing port to {}'.format(self.port))
            else:
                pass
                # print('No ports found!')
        
    def processInput(self, data):
        data = data.strip()
        if len(data) == 0:
            return
        if data[0] == 'i' and data [-1] == 'b':
            ibutton = int(data[1:-1])
            self.window.ibutton_scanned.emit(ibutton)
        elif len(data) > 8: # probably barcode?
            barcode = data
            self.window.barcode_scanned.emit(barcode)
        else:
            print('Unknown data: {}'.format(data))

    def run( self ):
        # print('running')
        while not self.exiting:
            try:
                r, w, e = select.select([self.serial],[],[], 1)
                if len(r) > 0:
                    self.buffer += self.serial.read()
                    if self.buffer.endswith('\n'):
                        self.processInput(self.buffer)
                        self.buffer = ''
            except:
                time.sleep(2)
                self.reconnect()
        # print('stopping')
        if self.serial:
            self.serial.close()

def main():
    app = QtGui.QApplication(sys.argv)
    window = BarSystem()
    # window.showFullScreen() # THIS NEEDS TO GO ON WHEN IT'S DONE
    window.center() # ONLY FOR TESTING
    window.btnCashOrderClicked() # SEE PREVIOUS LINE
    # window.btnMinimizeClicked() # ALSO ONLY FOR TESTING (serial to be specific)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()