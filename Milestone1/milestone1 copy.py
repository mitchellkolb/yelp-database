
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
            conn = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='plzPass451'")
        except:
            print('Unable to connect to database')
         """
        try:
            conn = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='plzPass451' port='1234'")
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
        categories = [('Sandwiches',), ('Restaurants',), ('RestaurantsTableService',), ('HasTV',), ('RestaurantsGoodForGroups',), ('NoiseLevel',), ('WiFi',), ('RestaurantsAttire',), ('RestaurantsReservations',), ('OutdoorSeating',), ('BusinessAcceptsCreditCards',), ('RestaurantsPriceRange2',), ('BikeParking',), ('RestaurantsDelivery',), ('romantic',), ('intimate',), ('classy',), ('hipster',), ('divey',), ('touristy',), ('trendy',), ('upscale',), ('casual',), ('RestaurantsTakeOut',), ('GoodForKids',), ('garage',), ('street',), ('validated',), ('lot',), ('valet',), ('Chiropractors',), ('Health & Medical',), ('Reflexology',), ('Beauty & Spas',), ('AcceptsInsurance',), ('ByAppointmentOnly',), ('WheelchairAccessible',), ('Chicken Wings',), ('Pizza',)]
        for row in categories:
            self.ui.categoryList.addItem(row[0])
        
        zipcodes = [('85016',), ('85225',), ('85008',), ('85018',), ('85032',), ('85308',), ('85281',), ('85282',), ('85029',), ('85345',), ('85351',), ('85204',), ('85027',), ('85226',), ('85364',), ('85719',), ('85705',), ('85302',), ('85301',), ('85224',), ('85303',), ('85251',), ('85710',), ('85022',), ('85202',), ('85210',), ('85021',), ('85051',), ('85711',), ('85020',), ('85023',), ('85015',), ('85712',), ('85306',), ('85009',), ('85017',), ('85304',), ('85033',), ('85704',), ('85203',), ('85031',), ('85713',), ('85381',), ('85382',), ('85019',), ('85283',), ('85233',), ('85716',), ('85714',), ('85201',), ('85353',)]
        for row in zipcodes:
            self.ui.zipcodeList.addItem(row[0])

        zipcodeStats1 = [("639",)]
        zipcodeStats2 = [("23473",)]
        zipcodeStats3 = [("6703.1",)]
        self.ui.zipStats1.setText(zipcodeStats1[0][0]) # This places the selected 
        self.ui.zipStats2.setText(zipcodeStats2[0][0]) # This places the selected  
        self.ui.zipStats3.setText(zipcodeStats3[0][0]) # This places the selected 

        
        #Adding some styling for the header and background count and labels for the header
        categoryResults = [('1', 'Real Estate'), ('7', 'Home Services'), ('11', 'Property Management'), ('5', 'Apartments'), ('12', 'Hair Salons'), ('3', 'Beauty & Spas'), ('9', 'Automotive'), ('2', 'Auto Parts & Supplies'), ('6', 'Car Dealers'), ('8', 'American (Traditional)'), ('4', 'Restaurants'), ('10', 'Auto Repair'), ('1', 'Fast Food'), ('11', 'Burgers'), ('7', 'General Dentistry'), ('3', 'Health & Medical'), ('8', 'Dentists'), ('9', 'Barbeque'), ('6', 'Sports Bars'), ('2', 'Nightlife'), ('10', 'Bars'), ('5', 'Food'), ('12', 'Pizza'), ('4', 'Italian'), ('11', 'Mattresses'), ('1', 'Shopping'), ('7', 'Home & Garden'), ('3', "Men's Clothing"), ('9', "Women's Clothing"), ('10', 'Fashion'), ('6', 'Accessories'), ('8', 'Event Planning & Services'), ('2', 'Hotels'), ('12', 'Hotels & Travel'), ('5', 'Active Life'), ('4', 'Yoga'), ('11', 'Fitness & Instruction')]
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
        businessResults = [("We-Ko-PA Golf Club", '123 Ave', 'Madison', '2.0', '5', '1.123', 'checkin'),
                        ("20/20 Image Eye Centers", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("4 Sons Chevron", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("AA Affordable Locksmith", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Adobe Wine & Liquors", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("All American Sports Grill", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Auto Mobile Detective", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Boulevard Cafe", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Casavino Custom Winery", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Chen's Garden", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Chocofin Fine Handmade Chocolates", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Comfort Inn Fountain Hills - Scottsdale", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("CopperWynd Resort and Club", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("DC Bar & Grill", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Desert Dog Off Road & Fabrication", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Discount Tire Store - Fountain Hills, AZ", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Dj's Bagel Cafe", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Doggie Style", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("El Encanto de la Fuente", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Euro Pizza Cafe", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Firerock Country Club", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Fireside Grill", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Flapjacks", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Fountain Hills", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Fountain Hills Dental Care", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Fountain Hills Express", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Fountain Hills Family Practice", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Fountain Hills Nails", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Fountain Hills Theater", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Fountain Park", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Francis & Sons Car Wash", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Go Divas", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Golf Club At Eagle Mountain", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Grapeables Fine Wines", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Ha Ha China", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Jet Carpet Cleaning", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Jimmy's Krazy Greek Restaurant", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("La Scala Creamery", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("La Tartine", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Le Baron Cleaners At Basha's Shopping Center", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Mountain View Coffee", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Newer Nails", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Octagon Cafe", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Overtime Sports Grille", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Palisades Veterinary Hospital", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Paul's Ace Hardware Stores", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Phil's Filling Station Grill", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Pisa Pizza", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Pony Express", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Que Bueno", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Redendo's Pizza & Pasta", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Rosati's of Fountain Hills", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Sakura Inn", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Sapori D'Italia", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Scottsdale Spa and Holistic Massage Therapy", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Senor Taco", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("SunRidge Canyon Golf Club", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Terra Nostra", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("The Appian Way", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Vu Bistro", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("WeKoPa Resort & Conference Center", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("You Need Nails", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Zusia's Doggie Salon & Su PAW market", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("America's Choice Inn & Suites", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Best Western Space Age Lodge", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Little Italy Pizza & Restaurant", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Love's Travel Stop", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Sofia's Mexican Food", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Space Age Restaurant", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Texaco Food Mart & Service", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Truckstop Holt's Shell", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Yucca Motel", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("A Better Tint & Accessories", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("A-1 Bike Center", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Aardbark Grooming", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Absolute Dental", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Accredited Family Healthcare", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Advanced Chiropractic", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("AllKids Urgent Care", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Anasazi Animal Clinic", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Apple Dumpling Cafe", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Arizona Animal Wellness Center", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Arizona Soccer Club", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("AZ Chiropractic", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("B&G Café", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Babe's Sports Bar and Grill", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Banana Republic", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Banner Gateway Medical Center", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Barnes Fine Jewelers", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Basha's #172", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Berge Mazda", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Berge Volkswagen", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Bergies Coffee Roast House", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Best Shoe Repair & Alterations", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Big League Dreams", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Big O Tires", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Blue 32 Sports Grill", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Blue Wasabi Sushi & Martini Bar", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Boleros At Seville", '123 Ave', 'Madison', '2.0', '5', '1.123', '30'),
                        ("Boston's", '123 Ave', 'Madison', '2.0', '5', '1.123', '30')]


        addresses = ["321 Maple Ln, Appleton, WI 54911", "654 Pine Dr, Racine, WI 53402", "987 Birch Rd, Kenosha, WI 53140", "741 Cedar Blvd, Eau Claire, WI 54701", "852 Willow Ct, La Crosse, WI 54601", "963 Walnut Pl, Oshkosh, WI 54901", "159 Spruce Way, Waukesha, WI 53186", "951 Chestnut St, Janesville, WI 53545", "753 Fir Ave, Sheboygan, WI 53081", "864 Sycamore Rd, Wauwatosa, WI 53213", "210 Redwood Ln, Fond du Lac, WI 54935", "357 Ash St, West Allis, WI 53214", "822 Poplar Dr, Wausau, WI 54401", "577 Cedar Rd, Brookfield, WI 53005", "443 Maple Ave, New Berlin, WI 53151", "299 Oakwood Ct, Beloit, WI 53511", "658 Pine Pl, Greenfield, WI 53220", "432 Elm Way, Manitowoc, WI 54220", "987 Birch St, Menomonee Falls, WI 53051", "654 Pine Pl, Franklin, WI 53132", "320 Maple Ave, Oak Creek, WI 53154", "210 Redwood Ct, West Bend, WI 53095", "741 Cedar St, Stevens Point, WI 54481", "864 Sycamore Ave, Superior, WI 54880", "357 Ash Pl, Mount Pleasant, WI 53406", "753 Fir Ct, Neenah, WI 54956", "951 Chestnut Rd, Caledonia, WI 53108", "159 Spruce Pl, Mequon, WI 53092", "951 Chestnut Ave, Watertown, WI 53094", "753 Fir Way, South Milwaukee, WI 53172", "864 Sycamore Blvd, Pleasant Prairie, WI 53158", "741 Cedar Ln, Germantown, WI 53022", "987 Birch Dr, Middleton, WI 53562", "654 Pine Ave, Howard, WI 54313", "320 Maple St, Onalaska, WI 54650", "210 Redwood Way, Marshfield, WI 54449", "357 Ash Blvd, Cudahy, WI 53110", "963 Walnut Pl, Wisconsin Rapids, WI 54494", "951 Chestnut St, Menasha, WI 54952", "753 Fir Ave, Ashwaubenon, WI 54304", "864 Sycamore Rd, Beaver Dam, WI 53916", "741 Cedar Dr, Sun Prairie, WI 53590", "987 Birch Way, South Milwaukee, WI 53172", "654 Pine Ct, Beloit, WI 53511", "320 Maple Pl, Stevens Point, WI 54481", "210 Redwood Ave, Muskego, WI 53150", "357 Ash Rd, De Pere, WI 54115", "963 Walnut Blvd, Fitchburg, WI 53711", "951 Chestnut Ln, Watertown, WI 53094", "753 Fir Ct, Middleton, WI 53562", "864 Sycamore Pl, DeForest, WI 53532", "741 Cedar Way, Pleasant Prairie, WI 53158", "987 Birch Dr, Howard, WI 54313", "654 Pine Ave, Suamico, WI 54313", "320 Maple St, Monona, WI 53716", "210 Redwood Rd, Port Washington, WI 53074", "357 Ash Ave, Burlington, WI 53105", "963 Walnut Way, Germantown, WI 53022", "951 Chestnut Pl, Greendale, WI 53129", "753 Fir Dr, Oregon, WI 53575", "864 Sycamore Ave, Cedarburg, WI 53012", "741 Cedar St, Prairie du Chien, WI 53821", "987 Birch Ln, Platteville, WI 53818", "654 Pine Way, Merrill, WI 54452"]

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
        time.sleep(5)
        #Adding some styling for the header and background count and labels for the header
        popularResults = [("Red Rock Springs Farmer's Market", '5.0', '5.0', '54'), ("Rock Springs Cafe & General Store", '5.0', '5.0', '23'), ("Argentos Pizza", '5.0', '5.0', '12'), ("Ciao Grazie Pizzeria Winebar", '5.0', '5.0', '47'), ("Club Tan Salon & Boutique", '5.0', '5.0', '36'), ("Days Inn Buckeye", '5.0', '5.0', '18'), ("Filibertos Sports Grill", '5.0', '5.0', '31'), ("Golf Club of Estrella", '5.0', '5.0', '6'), ("Hula Hawaiian Barbeque", '5.0', '5.0', '40'), ("Joe Foss Shooting Range", '5.0', '5.0', '8'), ("La Placita Cafe", '5.0', '5.0', '57'), ("Love's", '5.0', '5.0', '55'), ("Memphis Best BBQ", '5.0', '5.0', '59'), ("Mikey's Restaraunt", '5.0', '5.0', '2'), ("Millstone Cafe", '5.0', '5.0', '28'), ("North Buckeye Animal Hospital", '5.0', '5.0', '53'), ("Postnet", '5.0', '5.0', '37'), ("Pretty Nails & Spa", '5.0', '5.0', '24'), ("River Ridge Veterinary Hosptal", '5.0', '5.0', '7'), ("Sundance Golf Club", '5.0', '5.0', '42'), ("The Sheep Camp", '5.0', '5.0', '58'), ("The Verrado Grille", '5.0', '5.0', '11'), ("Waddells Longhorn Corral", '5.0', '5.0', '27'), ("Wild West Cowboy Steakhouse", '5.0', '5.0', '35'), ("AZ Wine Co", '5.0', '5.0', '16'), ("Bad Donkey Sub Salad & Pizza", '5.0', '5.0', '49'), ("Black Mountain Coffee Shop", '5.0', '5.0', '43'), ("Bonnie's Yarn Crafts", '5.0', '5.0', '26'), ("Boulders Golf Club", '5.0', '5.0', '60'), ("Boulders Resort & Spa", '5.0', '5.0', '3'), ("Brix Wine", '5.0', '5.0', '45'), ("Cafe Bink", '5.0', '5.0', '10'), ("Carefree Art & Wine Festival", '5.0', '5.0', '31'), ("Carefree Cleaners", '5.0', '5.0', '21'), ("Carefree Internal Medicine MD", '5.0', '5.0', '39'), ("Carefree Resort & Conference Center", '5.0', '5.0', '32'), ("Carefree Station", '5.0', '5.0', '22'), ("Cellar 13 Wine Bar", '5.0', '5.0', '56'), ("China Joy", '5.0', '5.0', '25'), ("English Rose Tea Room", '5.0', '5.0', '46'), ("Giordano Trattoria Romana", '5.0', '5.0', '19'), ("Little Barber Shop", '5.0', '5.0', '15'), ("Lowe's Home Improvement Warehouse of Phoenix", '5.0', '5.0', '1'), ("Maduro Cigar Emporium", '5.0', '5.0', '52'), ("Pizzafarro's", '5.0', '5.0', '9'), ("The Sundial Cafe", '5.0', '5.0', '5'), ("Airport Tavern", '5.0', '5.0', '13'), ("Bedillon's Cactus Garden & Museum", '5.0', '5.0', '33'), ("Best Western Plus Casa Grande", '5.0', '5.0', '4'), ("Big House Cafe", '5.0', '5.0', '44'), ("Big Wa Chinese Restaurant", '5.0', '5.0', '20'), ("Border Line Cocina Mexicana", '5.0', '5.0', '51'), ("Cabo's Bar and Grill", '5.0', '5.0', '41'), ("Casa Grande Nails", '5.0', '5.0', '14'), ("Comfort Inn", '5.0', '5.0', '50'), ("Compton Motors", '5.0', '5.0', '17'), ("Cook E Jar Bakery & Cafe", '5.0', '5.0', '38'), ("Creative Cafe", '5.0', '5.0', '29'), ("Crossroads Auto Center", '5.0', '5.0', '48'), ("Curbside Coffee & Cafe", '5.0', '5.0', '34'), ("Dell's Pizza And Sports Bar", '5.0', '5.0', '60'), ("Discount Tire Store - Casa Grande, AZ", '5.0', '5.0', '2')]
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
        time.sleep(5)
        #Adding some styling for the header and background count and labels for the header
        successfulResults = [("Dodge Electric", '2.56789', '620'), ("Doggie Steps Dog Training, LLC.", '3.78543', '567'), ("Dog's Day Out Grooming", '1.23456', '189'), ("Douglas Barber Shop", '4.32109', '473'), ("Down Under Pool Care", '3.98765', '89'), ("Downtown Chandler", '2.34567', '369'), ("Downtown Chandler Farmer's Market", '4.09876', '414'), ("Drastic Changes Tattoo Studio", '1.54321', '94'), ("Dynamic Dentistry", '2.87654', '613'), ("East Valley Family Medical", '4.67890', '337'), ("East Valley Family Physicians", '1.87654', '502'), ("East Valley Internal Medicine P C", '4.34567', '656'), ("East Valley Oral Surgery", '3.98765', '142'), ("Egg Roll Lumpia Factory", '2.23456', '424'), ("El Alamo Carniceria", '4.12345', '364'), ("El Metate Mexican Food", '1.43210', '151'), ("El Palacio Restaurant & Cantina", '3.98765', '659'), ("El Ranchero Mexican Grill", '2.12345', '302'), ("El Rancho Market", '4.87654', '481'), ("El Sol Mexican Cafe", '1.87654', '44'), ("El Taco de Chandler", '3.76543', '507'), ("El Zocalo Mexican Grill", '2.45678', '552'), ("Elmer's Tacos", '4.10987', '649'), ("Enjoi Nails and Spa", '1.54321', '119'), ("Enzo's Gelato & Coffee Bar", '2.45678', '72'), ("Evdi Medical Imaging Centers", '3.89012', '465'), ("Evolution Custom Motorcycles", '1.23456', '265'), ("Eye Care Professionals", '4.76543', '122'), ("EZ Flow Plumbing", '2.12345', '67'), ("Fairfield Inn by Marriott", '4.87654', '366'),("Dodge Electric", '2.56789', '620'), ("Doggie Steps Dog Training, LLC.", '3.78543', '567'), ("Dog's Day Out Grooming", '1.23456', '189'), ("Douglas Barber Shop", '4.32109', '473'), ("Down Under Pool Care", '3.98765', '89'), ("Downtown Chandler", '2.34567', '369'), ("Downtown Chandler Farmer's Market", '4.09876', '414'), ("Drastic Changes Tattoo Studio", '1.54321', '94'), ("Dynamic Dentistry", '2.87654', '613'), ("East Valley Family Medical", '4.67890', '337'), ("East Valley Family Physicians", '1.87654', '502'), ("East Valley Internal Medicine P C", '4.34567', '656'), ("East Valley Oral Surgery", '3.98765', '142'), ("Egg Roll Lumpia Factory", '2.23456', '424'), ("El Alamo Carniceria", '4.12345', '364'), ("El Metate Mexican Food", '1.43210', '151'), ("El Palacio Restaurant & Cantina", '3.98765', '659'), ("El Ranchero Mexican Grill", '2.12345', '302'), ("El Rancho Market", '4.87654', '481'), ("El Sol Mexican Cafe", '1.87654', '44'), ("El Taco de Chandler", '3.76543', '507'), ("El Zocalo Mexican Grill", '2.45678', '552'), ("Elmer's Tacos", '4.10987', '649'), ("Enjoi Nails and Spa", '1.54321', '119'), ("Enzo's Gelato & Coffee Bar", '2.45678', '72'), ("Evdi Medical Imaging Centers", '3.89012', '465'), ("Evolution Custom Motorcycles", '1.23456', '265'), ("Eye Care Professionals", '4.76543', '122'), ("EZ Flow Plumbing", '2.12345', '67'), ("Fairfield Inn by Marriott", '4.87654', '366'),("Dodge Electric", '2.56789', '620'), ("Doggie Steps Dog Training, LLC.", '3.78543', '567'), ("Dog's Day Out Grooming", '1.23456', '189'), ("Douglas Barber Shop", '4.32109', '473'), ("Down Under Pool Care", '3.98765', '89'), ("Downtown Chandler", '2.34567', '369'), ("Downtown Chandler Farmer's Market", '4.09876', '414'), ("Drastic Changes Tattoo Studio", '1.54321', '94'), ("Dynamic Dentistry", '2.87654', '613'), ("East Valley Family Medical", '4.67890', '337'), ("East Valley Family Physicians", '1.87654', '502'), ("East Valley Internal Medicine P C", '4.34567', '656'), ("East Valley Oral Surgery", '3.98765', '142'), ("Egg Roll Lumpia Factory", '2.23456', '424'), ("El Alamo Carniceria", '4.12345', '364'), ("El Metate Mexican Food", '1.43210', '151'), ("El Palacio Restaurant & Cantina", '3.98765', '659'), ("El Ranchero Mexican Grill", '2.12345', '302'), ("El Rancho Market", '4.87654', '481'), ("El Sol Mexican Cafe", '1.87654', '44'), ("El Taco de Chandler", '3.76543', '507'), ("El Zocalo Mexican Grill", '2.45678', '552'), ("Elmer's Tacos", '4.10987', '649'), ("Enjoi Nails and Spa", '1.54321', '119'), ("Enzo's Gelato & Coffee Bar", '2.45678', '72'), ("Evdi Medical Imaging Centers", '3.89012', '465'), ("Evolution Custom Motorcycles", '1.23456', '265'), ("Eye Care Professionals", '4.76543', '122'), ("EZ Flow Plumbing", '2.12345', '67'), ("Fairfield Inn by Marriott", '4.87654', '366'),("Dodge Electric", '2.56789', '620'), ("Doggie Steps Dog Training, LLC.", '3.78543', '567'), ("Dog's Day Out Grooming", '1.23456', '189'), ("Douglas Barber Shop", '4.32109', '473'), ("Down Under Pool Care", '3.98765', '89'), ("Downtown Chandler", '2.34567', '369'), ("Downtown Chandler Farmer's Market", '4.09876', '414'), ("Drastic Changes Tattoo Studio", '1.54321', '94'), ("Dynamic Dentistry", '2.87654', '613'), ("East Valley Family Medical", '4.67890', '337'), ("East Valley Family Physicians", '1.87654', '502'), ("East Valley Internal Medicine P C", '4.34567', '656'), ("East Valley Oral Surgery", '3.98765', '142'), ("Egg Roll Lumpia Factory", '2.23456', '424'), ("El Alamo Carniceria", '4.12345', '364'), ("El Metate Mexican Food", '1.43210', '151'), ("El Palacio Restaurant & Cantina", '3.98765', '659'), ("El Ranchero Mexican Grill", '2.12345', '302'), ("El Rancho Market", '4.87654', '481'), ("El Sol Mexican Cafe", '1.87654', '44'), ("El Taco de Chandler", '3.76543', '507'), ("El Zocalo Mexican Grill", '2.45678', '552'), ("Elmer's Tacos", '4.10987', '649'), ("Enjoi Nails and Spa", '1.54321', '119'), ("Enzo's Gelato & Coffee Bar", '2.45678', '72'), ("Evdi Medical Imaging Centers", '3.89012', '465'), ("Evolution Custom Motorcycles", '1.23456', '265'), ("Eye Care Professionals", '4.76543', '122'), ("EZ Flow Plumbing", '2.12345', '67'), ("Fairfield Inn by Marriott", '4.87654', '366')]
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




