import sys

import psycopg2
from PyQt5.QtSql import QSqlQueryModel
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, \
    QTableView
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap, QStandardItemModel

qtCreatorFile = "ProjectApp.ui" # Enter file here.

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
            conn = psycopg2.connect("dbname='YelpDB' user='postgres' host='localhost' password='admin'")

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
        sql = "SELECT DISTINCT State from business ORDER BY state"
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
        print("in stateChanged")
        self.ui.cityList.clear()
        state = self.ui.stateList.currentText()

        self.ui.businesses.clear()
        print("bus cleared")

        if self.ui.stateList.currentIndex() >= 0:
            sql = "SELECT distinct city from business WHERE State = '" + state + "' ORDER BY city;"
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

            sql = "SELECT name, city, state from business WHERE State = '" + state + "' ORDER BY name;"

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
        print("in city changed")
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()

            sql = "SELECT name, city, state from business WHERE State = '" + state + "' and city = '" + city \
                  + "' ORDER BY name;"
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
        sql = "SELECT name FROM  business  WHERE name LIKE '%" + businessname + "%' ORDER BY name"

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
        sql = "SELECT city FROM  business  WHERE name = '" + newBusName + "'"
        #sql = "SELECT " + strCity + strFromBusiness + " WHERE " + strName + " = '" + newBusName + "'"
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