
# Mitchell Kolb -- CPTS 451 -- Milestone Project
# I used these libraries for this project so far
# pip3 install pyqt6
# pip3 install pyqt6-tools

# To run the pyqt6 designer program use this command in the terminal -- pyqt6-tools designer


import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt6 import uic, QtCore
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtCore import QTimer
import psycopg2
import random, time, asyncio

qtCreatorFile = "milestone1App.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone1(QMainWindow):
    def __init__(self):
        super(milestone1, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.displayAll()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged) #has the box update on the contigency when the user picks an options
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged) #connects right box on page1 
        self.ui.bname.textChanged.connect(self.getBusinessNames) #connects the page2 top bname box
        self.ui.businesses.itemSelectionChanged.connect(self.displayBusinessCity) #connects right box on page1 
        self.ui.refresh.clicked.connect(self.otherTable1)
        self.ui.refresh.clicked.connect(self.otherTable2)


    def executeQuery(self,sql_str):
        """ try:
            conn = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='s'")
        except:
            print('Unable to connect to database')
         """
        try:
            conn = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='s' port='1234'")
        except psycopg2.Error as e:
            error_msg = f"Unable to connect to the database. Error: {e}"
            print(error_msg)
            return None
        
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result

    def loadStateList(self):
        self.ui.stateList.clear() #clears everything from the combo box then adds the db info 
        sql_str = "SELECT distinct state FROM business ORDER BY state;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print("Query Failed")

        self.ui.stateList.setCurrentIndex(-1) #anytihng positive pre-sets the box to have one of the items selected
        self.ui.stateList.clearEditText() #clears the text

    def displayAll(self):
        categories = "SELECT u.userID, u.username, u.income, r.date_, r.reviewScore, r.starRating, r.content_of_review FROM Users u LEFT JOIN Review r ON u.userID = r.userID LIMIT 10;"

        for row in categories:
            self.ui.categoryList.addItem(row[0])
        
        zipcodes = [('85016',), ('85225',)]
        for row in zipcodes:
            self.ui.zipcodeList.addItem(row[0])

        zipcodeStats1 = [("639",)]
        zipcodeStats2 = [("23473",)]
        zipcodeStats3 = [("6703.1",)]
        self.ui.zipStats1.setText(zipcodeStats1[0][0]) # This places the selected 
        self.ui.zipStats2.setText(zipcodeStats2[0][0]) # This places the selected  
        self.ui.zipStats3.setText(zipcodeStats3[0][0]) # This places the selected 

        
        #Adding some styling for the header and background count and labels for the header
        categoryResults = "SELECT b.businessID, b.business_name, b.address, b.city, b.state, b.lat_long_cords, b.business_details, c.nameCat, c.typesCat, ch.date_, ch.amounr_of_checkins FROM Businesses b LEFT JOIN Categories c ON b.businessID = c.businessID LEFT JOIN Checkin ch ON b.businessID = ch.businessID LIMIT 10;"
        results = categoryResults
        style = "::section {""background-color: #5C5C5C; }"
        self.ui.categoryTable.horizontalHeader().setStyleSheet(style)

        self.ui.categoryTable.setColumnCount(len(results[0]))
        self.ui.categoryTable.setRowCount(len(results))

        self.ui.categoryTable.setHorizontalHeaderLabels(['# of B`s', 'Category'])
        self.ui.categoryTable.resizeColumnsToContents()
        self.ui.categoryTable.setColumnWidth(0,50)
        self.ui.categoryTable.setColumnWidth(1,135)
        currentRowCount = 0

        for row in results:
            for colCount in range (0,len(results[0])):
                self.ui.categoryTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
            currentRowCount += 1

        #Adding some styling for the header and background count and labels for the header
        businessResults = "SELECT b.businessID, b.business_name, b.address, b.city, b.state, b.lat_long_cords, b.business_details, c.nameCat, c.typesCat, ch.date_, ch.amounr_of_checkins, u.userID, u.username, u.income, r.date_, r.reviewScore, r.starRating, r.content_of_review FROM Businesses b LEFT JOIN Categories c ON b.businessID = c.businessID LEFT JOIN Checkin ch ON b.businessID = ch.businessID LEFT JOIN Users u ON b.businessID = u.userID LEFT JOIN Review r ON b.businessID = r.userID LIMIT 10;"
        addresses = ["teststring"]
        for i in range(len(businessResults)):
            selected_address = random.choice(addresses)
            stars = round(random.uniform(1.0, 4.0), 1)  # Single floating point for stars
            rev = random.randint(2, 24)  # 5th item replacement
            rating = round(random.uniform(1.1111, 3.9999), 3)  # 3 floating points for rating
            checkin = random.randint(5, 90)  # 7th item replacement
            businessResults[i] = (businessResults[i][0],  # Keep the 1st item
                                selected_address,  # Keep the 2nd item
                                businessResults[i][2],  # Keep the 3rd item
                                str(stars),  # Convert to string for the 4th item
                                str(rev),  # Convert to string for the 5th item
                                str(rating),  # Convert to string for the 6th item
                                str(checkin))  # Convert to string for the 7th item


        results = businessResults
        style = "::section {""background-color: #5C5C5C; }"
        self.ui.businessTable.horizontalHeader().setStyleSheet(style)

        self.ui.businessTable.setColumnCount(len(results[0]))
        self.ui.businessTable.setRowCount(len(results))

        self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', '# of R`s', 'R`s Rating', '# of Checkins'])
        self.ui.businessTable.resizeColumnsToContents()
        self.ui.businessTable.setColumnWidth(0,150)
        self.ui.businessTable.setColumnWidth(1,150)
        self.ui.businessTable.setColumnWidth(2,70)
        self.ui.businessTable.setColumnWidth(3,50)
        self.ui.businessTable.setColumnWidth(4,70)
        self.ui.businessTable.setColumnWidth(5,70)
        self.ui.businessTable.setColumnWidth(6,70)

        currentRowCount = 0

        for row in results:
            for colCount in range (0,len(results[0])):
                self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
            currentRowCount += 1
          

    def otherTable1(self):
        #Adding some styling for the header and background count and labels for the header
        popularResults = "SELECT b.businessID, b.business_name, b.address, FROM Businesses b LEFT JOIN Checkin ch ON b.businessID = ch.businessID LEFT JOIN Users u ON b.businessID = u.userID LEFT JOIN Review r ON b.businessID = r.userID LIMIT 10;"
        results = popularResults
        style = "::section {""background-color: #5C5C5C; }"
        self.ui.popularTable.horizontalHeader().setStyleSheet(style)

        self.ui.popularTable.setColumnCount(len(results[0]))
        self.ui.popularTable.setRowCount(len(results))

        self.ui.popularTable.setHorizontalHeaderLabels(['Business Name', 'Stars', 'Rev Rating', '# of R`s'])
        self.ui.popularTable.resizeColumnsToContents()
        self.ui.popularTable.setColumnWidth(0,100)
        self.ui.popularTable.setColumnWidth(1,50)
        self.ui.popularTable.setColumnWidth(1,60)
        self.ui.popularTable.setColumnWidth(1,50)

        currentRowCount = 0

        for row in results:
            for colCount in range (0,len(results[0])):
                self.ui.popularTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
            currentRowCount += 1

    def otherTable2(self):
        #Adding some styling for the header and background count and labels for the header
        successfulResults = "SELECT b.business_name, c.nameCat, u.username FROM Businesses b LEFT JOIN Categories c ON b.businessID = c.businessID LEFT JOIN Users u ON b.businessID = u.userID LEFT JOIN Checkin ch ON b.businessID = ch.businessID LEFT JOIN Review r ON b.businessID = r.userID LIMIT 10;"


        results = successfulResults
        style = "::section {""background-color: #5C5C5C; }"
        self.ui.successfulTable.horizontalHeader().setStyleSheet(style)

        self.ui.successfulTable.setColumnCount(len(results[0]))
        self.ui.successfulTable.setRowCount(len(results))

        self.ui.successfulTable.setHorizontalHeaderLabels(['Business Name', '# of Rev`s', '# of Checkins'])
        self.ui.successfulTable.resizeColumnsToContents()
        self.ui.successfulTable.setColumnWidth(0,110)
        self.ui.successfulTable.setColumnWidth(1,100)
        self.ui.successfulTable.setColumnWidth(1,60)

        currentRowCount = 0

        for row in results:
            for colCount in range (0,len(results[0])):
                self.ui.successfulTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
            currentRowCount += 1



    def stateChanged(self): #displays the info when user picks a state
        self.ui.cityList.clear() #Clears the box so switching between states creates a new list and not appending the existing list with the new list
        state = self.ui.stateList.currentText() #gets user selected item from statelist combo box whatever that may be
        if (self.ui.stateList.currentIndex() >= 0 ): #This executes the query only if a state is selected in the combo box
            
            # ----  This is for the bottom left hand box on page1
            sql_str = "SELECT distinct city FROM business WHERE state = '" + state + "' ORDER BY city;"
            #print(sql_str)
            try:
                results = self.executeQuery(sql_str)
                #print(results)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print("Query has Failed for cityList")

    def cityChanged(self):
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            sql_str = "SELECT name, city, state FROM business WHERE state = '" + state + "' AND city = '" + city + "' ORDER BY name;"
            results = self.executeQuery(sql_str)

    def getBusinessNames(self):
        self.ui.businesses.clear()
        businessname = self.ui.bname.text()
        sql_str = "SELECT name FROM business WHERE name LIKE '%" + businessname + "%' ORDER BY name;"
        try: 
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.businesses.addItem(row[0])
        except:
            print("Querry error page2 business names")

    def displayBusinessCity(self):
        businessname = self.ui.businesses.selectedItems()[0].text()
        sql_str = "SELECT city FROM business WHERE name = '" + businessname + "';"
        try: 
            results = self.executeQuery(sql_str)
            print(results)
            self.ui.bcity.setText(results[0][0]) # This places the selected business in the city box 
        except:
            print("Query failed in page2 in displaybusinessCity")






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone1()
    window.show()
    sys.exit(app.exec())




