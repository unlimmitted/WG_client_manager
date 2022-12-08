import subprocess
import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from routeros_api.exceptions import RouterOsApiCommunicationError
import design
import routeros_api
import pywgkey
from qr_generate import create_conf, show
import json
import sdesign
import os

def get_interface_from_settings():
    with open('settings.json') as settings:
        data = json.load(settings)
        for p in data['settings']:
            interface = p['Interface']
        return interface
def get_server_public_key(api):
    return api.get_resource('/interface/wireguard').get(name="wg-in")[0].get('public-key')


def get_comment(api):
    list_comment_get = api.get_resource('/interface/wireguard/peers').get(interface=get_interface_from_settings())
    return [str(d['comment']) for d in list_comment_get]


def get_max_ip(api):
    list_get = api.get_resource('/interface/wireguard/peers').get(interface=get_interface_from_settings())
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
        self.settings_button.clicked.connect(self.show_settings)
        self.pushButton_3.clicked.connect(self.openExplorer)

    def connection(self):
        with open('settings.json') as json_file:
            data = json.load(json_file)
            for p in data['settings']:
                address = p['address']
                login = p['login']
                password = p['password']
        connection = routeros_api.RouterOsApiPool(
            host=address,
            username=login,
            password=password,
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
            self.connButton.setEnabled(False)
            self.label_3.setText('Connected')
        except RouterOsApiCommunicationError:
            self.label_3.setText('Incorrect data')

    def create(self):
        api = MainApp.connection(self)
        with open('settings.json') as json_file:
            data = json.load(json_file)
            for p in data['settings']:
                network = p['network']
        formating_network = (network.split('/')[0])[:-1]
        new_ip = formating_network + str(get_max_ip(api)) + '/' + (network.split('/'))[1]
        list_address_num = api.get_resource('/interface/wireguard/peers')
        client_key = pywgkey.WgKey()
        client_private_key = f"{client_key.privkey}"
        client_public_key = f"{client_key.pubkey}"
        server_public_key = get_server_public_key(api)
        if self.lineEdit_4.text():
            get_client_name = api.get_resource('/interface/wireguard/peers').get(comment=self.lineEdit_4.text())
            if get_client_name:
                self.label_3.setText('Client name\n already exists')
            else:
                list_address_num.add(interface=get_interface_from_settings(),
                                     comment=f"{self.lineEdit_4.text()}",
                                     public_key=client_public_key,
                                     allowed_address=new_ip,
                                     persistent_keepalive='00:00:20')
                with open('settings.json') as settings:
                    data = json.load(settings)
                    for p in data['settings']:
                        end_point = p['end_point']
                        dns = p['DNS']
                        mtu = p['MTU']
                create_conf(server_public_key, new_ip, client_private_key, end_point, dns, mtu, self.lineEdit_4.text())
                qr_view = self.QR_view
                scene = QtWidgets.QGraphicsScene(self)
                pixmap = QPixmap('QR.png').scaledToWidth(qr_view.geometry().height() - qr_view.geometry().y())
                scene.addItem(QtWidgets.QGraphicsPixmapItem(pixmap))
                qr_view.setScene(scene)
                self.comboBox.addItem(self.lineEdit_4.text())
                self.label_3.setText('Client created')
        else:
            self.label_3.setText('Client field \n is empty')

    def show_qr(self):
        show(self.comboBox.currentText())
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
        config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   f'configs/{self.comboBox.currentText()}.conf')
        os.remove(config_path)
        self.comboBox.removeItem(index)

    def show_settings(self):
        self.settings = Settings_()
        self.settings.show()

    def openExplorer(self):
        subprocess.Popen(rf'explorer /select,"{os.getcwd()}\configs\{self.comboBox.currentText()}.conf"')


class Settings_(QtWidgets.QMainWindow, sdesign.Ui_Settings_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.save_button.clicked.connect(self.saveSettings)
        with open('settings.json') as settings:
            data = json.load(settings)
            for p in data['settings']:
                self.end_point_line.setText(p['end_point'])
                self.network_line.setText(p['network'])
                self.mtu_line.setText(p['MTU'])
                self.dns_line.setText(p['DNS'])
                self.inteface_line.setText(p['Interface'])
                self.Address_Edit_Line.setText(p['address'])
                self.Login_Edit_Line.setText(p['login'])
                self.Password_Edit_Line.setText(p['password'])

    def saveSettings(self):
        data = {}
        data['settings'] = []
        data['settings'].append({
            'end_point': self.end_point_line.text(),
            'network': self.network_line.text(),
            'MTU': self.mtu_line.text(),
            'DNS': self.dns_line.text(),
            'Interface': self.inteface_line.text(),
            'address': self.Address_Edit_Line.text(),
            'login': self.Login_Edit_Line.text(),
            'password': self.Password_Edit_Line.text()
        })
        with open('settings.json', 'w') as outfile:
            json.dump(data, outfile, indent=2)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_(app.exec())


if __name__ == '__main__':
    main()
