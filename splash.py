import sys,os
from PyQt5.QtWidgets import QMainWindow,QApplication,QFrame,QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer,Qt
from PyQt5 import uic

counter=0

style="""

QFrame#back{
    border-radius:20px;
    border-top-right-radius:20px;
    background-image:url(bgdisplay.jpg);
}

"""

class SplashScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitializeUI()

    def InitializeUI(self):
        # self.width,self.height=self.width(),self.height()
        base_path = os.path.abspath(os.path.dirname(__file__))
        uicpath=os.path.join(base_path, "splash.ui")

        uic.loadUi(uicpath,self)

        self.back=self.findChild(QFrame,"background")
        self.moving=self.findChild(QFrame,"moving")
        self.percent=self.findChild(QLabel,"percent")

        desktoprect=QApplication.desktop().availableGeometry(self)
        center=desktoprect.center()

        self.setGeometry(center.x()-(self.width()//2),center.y()-(self.height()//2),700,350)
        self.setWindowTitle("Wordle")
        self.setWindowIcon(QIcon(os.path.join(base_path,"wordle_icon.png")))

        self.timer=QTimer()
        self.timer.timeout.connect(self.changeprogressvalue)
        self.timer.start(75)
        self.value=0

        self.displayWidgets()

        # self.show()

    def displayWidgets(self):
        # self.back.setObjectName("back")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet(style)
        # self.back.set

    def keyPressEvent(self,event):
        key=event.key()
        # print(key)
        if key==16777216:
            self.close()

    def changeprogressvalue(self):

        value=self.value
        if self.value>=100:
            self.timer.stop()
            # self.close()

        txt="""<html><head/><body><p><span style=" color:#ffff00;">{percent}</span><span style=" color:#ffff00; vertical-align:super;">%</span></p></body></html>"""

        finaltxt=txt.replace("{percent}",str(value))
        self.percent.setText(finaltxt)
        self.setprogressvalue(value)

        

        self.value+=4

    def setprogressvalue(self,value):

        stylesheet="""
        QFrame{
            border-radius:150px;
            background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{stop1} rgba(255, 0, 127, 0), stop:{stop2} rgba(255,0,255, 230));
        }
        """

        progress=(100-value)/100

        
        stop1=str(progress-0.001)
        
        stop2=str(progress)

        if(progress-0.001<0):stop1=str(progress)
        # print(value,progress,progress-0.001)

        finalstylesheet=stylesheet.replace("{stop1}",stop1).replace("{stop2}",stop2)

        self.moving.setStyleSheet(finalstylesheet)




if __name__=="__main__":
    app=QApplication(sys.argv)
    window=SplashScreen()
    window.show()
    sys.exit(app.exec_())
