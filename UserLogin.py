import ast

# Login function
def login(correctUser, correctPass): 
    while True:
        try:
            username = input("Username: ")
            password = input("Password: ")
            if username == correctUser and password == correctPass:
                break # If the username and password matches, break the loop and continue to the menu
            else:
                print("Incorrect username and/or password! Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")
    print("Login success!")

# Retrieve values from a text file and stores it in a dictionary
def readFile(fileName):
        try:
            data = {}
            with open(fileName, 'r') as file:
                for line in file:
                    index, record = line.split(': ', 1)
                    data[int(index)] = ast.literal_eval(record.strip())
            return data
        except FileNotFoundError:
            print(f"Error: File '{fileName}' not found.")
            return {}
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return {}
# Write values from a dictionary into a text file
def writeToFile(data, fileName):
    try:
        with open(fileName, 'w') as file:
            for index, record in data.items():
                file.write(f"{index}: {record}\n")
        print(f"Data successfully written to '{fileName}'.")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

# Input customer details
def customerInput(id, dict):
    try:
        name = str(input("Name (cannot be changed later): "))
        address = str(input("Address: "))
        telephoneNumber = int(input("Telephone Number: "))
        details = [name, address, telephoneNumber] # Put each customer details into a list
        dict.update({id: # Adds list into the dictionary with a new ID
                            {"name": details[0],
                             "address": details[1],
                             "telephoneNumber": details[2]
                             }})
        print("New customer successfully added!")
    except Exception as e:
        print(f"An error occurred: {e}")

# Edit customer's address and telephone number
def customerEdit(dict):
    try:
        editId = int(input("Which customer ID would you like to edit? "))
        for key, value in dict[editId].items():
            print(f"{key}: {value}")
        newAddress = str(input("\nNew address: "))
        newTelephoneNumber = int(input("New telephone number: "))
        dict[editId].update({"address": newAddress, "telephoneNumber": newTelephoneNumber}) # Updates customer details based on the ID
        print("Customer details successfully updated!")
    except KeyError:
        print(f"No customer found with ID {editId}") # Error handling when ID entered doesn't exist
    except Exception as e:
        print(f"An error occurred: {e}")

# View price of parcel based on weight and destination
def viewPrice(dict):
    try:
        weight = float(input("Weight: "))
        destination = str(input("Destination: "))
        if weight < 1:
            weight = "below_1kg"
        elif weight <= 3:
            weight = "1kg_to_3kg"
        print(dict[destination][weight])
    except KeyError:
        print(f"No price found for destination {destination} and weight {weight}") # Error handling when destination and weight doesn't match
    except Exception as e:
        print(f"An error occurred: {e}")

# View details of parcel received based on date and destination
def viewParcelsReceived(dict):
    try:
        found = False
        dateView = str(input("Date (yyyy/mm/dd): "))
        destinationView = str(input("Destination: "))
        for key, parcel in dict.items():
            if parcel['date'] == dateView and parcel['destination'] == destinationView:
                found = True
                print(f"\nParcel Received ID: {key}")
                for key, value in parcel.items():
                    print(f"{key}: {value}")
        if not found:
            print("No parcel found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Initializaton
operatorUsername = "operator"
operatorPassword = "12345"
continueOption = 'y'
customerDetails = {}
parcelReceived = {}
parcelPrice = prices = {
        'Zone A': {'below_1kg': 8.00, '1kg_to_3kg': 16.00},
        'Zone B': {'below_1kg': 9.00, '1kg_to_3kg': 18.00},
        'Zone C': {'below_1kg': 10.00, '1kg_to_3kg': 20.00},
        'Zone D': {'below_1kg': 11.00, '1kg_to_3kg': 22.00},
        'Zone E': {'below_1kg': 12.00, '1kg_to_3kg': 24.00}
    }

# Main function
def login_process():
    global continueOption
    login(operatorUsername, operatorPassword)
    customerDetails = readFile('customerDetails.txt') # Move the text file into the dictionary
    parcelReceived = readFile('parcelReceived.txt')
    customerId = len(customerDetails) # Continue numbering for customer ID
    while continueOption == 'y': 
        option = int(input("\n===== Menu =====\n1. Add customer details\n2. Modify customer details\n3. List of customers\n4. Parcel prices\n5. List of parcel received\n6. Billing Menu\n7. Exit to First Menu\nPlease enter your option: "))
        match option:
            case 1:
                customerInput(customerId, customerDetails)
                customerId+=1
            case 2:
                customerEdit(customerDetails)
            case 3:
                for key, customer in customerDetails.items():
                    print(f"\nID: {key}")
                    for key, value in customer.items():
                        print(f"{key}: {value}")
            case 4:
                viewPrice(parcelPrice)
            case 5:
                viewParcelsReceived(parcelReceived)
            case 6:
                import Billing
            case 7:
                import FirstMenu
            case _:
                print("Invalid input, please enter a valid option!")
                continue
        continueOption = input("\nWould you like to select another option from the menu? (y/n) ") # Prompt the menu until the user wants to exit
    writeToFile(customerDetails, 'customerDetails.txt') # Move values from the dictionary to the text file
    print("Successfully logged out.")
    
def continue_login_process():
    global continueOption
    continueOption = 'y'
    login_process()
    
if __name__ == "__main__":
    login_process()