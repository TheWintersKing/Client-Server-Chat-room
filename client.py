#Kevin Francis Jose
#1001570348
"""Client Code"""
import sys , time
from PyQt5.QtWidgets import QApplication, QWidget , QLineEdit ,QPushButton , QTextEdit , QDialog
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
import socket
from threading import Thread
from socketserver import ThreadingMixIn
from http_request import HTTP_Request

Quitting = False

#Cal time Difference between messages

def Time_Btw(start , end):
    return end - start

#Build GUI

class Window (QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'GATTALIEFE CHATS'#name of program
        self.left = 50 #starting position
        self.top = 50
        self.width = 500 #size of app
        self.height = 500
        self.start = 0.0 #start time
        self.initUI()

#Create GUI

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('Icon.png'))

#Input TextBox to send message

        self.chatTextField = QLineEdit(self)
        self.chatTextField.resize(480,50)
        self.chatTextField.move(10,400)

#Output TextBox to display recvieed meassge

        self.chatTextField2 = QTextEdit(self)
        self.chatTextField2.resize(480,360)
        self.chatTextField2.move(10,20)
        self.chatTextField2.setReadOnly(True)

#Button to send

        self.btnSend=QPushButton("Send",self)
        self.btnSend.resize(480,30)
        self.btnSend.move(10,460)
        self.btnSend.clicked.connect(self.send)

        self.show()

# Send Data to server inirder to be broadcasted

    def send (self) :
        text = self.chatTextField.text()
        t = Time_Btw(self.start,time.time()) #cal dif btw msg
        self.start = time.time() #set current meassge time

        data = "(" + str(int(t/60)) + ":"+str (int(t%60))+")-" + text

        #send HTTP request for posting Data

        msg = HTTP_Request.encode_HTTP(data ,'POST' , '127.0.0.9',33000,Client)
        Client.send(msg.encode("utf8"))
        self.chatTextField.setText("")
        #if msg == :quit close app
        if text == ':quit':
            Client.close()
            sys.exit()
            Quitting = True

#Class Contain client information for reviecing data on Different thread

class ClientThread(Thread):
    def __init__(self,window):
        Thread.__init__(self)
        self.window=window

#Starts client connects to server and recieves messages in HTTP

    def run(self):

       host = '127.0.0.9' #server ip
       port = 33000 #port number of server
       BUFFER_SIZE = 2048 #buffer size
       global Client

       New_connection = True

       Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket of client

       try:
           Client.connect((host, port)) #connect to server
       except socket.error as e:
           sys.exit() #connection failed
       #loops until program quits and recieve meassage to posted

       while not Quitting:
           if New_connection: #send http request to connect to server
               Client.send (HTTP_Request.encode_HTTP("",'GET',host,port,Client).encode("utf8"))
               New_connection = False
           msg = Client.recv(BUFFER_SIZE).decode()
           text = HTTP_Request.response_decode(msg)
           window.chatTextField2.append(text)


#Program starts here

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    clientThread=ClientThread(window)
    clientThread.start()
    sys.exit(app.exec_())
