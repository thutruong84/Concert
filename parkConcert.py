import string
import json

# Open seat data file
filename = "/Users/Admin/seating.json"
try:
    jsonFile = open(filename, 'r')
except OSError:
    print("ERROR: Unable to open the file %s" % pathToFile)
seatData = json.load(jsonFile)

# Function to print seat nicely
def PrintSeating(seatData):
    for i in range(len(seatData)):
        for j in range(len(seatData[i])):
            if seatData[i][j] == 1:
                seatData[i][j] = "X"
            else:
                seatData[i][j] = "a"
    columnName = list(string.ascii_lowercase)
    print('    ' + ' '.join(columnName))
    for i in range(20):
        print("{:2d}".format(i) + '  ' + ' '.join(seatData[i]))

def ReserveSeat(row,col, seatData):
    #convert the letter column index to number column index
    seatData[row][col] = 1
    with open("/Users/Admin/seating.json", "w") as jsonFile:
        json.dump(seatData, jsonFile)
    return seatData
    

def Billing(row):
    if row in range(0,5):
        seatPrice = 80
        pricePlusTax = 80 + (80 * 7.25 / 100)
        totalPrice = pricePlusTax + 5 
    elif row in range(5,11):
        seatPrice = 50
        pricePlusTax = 50 + (50 * 7.25 / 100)
        totalPrice = pricePlusTax + 5
    else:
        seatPrice = 25
        pricePlusTax = 25 + (25 * 7.25 / 100)
        totalPrice = pricePlusTax + 5 

    print("Your seat price is $" + str(seatPrice))
    print("Plus 7.25% tax, the price is $" + str(pricePlusTax))
    print("A $5 mask is required, so total price is $" + str(totalPrice))
    return totalPrice


# function for seat constraint
def seatConstraint(row,col,seatData):
    if (row % 2) == 0:
        Row = seatData[row]
        if col == 0:
            if (Row[0]+Row[1]+Row[2]) == 0:
                print("Seat available")
                condition = True
            else: 
                print("Seat not available. Pick another one")
                condition = False
        elif col == 1:
            if (Row[0]+Row[1]+Row[2]+Row[3]) == 0:
                print("Seat available")
                condition = True
            else: 
                print("Seat not available. Pick another one")
                condition = False
        elif col == 25:
            if (Row[25]+Row[24]+Row[23] == 0):
                print("Seat available")
                condition = True
            else: 
                print("Seat not available. Pick another one")
                condition = False
        elif col == 24:
            if (Row[25]+Row[24]+Row[23]+Row[22]) == 0:
                print("Seat available")
                condition = True
            else: 
                print("Seat not available. Pick another one")
                condition = False
        else:
            if (Row[col-2]+Row[col-1]+Row[col]+Row[col+1]+Row[col+2]) == 0:
                print("Seat available")
                condition = True
            else:
                print("Seat not available. Pick another one")
                condition = False
    else:
        print("Odd row not available. Pick row 0 or even row only")
        condition = False
    
    return condition

# function to get customer's info
def customer(name,email,ticket,bill):
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


# Create a menu for buying single seat
def single(seatData):
    check = False
    while (check == False):
        print("Due to COVID 19 resstriction, odd rows are blocked. Pick row 0 or even row only.")
        row = input("Enter the row (in number) of the seat you want:")
        row = int(row)
        col1 = input("Enter the column (in letter) of the seat you want:")
        #convert the letter column index to number column index
        col = ord(col1) - 97
        check = seatConstraint(row,col,seatData)
    
    ReserveSeat(row,col, seatData)
    print("The seat has been reserved for you.")
    bill = Billing(row)
    print("To purchase the ticket, please enter")
    name = input("Name:")
    email = input("Email address:")
    print("You have purchased the ticket successfully. Your info is saved.")
    ticket = str(row) + col1
    customer(name,email,ticket,bill)


# create a menu function to display menu option and get user input
def menu():
    print("---Enter a letter to select search option or 'Q' to quit---")
    print("[V]iew/display available seating")
    print("[B]uy/purchase a ticket")
    print("[S]earch by name")
    print("[D]isplay all purchases")
    print("[Q]uit this program")
    option = input("Choose an option:")
    return option


# initialize the main menu and get user input
# choice = menu()

# # create a while loop that will quit the program if user enters "q"

# while (choice != "Q"):

#     # case a: search by full name
#     if choice == "V":
#         PrintSeating(seatData)
#         print("Front Seat (rows 0 - 4) price $80")
#         print("Middle Seat (rows 5 - 10) price $50")
#         print("Back Seat (rows 11-19) price $25")
#         choice = menu()

#     # case b: search by last name
#     elif choice == "B":
#         singleBulk = input("Do you want to buy a single ticket or bulk? S or B:")
#         if singleBulk == "S":
            
#         print("Due to COVID 19 resstriction, odd rows are blocked. Pick row 0 or even row only.")
#         row = input("Enter the row (in number) of the seat you want:")
#         row = int(row)
#         col = input("Enter the column (in letter) of the seat you want:")
#         checkSeat = seatConstraint(row,col,seatData)
#         if checkSeat == False:
#             print("false")
#             choice = "B"
#         choice = menu()
    
#     # case c: search by first name    
#     elif choice == "c":
#         name = processName()
#         searchName(name,firstName)
#         choice = menu()

#     # if user inputs any letter other than a,b,c or q  
#     else:
#         print("*** Your choice is not valid ***")
#         choice = menu()

single(seatData)