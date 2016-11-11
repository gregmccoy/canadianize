from qtgui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from fix_emails.job import Job

class EmailsGUI(Ui_MainWindow):

    def __init__(self):
        print("Running __init__")
        self.filename = ""
        self.outfile = "default.html"
        self.html = ""
        self.job = Job(False)

    def initGUI(self, MainWindow):
        print("Setting up EmailGUI")
        self.window = MainWindow
        self.pushButton.clicked.connect(self.runClicked)
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.setStatusTip('Open File')
        self.actionOpen.triggered.connect(self.fileOpen)
        self.menuFile

    def runClicked(self):
        obj = self.job.html_email(self.filename)
        self.writeOutfile(obj)

        obj = self.job.run_results(self.outfile)
        self.writeResults(obj)

        self.HTMLEdit.appendPlainText(obj.get_content())
        self.webView.setUrl(QtCore.QUrl("file://" + self.outfile))


    def writeOutfile(self, obj):
        with open(self.outfile, 'w+') as o:
            data = obj.get_content()
            o.write(data)

    def writeResults(self, obj):
        html = self.job.html_result(obj)
        if html is not None:
            with open("data/result.html", 'w+') as o:
                o.write(html)


    def fileOpen(self):
        self.filename, _ = QtWidgets.QFileDialog.getOpenFileName(self.window, 'Open File', ".")
        with open(self.filename, 'r+') as f:
            self.html = f.read()
        self.HTMLEdit.appendPlainText(self.html)
        self.webView.setUrl(QtCore.QUrl("file://" + self.filename))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = EmailsGUI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.initGUI(MainWindow)
    sys.exit(app.exec_())
