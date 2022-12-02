import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from routeros_api.exceptions import RouterOsApiCommunicationError
import design
import routeros_api
import pywgkey
from qr_generate import create_conf, show
import json


# connection = routeros_api.RouterOsApiPool(
#     # host=self.lineEditAddress.text(),
#     # username=self.lineEditLogin.text(),
#     # password=self.lineEditPassword.text(),
#     host='192.168.0.49',
#     username='admin',
#     password='pfrhsnj',
#     plaintext_login=True
# )

def add_to_json(comment, private_key):
    json_data = {
        comment: private_key,
    }
    data = json.load(open("client_data.json"))
    data.append(json_data)
    with open("client_data.json", "w") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def read_json(comment):
    with open('client_data.json') as json_file:
        data = json.load(json_file)
        for p in data:
            return p[comment]


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
        self.connButton.clicked.connect(self.connection_click)
        self.pushButton.clicked.connect(self.create)
        self.pushButton_4.clicked.connect(self.show_qr)
        self.pushButton_2.clicked.connect(self.delete_client)

    def connection(self):
        connection = routeros_api.RouterOsApiPool(
            host=self.lineEditAddress.text(),
            username=self.lineEditLogin.text(),
            password=self.lineEditPassword.text(),
            plaintext_login=True
        )
        api = connection.get_api()
        return api

    def connection_click(self):
        try:
            api = MainApp.connection(self)
            self.setWindowTitle("WireGuard client's - CONNECTED")
            self.comboBox.addItems(get_comment(api))
            self.groupBox.setEnabled(True)
            self.groupBox_2.setEnabled(True)
            self.groupBox_3.setEnabled(False)
        except RouterOsApiCommunicationError:
            return

    def create(self):
        try:
            api = MainApp.connection(self)
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
        add_to_json(self.lineEdit_4.text(), client_private_key)
        qr_view = self.QR_view
        scene = QtWidgets.QGraphicsScene(self)
        pixmap = QPixmap('QR.png').scaledToWidth(qr_view.geometry().height() - qr_view.geometry().y())
        scene.addItem(QtWidgets.QGraphicsPixmapItem(pixmap))
        qr_view.setScene(scene)
        self.comboBox.addItem(self.lineEdit_4.text())

    def show_qr(self):
        api = MainApp.connection(self)
        list_get = api.get_resource('/interface/wireguard/peers').get(comment=self.comboBox.currentText())
        client_address = ''.join([str(d['allowed-address']) for d in list_get])
        end_point = "ton.cloudns.nz:12038"
        show(get_server_public_key(api), client_address, read_json(self.comboBox.currentText()), end_point)
        qr_view = self.QR_view
        scene = QtWidgets.QGraphicsScene(self)
        pixmap = QPixmap('QR.png').scaledToWidth(qr_view.geometry().height() - qr_view.geometry().y())
        scene.addItem(QtWidgets.QGraphicsPixmapItem(pixmap))
        qr_view.setScene(scene)

    def delete_client(self):
        api = MainApp.connection(self)
        list_get = api.get_resource('/interface/wireguard/peers')
        get_id = list_get.get(comment=self.comboBox.currentText())[0].get('id')
        list_get.remove(id=get_id)
        index = self.comboBox.findText(self.comboBox.currentText())
        self.comboBox.removeItem(index)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
