from qtgui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from fix_emails.job import Job
from fix_emails.utils import readConf
import os
import csv

class EmailsGUI(Ui_MainWindow):

    def __init__(self):
        print("Running __init__")
        self.filename = ""
        self.outfile = "default.html"
        self.html = ""
        self.country = readConf("country")
        if not self.country:
            self.country = "CA"
        self.job = Job(False, input_type="qt")
        self.replace_items = self.getReplace("data/replace_{}.csv".format(self.country))


    def initGUI(self, MainWindow):
        print("Setting up EmailGUI")
        self.window = MainWindow
        self.run_button.clicked.connect(self.runClicked)
        self.undo_button.clicked.connect(self.undoClicked)
        self.back_button.clicked.connect(self.webView.back)
        self.update_list_button.clicked.connect(self.updateClicked)
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.setStatusTip('Open File')
        self.actionOpen.triggered.connect(self.fileOpen)
        self.webView.urlChanged.connect(self.updateAddress)
        self.address_bar.returnPressed.connect(self.updateUrl)

        self.replace_list.clear()
        with open("data/replace_{}.csv".format(self.country), 'r') as f:
            self.replace_list.appendPlainText(f.read())

        self.to_select.currentIndexChanged.connect(self.runCountry)

        countries = [ "CA", "US", "GB" ]

        for country in countries:
            self.to_select.addItem(country)

        self.menuFile


    def runCountry(self):
        self.country = self.to_select.currentText()
        self.replace_items = self.getReplace("data/replace_{}.csv".format(self.country))
        self.replace_list.clear()
        with open("data/replace_{}.csv".format(self.country), 'r') as f:
            self.replace_list.appendPlainText(f.read())


    def undoClicked(self):
        self.webView.setUrl(QtCore.QUrl("file://" + self.filename))


    def runClicked(self):
        source = self.source_text.text
        print(self.country)
        obj = self.job.html_email(self.filename, country=self.country)
        self.writeOutfile(obj)

        obj = self.job.run_results(self.outfile)
        self.writeResults(obj)

        self.HTMLEdit.clear()
        self.HTMLEdit.appendPlainText(obj.get_content())
        self.webView.setUrl(QtCore.QUrl("file://" + os.getcwd() + "/" + self.outfile))
        print("Saved to {}".format(self.outfile))
        self.webViewResult.setUrl(QtCore.QUrl("file://" + os.getcwd() + "/data/result.html"))
        self.updateAddress()


    def updateClicked(self):
        text = self.replace_list.toPlainText()
        with open("data/replace_{}.csv".format(self.country), 'w') as w:
            w.write(text)
        QtWidgets.QMessageBox.about(self.window, "Update complete", "Replace List saved")


    def updateAddress(self):
        url = self.webView.url().toString()
        self.address_bar.setText(url)

    def updateUrl(self):
        self.webView.setUrl(QtCore.QUrl(self.address_bar.text()))

    def getReplace(self, list):
        replace_items = []
        with open(list, "r") as f:
            replace_csv = csv.reader(f, delimiter='|')
            for row in replace_csv:
                replace_items.append(row)
        return replace_items


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
        if self.filename:
            with open(self.filename, 'r+') as f:
                self.html = f.read()
            self.HTMLEdit.clear()
            self.HTMLEdit.appendPlainText(self.html)
            self.webView.setUrl(QtCore.QUrl("file://" + self.filename))


class OutLog:
    def __init__(self, edit, out=None, color=None):
        """(edit, out=None, color=None) -> can write stdout, stderr to a
        QTextEdit.
        edit = QTextEdit
        out = alternate stream ( can be the original sys.stdout )
        color = alternate color (i.e. color stderr a different color)
        """
        self.edit = edit
        self.out = None
        self.color = color

    def write(self, m):
        self.edit.insertPlainText(m)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = EmailsGUI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.initGUI(MainWindow)
    sys.stdout = OutLog(ui.output_box, sys.stdout)
    sys.exit(app.exec_())
