import sys

import psycopg2
from PyQt5.QtSql import QSqlQueryModel
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, \
    QTableView, QPushButton
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
        self.ui.zipcodeList.itemSelectionChanged.connect(self.zipcodeChanged)
        self.ui.busSearchButton.clicked.connect(self.busSearchButtonClicked)
        self.ui.clearButton.clicked.connect(self.clearButtonClicked)

    def busSearchButtonClicked(self):
        self.getBusinessData()

    def clearButtonClicked(self):
        for i in reversed(range(self.ui.businessTable.rowCount())):
            self.ui.businessTable.removeRow(i)

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

    def executeQuerySingleValue(self, sql):
        try:
            conn = psycopg2.connect("dbname='YelpDB' user='postgres' host='localhost' password='admin'")

        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        result = cur.fetchone()
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
        self.ui.cityList.clear()
        state = self.ui.stateList.currentText()
        self.ui.businessTable.clear()
        self.ui.zipcodeList.clear()

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

    def cityChanged(self):
        print("in city changed")
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            self.ui.zipcodeList.clear()

            # Get Zipcode list
            sql = "SELECT DISTINCT postalCode from business WHERE State = '" + state + "' and city = '" + city \
                    + "' ORDER BY postalCode;"

            print(sql)

            try:
                results = self.executeQuery(sql)
                for row in results:
                    self.ui.zipcodeList.addItem(row[0])
                print(results)
            except:
                print("Query failed for getting City")

            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)

    def zipcodeChanged(self):
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) \
                and (len(self.ui.zipcodeList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.zipcodeList.selectedItems()[0].text()
            self.ui.numBusinesses.clear()
            self.ui.totalPopulation.clear()
            self.ui.averageIncome.clear()
            self.ui.topCategoriesList.clear()
            self.ui.businessTable.clear()
            self.ui.categoryList.clear()

            # Get numBusinesses
            sql = "SELECT COUNT(*) " \
                  "from business WHERE State = '" + state + "' and city = '" + city \
                  + "' and postalCode = '" + zipcode + "'"
            print(sql)
            try:
                results = self.executeQuerySingleValue(sql)
                self.ui.numBusinesses.setPlainText(str(results[0]))

            except Exception as e:
                print(e)

            # Get total population
            sql = "SELECT distinct p.population from postalcode p " \
                  "JOIN business b on b.postalcode = p.postalcode " \
                  "WHERE b.State = '" + state + "' and b.city = '" + city \
                  + "' and b.postalCode = '" + zipcode + "'"

            print(sql)
            try:
                results = self.executeQuerySingleValue(sql)
                self.ui.totalPopulation.setPlainText(str(results[0]))

            except Exception as e:
                print(e)

            # Get averageIncome (aka mean)
            sql = "SELECT distinct p.meanincome from postalcode p " \
                  "JOIN business b on b.postalcode = p.postalcode " \
                  "WHERE b.State = '" + state + "' and b.city = '" + city \
                  + "' and b.postalCode = '" + zipcode + "'"

            print(sql)
            try:
                results = self.executeQuerySingleValue(sql)
                self.ui.averageIncome.setPlainText(str(results[0]))

            except Exception as e:
                print(e)

            # Get top categories
            sql = "SELECT COUNT(*), c.categoryName from category c " \
                  "JOIN BusinessCategory bc on bc.categoryId = c.categoryId " \
                  "JOIN business b on b.businessId = bc.businessId " \
                  "WHERE b.State = '" + state + "' and b.city = '" + city \
                  + "' and b.postalCode = '" + zipcode + "'" \
                  + "GROUP BY c.categoryName"

            print(sql)
            try:
                results = self.executeQuery(sql)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.topCategoriesList.horizontalHeader().setStyleSheet(style)
                self.ui.topCategoriesList.setColumnCount(len(results[0]))
                self.ui.topCategoriesList.setRowCount(len(results))
                self.ui.topCategoriesList.setHorizontalHeaderLabels(['# of Business', 'Category'])
                self.ui.topCategoriesList.resizeColumnsToContents()
                self.ui.topCategoriesList.setColumnWidth(0, 100)
                self.ui.topCategoriesList.setColumnWidth(1, 30)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.topCategoriesList.setItem(currentRowCount, colCount,
                                                          QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1

            except Exception as e:
                print(e)

            # Get categories list
            sql = "SELECT DISTINCT c.categoryName from category c " \
                  "JOIN BusinessCategory bc on bc.categoryId = c.categoryId " \
                  "JOIN business b on b.businessId = bc.businessId " \
                  "WHERE b.State = '" + state + "' and b.city = '" + city \
                  + "' and b.postalCode = '" + zipcode + "'"

            print(sql)

            try:
                results = self.executeQuery(sql)
                for row in results:
                    self.ui.categoryList.addItem(row[0])
                print(results)
            except:
                print("Query failed for getting CategoryList")
                print(e)

    def getBusinessData(self):
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) \
                and (len(self.ui.zipcodeList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.zipcodeList.selectedItems()[0].text()
            categoryname = ""

            if (len(self.ui.categoryList.selectedItems()) > 0) :
                categoryname = self.ui.categoryList.selectedItems()[0].text()

            sql = "SELECT DISTINCT name, address, city, stars, reviewCount, ReviewRating, numCheckins " \
                  " FROM business b " \
                  " JOIN BusinessCategory bc on bc.businessId = b.businessId " \
                  " JOIN Category c on c.categoryId = bc.categoryId " \
                  " WHERE State = '" + state + "' and city = '" + city + "'" \
                  " AND postalCode = '" + zipcode + "'" \

            if categoryname != "":
                sql += " AND c.categoryName = '" + categoryname + "'"

                sql += " ORDER BY name;"

            print(sql)

            try:
                results = self.executeQuery(sql)
                style = "::section {""background-color: #f3f3f3; height:50px; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars',
                                                                 'Review Count', 'Review Rating', '# of Checkins'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 220)
                self.ui.businessTable.setColumnWidth(1, 150)
                self.ui.businessTable.setColumnWidth(2, 100)
                self.ui.businessTable.setColumnWidth(3, 50)
                self.ui.businessTable.setColumnWidth(4, 80)
                self.ui.businessTable.setColumnWidth(5, 80)
                self.ui.businessTable.setColumnWidth(6, 60)

                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1

            except Exception as e:
                print(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone1()
    window.show()
    sys.exit(app.exec_())
