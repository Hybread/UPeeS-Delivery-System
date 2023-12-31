import json

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"An error occurred while reading the JSON file: {e}")
        return None
    
# Retrieve values from a text file and stores it in a dictionary
def read_customer_info(file_path):
    customer_dict = {}

    with open(file_path, 'r') as file:
        current_id = None
        current_data = None

        for line in file:
            line = line.strip()

            if '{' in line and '}' in line:
                if current_id is not None and current_data is not None:
                    customer_dict[current_id] = current_data

                current_id, current_data = extract_customer_info(line)

        # Add the last customer's data
        if current_id is not None and current_data is not None:
            customer_dict[current_id] = current_data

    return customer_dict

def extract_customer_info(line):
    # Assuming the line contains something like "0: {'name': 'Collin', 'address': 'PH', 'telephoneNumber': 123}"
    parts = line.split(':', 1)
    customer_id = int(parts[0])
    customer_data = eval(parts[1])  # Safely evaluate the dictionary from the string
    return customer_id, customer_data
        
# Write values from a dictionary into a text file
def appendToFile(data, fileName):
    try:
        existing_indexes = set()

        # Read existing indexes from the file
        with open(fileName, 'r') as file:
            for line in file:
                if line.strip().endswith('}'):
                    parts = line.split(':', 1)
                    existing_indexes.add(int(parts[0]))

        with open(fileName, 'a') as file:
            for index, record in data.items():
                if index not in existing_indexes:
                    file.write(f"{index}: {record}\n")
                    existing_indexes.add(index)  # Update the set of existing indexes

        print(f"Data successfully appended to '{fileName}'.")
    except Exception as e:
        print(f"An error occurred while appending to the file: {e}")

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
            weight = "UNDER1KG"
        elif weight <= 3:
            weight = "1KGTO3KG"
        elif weight > 3:
            weight = "OVER3KG"
        print(dict[weight][destination])
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

# Main function
def operatorMenu():
    customerDetails = {}
    parcelReceived = {}
    customerDetails = read_customer_info('customerDetails.txt') # Move the text file into the dictionary
    parcelReceived = read_customer_info('parcelReceived.txt')
    parcelPrice = read_json_file('parcel_price.json')
    print(parcelPrice)
    print(customerDetails)
    customerId = len(customerDetails) # Continue numbering for customer ID
    while True: 
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
                appendToFile(customerDetails, 'customerDetails.txt')
                from Billing import billingMenu
                billingMenu() # Executes main function from Billing.py
                break
            case 7:
                appendToFile(customerDetails, 'customerDetails.txt')
                print("Successfully logged out.")
                from FirstMenu import opening_menu
                opening_menu() # Executes main menu
                break
            case _:
                print("Invalid input, please enter a valid option!")
                continue