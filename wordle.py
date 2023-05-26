import sys
import os
from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import uic,QtCore
from random import randint

# Get the path to the all_words.txt file in the same directory as the script
base_path = os.path.abspath(os.path.dirname(__file__))
filepath = os.path.join(base_path, "all_words.txt")

# Open the file
words,common_words=[],[]
with open(filepath, "r") as f:  
    words=f.readlines()
f.close()

filepath = os.path.join(base_path, "common_words.txt")
with open(filepath, "r") as f:
    common_words=f.readlines()
f.close()

total_words=len(common_words)-1

class MainWindow(QMainWindow):
    global words,common_words,total_words
    def __init__(self):
        super().__init__()
        uicpath=os.path.join(base_path, "wordle.ui")
        uic.loadUi(uicpath,self)

        desktoprect=QApplication.desktop().availableGeometry(self)
        center=desktoprect.center()

        self.setGeometry(center.x()-(self.width()//2),center.y()-(self.height()//2),580,775)

        self.setWindowTitle("Wordle")

        self.setWindowIcon(QIcon(os.path.join(base_path,"wordle_icon.png")))
            
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


        self.row,self.col=0,0
        self.word=common_words[randint(0,total_words)].strip('\n')
        # self.word="canny"
        # print(self.word)

        self.refreshbtn.clicked.connect(self.refresh_all)
        self.exitbtn.clicked.connect(self.close_app)


    def close_app(self):
        self.close()

    def changetext(self,key):


        if key==16777219:
            if self.col>0:
                self.col-=1
                self.glayout.itemAtPosition(self.row,self.col).widget().setText("")
            return


        if self.col==5:
            # __backspace
            

            # __enter
            if key==16777220:
                output,exists=self.match_guess()
                # print(['No','Yes'][output])

                if not exists:
                    QMessageBox.information(self,"Info","Word not exists!!!")
                    return

                if output:
                    button=QMessageBox.question(self,"Correct Answer","Want to play Again!!!")
                    if button==QMessageBox.Yes:
                        self.refresh_all()
                    else:
                        self.close()
                    return

                if self.row==5:
                    if output:
                        button=QMessageBox.question(self,"Correct Answer","Want to play Again!!!")
                        if button==QMessageBox.Yes:
                            self.refresh_all()
                        else:
                            self.close()

                    else:
                        button=QMessageBox.question(self,"Game Ends","Correct Answer is {} \nWant to play Again!!!".format(self.word))
                        if button==QMessageBox.Yes:
                            self.refresh_all()
                        else:
                            self.close()
                    return 
                self.row+=1
                self.col=0
            return

        if key>=65 and key<=90 and self.row<=5 and self.col<=4:
            self.glayout.itemAtPosition(self.row,self.col).widget().setText(chr(key))
            self.col+=1


    def match_guess(self):
        # return (result,isexists)
        global words
        guess=""
        for i in range(5):
            tmp=self.glayout.itemAtPosition(self.row,i).widget().text()
            guess+=tmp

        # check if guess exists in our words list
        exists=False
        for word in words:
            word=word.strip()
            if guess.lower()==word:
                exists=True
                break
        
        if not exists:
            return (False,False)

         
        count=[0]*27
        colored=[[0 for col in range(5)] for row in range(6)]
        # print(colored)
        for i in range(5):
            count[ord(self.word[i])-97]+=1

        for i in range(5):
            tmp=self.glayout.itemAtPosition(self.row,i).widget().text()
            # print(tmp)
            if tmp.lower()==self.word[i]:
                
                count[ord(tmp.lower())-97]-=1
                self.glayout.itemAtPosition(self.row,i).widget().setStyleSheet("background-color:rgba(0,255,0,210);")
                colored[self.row][i]=1

        for i in range(5):
            tmp=self.glayout.itemAtPosition(self.row,i).widget().text()

            if (tmp.lower() in self.word) and count[ord(tmp.lower())-97]>0:                
                count[ord(tmp.lower())-97]-=1
                if colored[self.row][i]==0:
                    self.glayout.itemAtPosition(self.row,i).widget().setStyleSheet("background-color:yellow;")
                    colored[self.row][i]=1

            elif tmp.lower()!=self.word[i]:
                self.glayout.itemAtPosition(self.row,i).widget().setStyleSheet("background-color:rgba(255,0,0,210);")

        return (guess.lower()==self.word,True)



    
    def keyPressEvent(self,event):
        # super(MainWindow,self).keyPressEvent(event)
        key=event.key()
        self.changetext(key)


    def refresh_all(self):
        self.row,self.col=0,0
        self.word=common_words[randint(0,total_words)].strip('\n')
        # print(self.word)

        for row in range(6):
            for col in range(5):
                self.glayout.itemAtPosition(row,col).widget().setText("")
                self.glayout.itemAtPosition(row,col).widget().setStyleSheet("background-color:rgb(255,255,255);")

        

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    app.exec_()