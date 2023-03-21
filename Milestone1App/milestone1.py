import sys

import psycopg2
from PyQt5.QtSql import QSqlQueryModel
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, \
    QTableView
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap, QStandardItemModel

qtCreatorFile = "milestone1App.ui" # Enter file here.
strFromBusiness = " FROM Public." + '"' + "businessMS1" + '"'
strName = '"' + "Name" + '"'
strState = '"' + "State" + '"'
strCity = '"' + "City" + '"'
strDblQt = '"'

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone1(QMainWindow):
    def __init__(self):
        super(milestone1, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.bname.textChanged.connect(self.getBusinessNames)
        self.ui.businesses.itemSelectionChanged.connect(self.displayBusinessCity)

    def executeQuery(self, sql):
        try:
            conn = psycopg2.connect("dbname='Milestone1db' user='postgres' host='localhost' password='admin'")

        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result


    def loadStateList(self):
        self.ui.stateList.clear()
        sql = "SELECT DISTINCT " + strState + strFromBusiness + " ORDER BY " + strState
        print(sql)
        try:
            results = self.executeQuery(sql)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except Exception as e:
                print(e)

        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    def stateChanged(self):
        self.ui.businesses.clear()

        try:
            self.ui.cityList.clear()
        except:
            print("Could not clear cityList")

        state = self.ui.stateList.currentText()

        if (self.ui.stateList.currentIndex() >= 0):
            sql = "SELECT DISTINCT " + strCity + strFromBusiness + " WHERE " + strState + " = '" + state + "' ORDER BY " + strCity
            print(sql)

            try:
                results = self.executeQuery(sql)
                for row in results:
                    self.ui.cityList.addItem(row[0])
                print(results)
            except:
                print("Query failed for getting City")

            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)

            sql = "SELECT " + strName + "," + strCity + "," + strState + strFromBusiness + " WHERE " + strState + " = '" + state + "' ORDER BY " + strName
            print(sql)
            try:
                results = self.executeQuery(sql)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 300)
                self.ui.businessTable.setColumnWidth(1, 100)
                self.ui.businessTable.setColumnWidth(2, 50)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
                    currentRowCount += 1

            except Exception as e:
                print(e)

    def cityChanged(self):
       # if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectItems()) > 0):
        state = self.ui.stateList.currentText()
        city = self.ui.cityList.selectedItems()[0].text()
        sql = "SELECT " + strName + "," + strCity + "," + strState + strFromBusiness + " WHERE " + strState + " = '" + state + "' AND " + strCity + "='" + city + "' ORDER BY " + strName
        print(sql)
        try:
            results = self.executeQuery(sql)
            style = "::section {""background-color: #f3f3f3; }"
            self.ui.businessTable.horizontalHeader().setStyleSheet(style)
            self.ui.businessTable.setColumnCount(len(results[0]))
            self.ui.businessTable.setRowCount(len(results))
            self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State'])
            self.ui.businessTable.resizeColumnsToContents()
            self.ui.businessTable.setColumnWidth(0, 300)
            self.ui.businessTable.setColumnWidth(1, 100)
            self.ui.businessTable.setColumnWidth(2, 50)
            currentRowCount = 0
            for row in results:
                for colCount in range(0, len(results[0])):
                    self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
                currentRowCount += 1

        except Exception as e:
            print(e)

    def getBusinessNames(self):
        self.ui.businesses.clear()
        businessname = self.ui.bname.text()
        sql = "SELECT " + strName + strFromBusiness + " WHERE " + strName + " LIKE '%" + businessname + "%' ORDER BY " + strName
        print(sql)
        try:
            results = self.executeQuery(sql)
            for row in results:
                self.ui.businesses.addItem(row[0])

        except:
             print("Query failed for getting bus")


    def displayBusinessCity(self):
        businessname = self.ui.businesses.selectedItems()[0].text()
        newBusName = businessname.replace("'", "''")
        sql = "SELECT " + strCity + strFromBusiness + " WHERE " + strName + " = '" + newBusName + "'"
        print(sql)
        try:
            results = self.executeQuery(sql)
            self.ui.bcity.setText(results[0][0])

        except:
            print("Query failed for getting bus")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone1()
    window.show()
    sys.exit(app.exec_())