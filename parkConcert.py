import string
import json
import copy

# Open seat data file
filename = "/Users/Admin/seating.json"
try:
    jsonFile = open(filename, 'r')
except OSError:
    print("ERROR: Unable to open the file %s" % pathToFile)
seatData = json.load(jsonFile)

# Function to print seat nicely
def PrintSeating(seatData):
    '''Function to print seat data nicely into a square'''
    theSeat = copy.deepcopy(seatData)
    for i in range(len(theSeat)):
        for j in range(len(theSeat[i])):
            if theSeat[i][j] == 1:
                theSeat[i][j] = "X"
            else:
                theSeat[i][j] = "a"
    columnName = list(string.ascii_lowercase)
    print('    ' + ' '.join(columnName))
    for i in range(20):
        print("{:2d}".format(i) + '  ' + ' '.join(theSeat[i]))

# Function to reserve seat
def ReserveSeat(row,col, seatData):
    '''Function to reserve seat given a row, a column, and the seat data'''
    #convert the letter column index to number column index
    seatData[row][col] = 1
    with open("/Users/Admin/seating.json", "w") as jsonFile:
        json.dump(seatData, jsonFile)
    return seatData
    
# Function to calculate the price customer must pay
def Billing(row):
    '''Function to calculate the price customer must pay after reserve a seat'''
    if row in range(0,5):
        seatPrice = 80
        pricePlusTax = seatPrice + (seatPrice * 7.25 / 100)
        totalPrice = pricePlusTax + 5 
        totalPrice = round(totalPrice,2)
    elif row in range(5,11):
        seatPrice = 50
        pricePlusTax = seatPrice + (seatPrice * 7.25 / 100)
        totalPrice = pricePlusTax + 5
        totalPrice = round(totalPrice,2)
    else:
        seatPrice = 25
        pricePlusTax = seatPrice + (seatPrice * 7.25 / 100)
        totalPrice = pricePlusTax + 5 
        totalPrice = round(totalPrice,2)
    # print the bill out
    print("Your seat price is $" + str(seatPrice))
    print("Plus 7.25% tax, the price is $" + str(pricePlusTax))
    print("A $5 mask is required, so total price is $" + str(totalPrice))
    return totalPrice


# function for seat constraint
def seatConstraint(row,col,seatData):
    '''Function to check for seat constraint'''
    # first check if the chosen row is 0 or even number only 
    if (row % 2) == 0:
        Row = seatData[row]
        # constraint for when column is a (or 0 when converted to index)
        if col == 0:
            if (Row[0]+Row[1]+Row[2]) == 0:
                print("Seat available")
                condition = True
            else: 
                print("Seat not available. Pick another one")
                condition = False
        # constraint for when column is b (or 1 when converted to index)
        elif col == 1:
            if (Row[0]+Row[1]+Row[2]+Row[3]) == 0:
                print("Seat available")
                condition = True
            else: 
                print("Seat not available. Pick another one")
                condition = False
        # constraint for when column is z (or 25 when converted to index)
        elif col == 25:
            if (Row[25]+Row[24]+Row[23] == 0):
                print("Seat available")
                condition = True
            else: 
                print("Seat not available. Pick another one")
                condition = False
        # constraint for when column is y (or 24 when converted to index)
        elif col == 24:
            if (Row[25]+Row[24]+Row[23]+Row[22]) == 0:
                print("Seat available")
                condition = True
            else: 
                print("Seat not available. Pick another one")
                condition = False
        # constraint for columns from c to x (or 2 to 23 when converted to index)
        else:
            if (Row[col-2]+Row[col-1]+Row[col]+Row[col+1]+Row[col+2]) == 0:
                print("Seat available")
                condition = True
            else:
                print("Seat not available. Pick another one")
                condition = False
    # if the row is odd number, seats not available at all
    else:
        print("Odd row not available. Pick row 0 or even row only")
        condition = False
    
    return condition

# function to get customer's info
def customer(name,email,ticket,bill):
    '''Function to get customer's info and append it to customer.json'''
    # open custom.json file
    with open('customer.json') as json_file:
        data = json.load(json_file)
    # python object to be appended
    customer = {"Name": name,
        "Email": email,
        "Ticket": ticket,
        "Bill": bill
        }
    # appending data to emp_details 
    data.append(customer)
    with open('customer.json','w') as f:
        json.dump(data, f, indent=5)

# Function for buying single seat
def single(seatData):
    '''Function for when customer want to buy single seat'''
    # check for seat constraint. If seat constraint does not pass (check = false),
    # keep looping until customer choose a seat that passes the constraint
    check = False
    while (check == False):
        print("Due to COVID 19 resstriction, odd rows are blocked. Pick row 0 or even row only and 2 seats apart.")
        row = input("Enter the row (in number) of the seat you want:")
        row = int(row)
        col1 = input("Enter the column (in letter) of the seat you want:")
        #convert the letter column index to number column index
        col = ord(col1) - 97
        check = seatConstraint(row,col,seatData)
    # after passing seat contraints, reserve the seat
    ReserveSeat(row,col, seatData)
    print("The seat has been reserved for you.")
    # calculate price of ticket
    bill = Billing(row)
    # Get customer's info
    print("To purchase the ticket, please enter")
    name = input("Name:")
    email = input("Email address:")
    print("You have purchased the ticket successfully. Your info is saved.")
    ticket = str(row) + col1
    customer(name,email,ticket,bill)

