import sys, time, csv, os, re, psutil
from datetime import datetime
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QMessageBox

qtCreatorFile = "mainWindow.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.button_start.clicked.connect(self.mainFunction)
        self.button_add.clicked.connect(self.addProgramsToBlockList)
        self.button_clearList.clicked.connect(self.clearList)
        self.button_removePrograms.clicked.connect(self.removeItem)
        self.loadBlockedList()

    def mainFunction(self):
        self.startTime = time.time()
        self.workingHours = int(self.hours.text())
        self.workingMinutes = int(self.minutes.text())
        self.workingSeconds = self.workingMinutes * 60 + self.workingHours * 3600
        print(self.startTime, self.workingSeconds)
        self.close()
        while not self.checkTime():
            self.load_csv_data()
        if self.checkTime():
            sys.exit()

    def removeItem(self):
        item = self.blockedProgramsList.takeItem(self.blockedProgramsList.currentRow())
        item = None
        items = []
        for index in range(self.blockedProgramsList.count()):
            items.append(self.blockedProgramsList.item(index))
        with open('blockedPrograms.csv', 'w+', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter='?')
            for i in items:
                writer.writerow([i])

    def clearList(self):
        listClear = QMessageBox.question(self, "Clear List", "Are you sure you want to clear the block list?")
        if listClear == QMessageBox.Yes:
            self.blockedProgramsList.clear()
            with open('blockedPrograms.csv', 'w+', newline='') as csvfile:
                csvfile.truncate()
        elif listClear == QMessageBox.No:
            pass

    def loadBlockedList(self):
        self.blockedProgramsList.clear()
        with open('blockedPrograms.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter='?', quotechar='|')
            for list in reader:
                for item in list:
                    self.blockedProgramsList.addItem(item)

    def checkTime(self):
        if time.time() > self.startTime+self.workingSeconds:
            return True
        return False

    def stringCheck(self):
        if not len(self.fileName) <= 0:
            return True
        return False

    def addProgramsToBlockList(self):
        #kad se klikne, dodaj izabrane .exe fajlove na QList - Uradjeno
        self.fileName = QFileDialog().getOpenFileName(self, 'Add Program to block list', 'c:\\', "Exe files (*.exe)")
        self.fileName = self.fileName[0] #getting first value in fileName tuple
        self.fileName = self.fileName.split('/') #spliting it on each slash so I can easly take the file name out
        self.fileName = self.fileName[-1]
        print(self.fileName) #making sure everything works fine (It does!! :D)
        with open('blockedPrograms.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter='?')
            if self.stringCheck():
                writer.writerow([self.fileName])
        self.loadBlockedList()

    def load_csv_data(self):
        self.programsToKill = []
        with open('blockedPrograms.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for y in reader:
                for x in y:
                    self.programsToKill.append(x)
        self.kill_process()

    def kill_process(self):
        for self.name in self.programsToKill:
            for proc in psutil.process_iter():
                if proc.name() == self.name:
                    if self.check_process_exist_by_name():
                        proc.kill()

    def check_process_exist_by_name(self):
        for proc in psutil.process_iter():
            if proc.name() == self.name:
                return True
        return False

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
