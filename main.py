import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from routeros_api.exceptions import RouterOsApiCommunicationError

import design
import routeros_api
import pywgkey
from qr_generate import create_conf , show

connection = routeros_api.RouterOsApiPool(
    host=self.lineEditAddress.text(),
    username=self.lineEditLogin.text(),
    password=self.lineEditPassword.text(),
    plaintext_login=True
)

def get_server_public_key(api):
    return api.get_resource('/interface/wireguard').get(name="wg-in")[0].get('public-key')

def get_comment(api):
    list_comment_get = api.get_resource('/interface/wireguard/peers').get(interface="wg-in")
    return [str(d['comment']) for d in list_comment_get]

def get_max_ip(api):
    list_get = api.get_resource('/interface/wireguard/peers').get(interface="wg-in")
    nums = [str(d['allowed-address']).split('.')[3] for d in list_get]
    max_ip = max([int(str(el[0:el.index('/')])) for el in nums])
    return max_ip + 1


class MainApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connButton.clicked.connect(self.connect)
        self.pushButton.clicked.connect(self.create)
        self.pushButton_4.clicked.connect(self.show_qr)

    def connect(self):
        api = connection.get_api()
        self.setWindowTitle("WireGuard client's - CONNECTED")
        self.comboBox.addItems(get_comment(api))

    def create(self):
        try:
            api = connection.get_api()
        except RouterOsApiCommunicationError:
            return
        # FIXME AAAAAAAAAAAAAAAAAAAAAAAAA
        network = '10.10.10.'
        new_ip = network + str(get_max_ip(api)) + '/32'
        list_address_num = api.get_resource('/interface/wireguard/peers')
        client_key = pywgkey.WgKey()
        client_private_key = f"{client_key.privkey}"
        client_public_key = f"{client_key.pubkey}"
        server_public_key = get_server_public_key(api)
        list_address_num.add(interface='wg-in',
                             comment=f"{self.lineEdit_4.text()}",
                             public_key=client_public_key,
                             allowed_address=new_ip,
                             persistent_keepalive='00:00:20')
        end_point = "ton.cloudns.nz:12038"
        create_conf(server_public_key, new_ip, client_private_key, end_point)

        qr_view = self.QR_view
        scene = QtWidgets.QGraphicsScene(self)
        pixmap = QPixmap('QR.png').scaledToWidth(qr_view.geometry().height() - qr_view.geometry().y())
        scene.addItem(QtWidgets.QGraphicsPixmapItem(pixmap))
        qr_view.setScene(scene)

    def show_qr(self):
        api = connection.get_api()
        # list_get = api.get_resource('/interface/wireguard/peers').get(comment=self.comboBox.currentText())
        # client_address = ''.join([str(d['allowed-address']) for d in list_get])
        # show(get_server_public_key(api), client_address, )

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
