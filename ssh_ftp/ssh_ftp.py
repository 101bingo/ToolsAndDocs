# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import re
import sys
import time
import paramiko

from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot,Qt
from PyQt5.QtWidgets import QMainWindow,QApplication,QKeyEventTransition,QTextEdit

from Ui_ssh_ftp import Ui_MainWindow

COLOR = {
    '[0m'        :'none',
    '[01;33m'    :'yellow',
    '[00;37m'    :'LightGray',
    '[01;35m'    :'MediumPurple',
    '[01;37m'    :'white',
    '[01;36m'    :'LightCyan',
    '[00;34m'    :'blue',
    '[01;30m'    :'DarkGray',
    '[00;35m'    :'purple',
    '[00;36m'    :'cyan',
    '[01;31m'    :'DarkRed',
    '[01;32m'    :'LightSeaGreen',
    '[01;34m'    :'LightBlue',
    '[00;31m'    :'red',
    '[00;33m'    :'brown',
    '[00;30m'    :'black',
    '[00;32m'    :'green',
}

def show_msg(clr, msg_info):
    msg = "<b><font color='{}'>{}</font></b>".format(clr, msg_info)
    return msg
    pass

class myTextEdit(QTextEdit):
    def __init__(self,parent):
        QTextEdit.__init__(self)
        self.parent=parent
    def keyPressEvent(self, event):
        QTextEdit.keyPressEvent(self,event)
        print('press')
        if event.key() == Qt.Key_Return:
            print('success')
            self.parent.dealMessage()

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.cmd_finish = False
        self.connected()
        self.sendcmd('ls')

        # self.testcmd()
        # self.textEdit.setText("<b><font color='LightBlue'>hello world</font></b>")
        # self.textEdit.setText('1231231231232131231adsfbcdwefasdfas')
        # self.textEdit.insertHtml("anaconda-ks.cfg  mirrored-files  <b><font color='red'>nginx-1.9.9 &nbsp;&nbsp;</font></b>  [01;31mnginx-1.9.9.tar.gz")

    @pyqtSlot()
    def on_textEdit_textChanged(self):
        # self.textEdit.returnPressed.connect(self.test)
        if self.textEdit.toPlainText().endswith('\n') and not self.cmd_finish:
            print(111111111111)
            self.cmd_finish = True
            cursor = self.textEdit.textCursor()
            cursor.movePosition(QtGui.QTextCursor.End)
            self.textEdit.setTextCursor(cursor)
            msg_block_num = self.textEdit.textCursor().blockNumber()
            msg = self.textEdit.document().findBlockByLineNumber(msg_block_num-1).text()
            msg = msg.split(']#')[-1]
            # msg = re.search(']# (.*)', msg).group(1) #匹配命令行
            self.sendcmd(msg.strip())
        if self.textEdit.toPlainText().endswith('#'):
            print(333333333333333)
            # self.textEdit.append('#')

    def connected(self):
        HOST = '20.100.101.2'
        PORT = 22
        USERNAME = 'root'
        PASSWORD = 'root'
        self.ssh = paramiko.Transport((HOST, PORT))
        self.ssh.start_client()
        self.ssh.auth_password(USERNAME, PASSWORD) #
        self.channel = self.ssh.open_session()
        self.channel.settimeout(65535)
        self.channel.get_pty() #获取终端
        self.channel.invoke_shell()
        pass

    def sendcmd(self, str_c):
        final_res = ''
        cmd = '{}\n'.format(str_c)
        self.channel.send(cmd)
        while True:
            time.sleep(0.2)
            data = self.channel.recv(1024)
            print(data)
            data = data.replace(b'\x1b', b'')
            data = data.decode('utf-8')
            if data.endswith(']# '):
                break
            pass
        self.cmd_finish = True
        
        res = data.split('[0m')
        print(res)
        data = re.sub('[\r\n]', '<br>', data)
        for info in res:
            
            info = re.sub('[\r\n]', '<br>', info)
            info = info.strip()
            if info.startswith('[0'):
                ms_color = info[:7]
                ms_color = COLOR[ms_color]
                re_info = info[7:] + '&nbsp;&nbsp;'
                info = show_msg(ms_color, re_info)
            final_res += info
        print('final_res:', final_res)
        self.textEdit.insertHtml(final_res)
        self.cmd_finish = False

        pass

    @pyqtSlot()
    def on_pushButton_clicked(self):
        msg = self.textEdit.textCursor().block().text()
        print(msg)

    # def keyReleaseEvent(self, event):
    #     # QTextEdit.keyPressEvent(self,event)
    #     print('press')
    #     # print(dir(Qt))
    #     if event.key() == Qt.Key_Return:
    #         print('success')
    #         self.parent.dealMessage()
        # if event.key() == Qt.Key_Backspace:
        #     print(2222222222222)
        #     if self.textEdit.toPlainText().endswith('#'):
        #         print(333333333333333)
        #         self.textEdit.insertPlainText('#')

    # def keyPressEvent(self, QKeyEvent):  # 键盘某个键被按下时调用
    #     #参数1  控件
    #     print(111111111111111)
    #     key = QKeyEvent.key()
    #     print(key)
    #     if QKeyEvent.key()== Qt.Key_A:  #判断是否按下了A键
    #         #key()  是普通键
    #         print('按下了A键')

    #     if QKeyEvent.modifiers()==Qt.ControlModifier and QKeyEvent.key()== Qt.Key_A:#两键组合
    #         #modifiers()   判断修饰键
    #         #Qt.NoModifier   没有修饰键
    #         #Qt.ShiftModifier    Shift键被按下
    #         #Qt.ControlModifier    Ctrl键被按下
    #         #Qt.AltModifier      Alt键被按下
    #         print('按下了Ctrl-A键')

    #     if QKeyEvent.modifiers() == Qt.ControlModifier|Qt.ShiftModifier and QKeyEvent.key() == Qt.Key_A:  # 三键组合
    #         print('按下了Ctrl+Shift+A键')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pytest = MainWindow()
    pytest.show()
    sys.exit(app.exec())
    
    