# Function for buying bulk seats
def bulk(seatData):
    '''Function for buying bulk seats'''
    # get the amount of tickets customer wants to buy
    numberOfTicket = input("How many tickets do you want to buy?")
    # create an empty array to store the rows of tickets
    rowArray = []
    # create an empty array to store the columns of tickets
    colArray = []
    # create an empty array to store both rows and columns of tickets
    rowAndColArray = []
    # looping through each ticket the customer wants to buy
    for i in range(int(numberOfTicket)):
        # check for seat constraint. If seat constraint does not pass (check = false),
        # keep looping until customer choose a seat that passes the constraint
        check = False
        while (check == False):
            print("Due to COVID 19 resstriction, odd rows are blocked. Pick row 0 or even row only.")
            row = input("Enter the row (in number) of seat " + str(i+1) + " you want:")
            row = int(row)
            col1 = input("Enter the column (in letter) of seat " + str(i+1) + " you want:")
            #convert the letter column index to number column index
            col = ord(col1) - 97
            check = seatConstraint(row,col,seatData)
        # after passing seat contraints, append the row and column into their arrays
        rowArray.append(row)
        colArray.append(col)
        rowAndColArray.append(str(row)+col1)
    # reserve the seats and calculate the bill
    print("All seats you chose have been reserved for you.")
    totalSeatPurchased = 0
    for i in range(int(numberOfTicket)):
        ReserveSeat(rowArray[i],colArray[i], seatData)
        print("********************************************")
        print("Billing for seat " + str(i+1))
        bill = Billing(rowArray[i])
        totalSeatPurchased += bill
    print("********************************************")
    print("Your total purchase is $" + str(totalSeatPurchased))
    # get customer's info
    print("To purchase the tickets, please enter")
    name = input("Name:")
    email = input("Email address:")
    rowAndColArray = ','.join(rowAndColArray)
    print("You have purchased the tickets successfully. Your info is saved.")
    customer(name,email,rowAndColArray,totalSeatPurchased)


# create a menu function to display menu option and get user input
def menu():
    '''Function to display menu option and get user input'''
    print("---Enter a letter to select search option or 'Q' to quit---")
    print("[V]iew/display available seating")
    print("[B]uy/purchase a ticket")
    print("[S]earch by name")
    print("[D]isplay all purchases")
    print("[Q]uit this program")
    option = input("Choose an option:")
    option = option.upper()
    return option

# initialize the main menu and get user input
choice = menu()

# create a while loop that will quit the program if user enters "q"
while (choice != "Q"):

    # case V: display available seating
    if choice == "V":
        PrintSeating(seatData)
        print("Front Seat (rows 0 - 4) price $80")
        print("Middle Seat (rows 5 - 10) price $50")
        print("Back Seat (rows 11-19) price $25")

    # case B: buy ticket
    elif choice == "B":
        singleBulk = input("Do you want to buy a single ticket or bulk? S or B:")
        singleBulk = singleBulk.upper()
        if singleBulk == "S":
            single(seatData)
        elif singleBulk == "B":
            bulk(seatData)
        else:
            print("Your choice is not valid.")
        #choice = menu()
    
    # case S: search by name 
    elif choice == "S":
        # full path
        pathToFile = "/Users/Admin/customer.json"
        # try to open a file and throw an error if it is not found
        try:
            jsonFile = open(pathToFile, 'r')
        except OSError:
            print("ERROR: Unable to open the file %s" % pathToFile)
        # read the whole json file into a variable
        customerList = json.load(jsonFile)
        # create an empty dictionary
        customerDictionary = {}
        # loop json list of data and put each name and ticket into a dictionary
        for elem in customerList:
            # fetch name and ticket
            name = elem["Name"]
            ticket = elem["Ticket"]
            customerDictionary[name] = ticket
        # get user's input    
        userName = input("Enter a name to display the tickets purchased:")
        # print value in the dictionary by giving it a string name as the key if the name exists
        if userName in customerDictionary:
            print("Ticket's purchased by " + userName + ": "  + customerDictionary[userName])
        # print no information found if name is not in the dictionary    
        else:
            print("No information for " + userName + " found.")
        #choice = menu()

    # case D: Display all purchases
    elif choice == "D":
        # full path
        pathToFile = "/Users/Admin/customer.json"
        # try to open a file and throw an error if it is not found
        try:
            jsonFile = open(pathToFile, 'r')
        except OSError:
            print("ERROR: Unable to open the file %s" % pathToFile)
        # read the whole json file into a variable
        purchaseList = json.load(jsonFile)
        # create an empty dictionary
        purchaseDictionary = {}
        # loop json list of data and put each name and bill into a dictionary
        for elem in purchaseList:
            # fetch name and birthday
            name = elem["Name"]
            bill = elem["Bill"]
            purchaseDictionary[name] = bill
        print("------------------------")    
        print("Below are all purchases:")
        # print key and value of purchaseDictionary
        for key, value in purchaseDictionary.items():
            print("Purchase for customer " + key + " is $" + str(value))
        # make an array of purchases
        purchaseArray = list(purchaseDictionary.values())
        # sum up all purchases for total income
        totalIncome = sum(purchaseArray)
        print("---> Total amount of income that the venue has made is $" + str(totalIncome))

        #choice = menu()

    # if user inputs any letter other than V,B,S,D, or Q
    else:
        print("*** Your choice is not valid ***")
        #choice = menu()
    choice = menu()
