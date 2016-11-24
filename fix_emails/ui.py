from .qt5_ui import Ui_MainWindow

from PyQt5 import QtWebKitWidgets
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

class EmailsGUI(Ui_MainWindow):

    def __init__(self):
        self.pushButton.setObjectName("pushButton")


