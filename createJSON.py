import string
import json

# Function to create 520 avaiable seats
def CreateSeating(rows,cols):
    rectangle = [[0]*cols for i in range(rows)]
    return rectangle

# Create 520 available seats
allSeats = CreateSeating(20,26)

# Serializing json 
json_object = json.dumps(allSeats)
  
# Writing to seating.json
with open("seating.json", "w") as outfile:
    outfile.write(json_object)

# Create an empty list
empty = []

# Serializing json 
emptyJsonObject = json.dumps(empty)

# Writing to customer.json
with open("customer.json", "w") as outfile:
    outfile.write(emptyJsonObject)

