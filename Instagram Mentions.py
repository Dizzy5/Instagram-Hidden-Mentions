# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\ELKAR\Documents\UI Designer\Instagram Mentions\Instagram Mentions.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import requests , json , time , re
import resources , DizzyIcon

def get_token():
        url = 'https://www.instagram.com/'
        headers_token = {'X-Instagram-AJAX' : '1' , 'X-Requested-With' : 'XMLHttpRequest'}
        res = requests.get(url, headers = headers_token)
        pattern = r'"csrf_token":"(.*?)"'
        return re.findall(pattern, res.text)[0]

theme = open('Theme.rtf' , 'r').read()
headerss = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'}

class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName("Form")
        # Form.resize(522, 816)
        Form.setFixedSize(522, 816)
        Form.setStyleSheet(theme)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 0, 661, 821))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/Picture.png"))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(170, 410, 191, 31))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(170, 460, 191, 31))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(202, 510, 121, 31))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(170, 360, 191, 31))
        self.lineEdit_3.setInputMask("")
        self.lineEdit_3.setText("")
        self.lineEdit_3.setObjectName("lineEdit_3")


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Get Mentions of Story"))
        Form.setWindowIcon(QIcon(':/Dizzy.png'))
        self.lineEdit.setPlaceholderText(_translate("Form", "Username"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "Password"))
        self.lineEdit_3.setToolTip(_translate("Form", "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">Username Target</span></p></body></html>"))
        self.pushButton.setText(_translate("Form", "Login and parse"))
        self.lineEdit_3.setPlaceholderText(_translate("Form", "Traget"))
        self.lineEdit_2.setEchoMode(QLineEdit.Password)


        self.pushButton.clicked.connect(self.Login)
        time.sleep(1)
        self.pushButton.clicked.disconnect()
        self.pushButton.clicked.connect(self.Get_Mentions_of_story)

    def Login(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        headers = {
                'Host' : 'www.instagram.com',  
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
                'Accept' : '*/*',
                'X-CSRFToken' : get_token(),
                'X-Instagram-AJAX' : '1',
                'Accept-Language' : 'ar,en-US;q=0.7,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                'X-Requested-With' : 'XMLHttpRequest',
                'Connection' : 'keep-alive',
                'Content-Type' : 'application/x-www-form-urlencoded'}

        data = {'enc_password': '#PWD_INSTAGRAM_BROWSER:0:&:' + password , 'username' : username}
        login_url = 'https://www.instagram.com/accounts/login/ajax/'
        login = requests.post(login_url , data=data , headers = headers)
        return login.cookies.get_dict()

    def Get_Mentions_of_story(self):
        global search
        get_user = self.lineEdit_3.text()
        url_for_id = f'https://www.instagram.com/{get_user.strip()}/?__a=1'
        try:
            search = re.search(r'"id":"(.*?)"', requests.get(url_for_id , headers = headerss).text).group(1)
            headers_mention = {
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
                "Accept": "*/*",
                "Accept-Language": "ar,en-US;q=0.7,en;q=0.3",
                "X-CSRFToken": self.Login()['csrftoken'],
                "X-IG-App-ID": "936619743392459",
                "X-IG-WWW-Claim": "hmac.AR1gZPJR6yrLrd7_qHkmhWpCY4fD-i7_7r2GlNOS-szTgMfS",
                "X-Requested-With": "XMLHttpRequest"
            }
            time.sleep(2)
            url_for_story = f'https://www.instagram.com/graphql/query/?query_hash=90709b530ea0969f002c86a89b4f2b8d&variables={{"reel_ids":["{search.strip()}"],"tag_names":[],"location_ids":[],"highlight_reel_ids":[],"precomposed_overlay":false,"show_story_viewer_list":true,"story_viewer_fetch_count":50,"story_viewer_cursor":"","stories_video_dash_manifest":false}}'
            get_info = requests.get(url_for_story , headers = headers_mention , cookies= self.Login())
            informations = get_info.json()['data']['reels_media'][0]['items']
            for story in informations:
                tappable_objects = story['tappable_objects']
                if tappable_objects:
                    for item in tappable_objects:
                        if item['__typename'] == 'GraphTappableMention':
                            users_list.append(item['username'])

            QMessageBox.information(Form ,"Mentions" , str(users_list))

        except:
            QMessageBox.information(Form ,"Somethings Wrong " , 'Please Check Username Target or Username - Password Before Click')

if __name__ == "__main__":
    users_list = []
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    id_to_user = dict()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_()),