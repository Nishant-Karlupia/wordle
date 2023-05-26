import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, QCoreApplication

from splash import SplashScreen
from wordle import MainWindow

# base_path = os.path.abspath(os.path.dirname(__file__))

try:
  from ctypes import windll
  myappid = "soundwave.wordle.1.0"
  windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
  pass

def run_app1():
    if not QCoreApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QCoreApplication.instance()

    splash = SplashScreen()
    splash.show()

    # Schedule the closeSplashScreen function to be called after 5 seconds
    QTimer.singleShot(2300, lambda: closeSplashScreen(app, splash))

    app.exec_()

def closeSplashScreen(app, splash):
    # Close the splash screen and open the main window
    splash.close()
    window = MainWindow()
    window.show()

def run_app2():
    # print("Running app2")
    if not QCoreApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QCoreApplication.instance()

    window = MainWindow()
    window.show()

    app.exec_()

if __name__ == '__main__':
    # print("Starting app1")
    run_app1()

    # print("Starting app2")
    run_app2()

    # print("Script execution complete")
