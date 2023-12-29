import json
from datetime import datetime

used_parcel_numbers = set()

def valid_date(date_str):
    try:
        datetime.strptime(date_str, '%d/%m/%Y')
        return True
    except ValueError:
        return False
    
def check_customer(name):
    with open('customerDetails.txt', 'r') as file:
        customers = file.readlines()
        customer_names = []
        for line in customers:
            if "'name':" in line: # Check if the line contains the "'name':" string
                parts = line.split("'name':") # Split the line by "'name':" to extract the customer name
                if len(parts) > 1:
                    customer_name = parts[1].split(",")[0].strip().strip("'")
                    customer_names.append(customer_name)
        return name in customer_names # Check if the given name is present in the extracted customer names
    
def store_bill_to_file(customer_name, bill_date, consignment_parcel_dict):
    # Read existing data from the file
    with open('customerDetails.txt', 'r') as file:
        existing_data = file.readlines()

    # Flag to determine if the customer's data is found
    customer_found = False

    # Checks through existing data
    for i, line in enumerate(existing_data):
        # Check if the line contains the selected customer's name
        if f"'name': '{customer_name}'" in line:
            customer_found = True
            # Append new bill data for the selected customer
            existing_data[i] += f"Bill Date: {bill_date}\n"
            existing_data[i] += "Consignment and Parcels:\n"
            for consignment, parcels in consignment_parcel_dict.items():
                existing_data[i] += f"Consignment: {consignment}\n"
                existing_data[i] += f"Parcels: {', '.join(parcels)}\n"
            existing_data[i] += "\n"  # Add a newline character after the entire bill data

    # If the selected customer is found, update the file with new data
    if customer_found:
        with open('customerDetails.txt', 'w') as file:
            file.writelines(existing_data)
    else:
        print(f"Customer '{customer_name}' not found in the data.")
        print()

def bill_options():
    print("===== Billing Menu =====")
    print("Select an option: ")
    print("1. Create a bill.")
    print("2. Add and calculate parcel prices.")
    print("3. Modify parcel details.")
    print("4. Delete parcels.")
    print("5. View a bill.")
    print("6. View list of bills and charged amount.")
    print("7. View list of bills and charged amount by DATE.")
    print("8. Return to previous page.")

def receive_bill_options():
    while True:
        try:
            option = int(input("Please enter your choice (1-8): "))
            if (1 <= option <= 8):
                print()
                return option
            else:
                print("Please enter a valid input! (1-8)")
                print()
        except ValueError():
            print("Invalid input! Please enter a valid input. (1-8)")
            print()

def first_menu():
    print("Pick an option")
    print("1. Check if customer exists in database.")
    print("2. Return to selection menu")
    user_choice = input("Enter you selection: ")
    return user_choice

def get_unique_consignment_number(existing_consignment_numbers):
    # Generate a consignment number starting from 10000000
    current_consignment_number = 10000000

    while current_consignment_number in existing_consignment_numbers:
        current_consignment_number += 1

    return current_consignment_number

def get_unique_parcel_number(existing_parcel_numbers):
    current_parcel_number = 'P10000000'

    while current_parcel_number in existing_parcel_numbers or current_parcel_number in used_parcel_numbers:
        current_parcel_number = 'P' + str(int(current_parcel_number[1:]) + 1).zfill(8)

    used_parcel_numbers.add(current_parcel_number)
    return current_parcel_number

# Function to update used parcel numbers with existing parcel numbers
def update_used_parcel_numbers(existing_parcel_numbers):
    used_parcel_numbers.update(existing_parcel_numbers)

def read_existing_data():
    existing_consignment_numbers = set()
    existing_parcel_numbers = set()

    with open('customerDetails.txt', 'r') as file:
        lines = file.readlines()

    consignment_number = None

    for line in lines:
        if line.startswith("Consignment:"):
            consignment_number = int(line.split(": ")[1])
            existing_consignment_numbers.add(consignment_number)
        elif line.startswith("Parcels:"):
            parcels = line.split(": ")[1].split(", ")
            existing_parcel_numbers.update(parcels)

    return existing_consignment_numbers, existing_parcel_numbers

def bill_menu(customer_name):
    # Read existing data from the file
    with open('customerDetails.txt', 'r') as file:
        existing_data = file.readlines()

    # Extract existing consignment and parcel numbers
    existing_consignment_numbers = set()
    existing_parcel_numbers = set()

    for line in existing_data:
        if line.startswith("Consignment:"):
            consignment_number = int(line.split(": ")[1])
            existing_consignment_numbers.add(consignment_number)
        elif line.startswith("Parcels:"):
            parcels = line.split(": ")[1].split(", ")
            existing_parcel_numbers.update(parcels)

    consignment_parcel_dict = {}  # Initialize an empty dictionary to store consignment and parcels

    while True:
        # Generate unique consignment number
        consignment_num = get_unique_consignment_number(existing_consignment_numbers)
        existing_consignment_numbers.add(consignment_num)

        if consignment_num not in consignment_parcel_dict:
            consignment_parcel_dict[consignment_num] = []  # Initialize an empty list for parcels

        while True:
            # Generate unique parcel number
            parcel_num = get_unique_parcel_number(existing_parcel_numbers.union(set(existing_parcel_numbers)))
            existing_parcel_numbers.add(parcel_num)

            consignment_parcel_dict[consignment_num].append(parcel_num)

            while True:
                add_more_parcels = input("Do you wish to add more parcels to this consignment? (y/n): ")
                if add_more_parcels.lower() == 'n' or add_more_parcels.lower() == 'y':
                    break
                else:
                    print("Invalid input! Please enter 'Y' or 'N'")
                    print()

            if add_more_parcels.lower() != 'y':
                break

        while True:
            add_more_consignments = input("Do you wish to add more consignments to the bill? (y/n): ")
            if add_more_consignments.lower() == 'n' or add_more_consignments.lower() == 'y':
                break
            else:
                print("Invalid input! Please enter 'Y' or 'N'")
                print()

        if add_more_consignments.lower() != 'y':
            break

    while True:
        bill_date = input("Enter a date for the bill to be created (DD/MM/YYYY): ")
        # Assuming you've collected consignment_parcel_dict data properly

        store_bill_to_file(customer_name, bill_date, consignment_parcel_dict)
        print(f"Bill successfully created for {customer_name}!")
        print()
        break

def calculate_price(weight, zone):
    prices = {
        'A': {'below_1kg': 8.00, '1kg_to_3kg': 16.00},
        'B': {'below_1kg': 9.00, '1kg_to_3kg': 18.00},
        'C': {'below_1kg': 10.00, '1kg_to_3kg': 20.00},
        'D': {'below_1kg': 11.00, '1kg_to_3kg': 22.00},
        'E': {'below_1kg': 12.00, '1kg_to_3kg': 24.00}
    }

    zone = zone.upper()  # Convert input to uppercase for case-insensitive comparison

    if weight < 1:
        price = prices.get(zone, {}).get('below_1kg')
    elif 1 <= weight <= 3:
        price = prices.get(zone, {}).get('1kg_to_3kg')
    else:
        price = 0  # Add handling for weights above 3kg if needed

    return price

def calculate_total_price(parcel_weights, parcel_zones):
    total_price = 0
    for weight, zone in zip(parcel_weights, parcel_zones):
        price = calculate_price(weight, zone)
        total_price += price

    return total_price

def calculate_total_price_with_tax(total_price):
    tax = 0.08 * total_price
    total_price_with_tax = total_price + tax
    return total_price_with_tax

def add_and_calculate_parcel_prices():
    while True:
        consignment_num = input("Enter the consignment number: ")

        # Read the content of the file
        with open('customerDetails.txt', 'r') as file:
            lines = file.readlines()

        found = False
        consignment_index = None
        total_price_index = None

        # Check the lines to find the given consignment number and the total price index
        for index, line in enumerate(lines):
            if f"Consignment: {consignment_num}" in line:
                found = True
                consignment_index = index
            elif found and line.startswith("Total price for Consignment"):
                total_price_index = index
                break

        if found and consignment_index is not None:
            parcels = []
            total_price = 0

            for index, line in enumerate(lines[consignment_index:], start=consignment_index):
                if line.strip().startswith('Parcels'):
                    parcels_line_index = index
                    parcels = line.split(':')[1].strip().split(', ')
                    print(f"Existing parcels for Consignment {consignment_num}: {', '.join(parcels)}")
                    parcel_to_calculate = input("Enter the parcel number to calculate price: ")

                    if parcel_to_calculate in parcels:
                        while True:
                            try:
                                weight = float(input(f"Enter the weight for parcel {parcel_to_calculate}: "))
                                if weight <= 0:
                                    print("Weight should be a positive number.")
                                    print()
                                else:
                                    break
                            except ValueError:
                                print("Invalid input! Please enter a valid weight.")
                                print()

                        while True:
                            zone = input(f"Enter the zone for parcel {parcel_to_calculate} (Zone A/B/C/D/E): ").upper()
                            if zone not in ['A', 'B', 'C', 'D', 'E']:
                                print("Invalid zone! Please enter Zone A, B, C, D, or E.")
                                print()
                            else:
                                break

                        # Calculate the total price for the selected parcel
                        total_price = calculate_price(weight, zone)

                        if total_price is not None:
                            # Calculate total price with tax
                            total_price_with_tax = calculate_total_price_with_tax(total_price)
                            print(f"Total price for parcel {parcel_to_calculate} (incl. tax): RM {total_price_with_tax:.2f}")

                            # Insert the total price with tax directly after the consignment details
                            if total_price_index is None:
                                lines.insert(parcels_line_index + 1, f"Total price for Parcel {parcel_to_calculate} in Consignment {consignment_num} (incl. tax): RM {total_price_with_tax:.2f}\n")
                            else:
                                lines.insert(total_price_index + 1, f"Total price for Parcel {parcel_to_calculate} in Consignment {consignment_num} (incl. tax): RM {total_price_with_tax:.2f}\n")
                                
                            with open('customerDetails.txt', 'w') as file:
                                file.writelines(lines)
                                print("Data updated successfully.")
                                break
                        else:
                            print("Invalid weight or zone! Please re-enter.")
                            print()
                    else:
                        print(f"Parcel {parcel_to_calculate} not found in Consignment {consignment_num}.")
                        print()
                    break

            if not found:
                print(f"Consignment {consignment_num} not found.")
                print()
            else:
                break

def modify_consignment():
    consignment_num = input("Enter the consignment number to modify: ")

    with open('customerDetails.txt', 'r') as file:
        lines = file.readlines()

    found = False

    for index, line in enumerate(lines):
        if f"Consignment: {consignment_num}" in line:
            found = True
        elif found and line.strip().startswith('Consignment'):
            break
        elif found and line.strip().startswith('Parcels'):
            parcels_line_index = index
            parcels = line.split(':')[1].strip().split(', ')
            print(f"Existing parcels for Consignment {consignment_num}: {', '.join(parcels)}")
            parcel_to_modify = input("Enter the parcel number to modify: ")

            if parcel_to_modify in parcels:
                new_parcel = input(f"Enter the updated parcel number for {parcel_to_modify}: ")

                # Ensure the new parcel number is unique and doesn't exist in other consignments
                while new_parcel in parcels or any(f"Parcels: {new_parcel}" in l for l in lines):
                    print(f"Parcel number '{new_parcel}' already exists or is assigned to another consignment.")
                    new_parcel = input(f"Enter a different unique parcel number for {parcel_to_modify}: ")

                parcels[parcels.index(parcel_to_modify)] = new_parcel  # Update the parcel number

                # Construct the updated parcels line with modified parcel details
                updated_parcels_line = f"Parcels: {', '.join(parcels)}\n"
                lines[parcels_line_index] = updated_parcels_line  # Update the line in the file
                print(f"Parcel {parcel_to_modify} in Consignment {consignment_num} altered successfully.")
                print()
                break

            else:
                print(f"Parcel {parcel_to_modify} not found in Consignment {consignment_num}.")
                print()
                break

    if not found:
        print(f"Consignment {consignment_num} not found.")
        print()
    else:
        # Update the entire consignment and parcels data in the stored file
        with open('customerDetails.txt', 'w') as file:
            for line in lines:
                file.write(line)

def delete_parcel():
    consignment_num = input("Enter the consignment number to delete the parcel from: ")  # Ask for consignment number

    with open('customerDetails.txt', 'r') as file:  # Open the file in read mode
        lines = file.readlines()  # Read lines from the file

    found = False  # Initialize a flag to track if the consignment is found

    for index, line in enumerate(lines):  # Loop through each line in the file
        if f"Consignment: {consignment_num}" in line:  # Check if consignment number exists in the line
            found = True  # Set found flag to True if consignment is found

        elif found and line.strip().startswith('Consignment'):  # If consignment is found, stop at the next consignment
            break

        elif found and line.strip().startswith('Parcels'):  # If consignment is found, and line starts with 'Parcels'
            parcels_line_index = index  # Store the index of the line containing parcel information
            parcels = line.split(':')[1].strip().split(', ')  # Extract and split parcel data
            print(f"Existing parcels for Consignment {consignment_num}: {', '.join(parcels)}")  # Display existing parcels
            parcel_to_delete = input("Enter the parcel number to delete: ")  # Ask for parcel number to delete

            if parcel_to_delete in parcels:  # Check if the parcel exists in the list of parcels
                parcels.remove(parcel_to_delete)  # Remove the selected parcel from the list
                updated_parcels_line = f"Parcels: {', '.join(parcels)}\n"  # Create updated parcel line
                lines[parcels_line_index] = updated_parcels_line  # Update the line with modified parcels
                print(f"Parcel {parcel_to_delete} in Consignment {consignment_num} deleted successfully.")  # Confirmation message
                print()
                break

            else:  # If the specified parcel is not found in the consignment
                print(f"Parcel {parcel_to_delete} not found in Consignment {consignment_num}.")
                print()
                break

    if not found:  # If the consignment number is not found in the file
        print(f"Consignment {consignment_num} not found.")
    
    else:  # If consignment number is found
        with open('customerDetails.txt', 'w') as file:  # Open the file in write mode to update
            for line in lines:  # Rewrite the updated lines to the file
                file.write(line)  # Write each line back to the file

def read_bill_data():
    with open('customerDetails.txt', 'r') as file:
        lines = file.readlines()
        bill_records = []
        index = 0
        while index < len(lines):
            line = lines[index].strip()
            if line.startswith("Bill Date:"):
                bill_date = line.split(": ")[1]
                next_index = index + 1
                if next_index < len(lines):
                    next_line = lines[next_index].strip()
                    if next_line.startswith("Consignment and Parcels:"):
                        consignment_and_parcels_data = {}
                        index += 2  # Move past the 'Consignment and Parcels:' line
                        while index < len(lines):
                            consignment_line = lines[index].strip()
                            if consignment_line.startswith("Consignment:"):
                                consignment = consignment_line.split(": ")[1]
                                index += 1
                                parcels_line = lines[index].strip()
                                parcels = parcels_line.split(": ")[1].split(", ")
                                consignment_and_parcels_data[consignment] = parcels
                            elif consignment_line == "":
                                break  # End of consignment and parcels data
                            index += 1
                        bill_records.append({'Bill Date': bill_date, 'Consignment and Parcels': consignment_and_parcels_data})
                else:
                    # Handle the scenario where there's no next line after 'Bill Date'
                    pass  # or raise an error or handle as necessary
            index += 1
    return bill_records

def update_bill_data(bill_records):
    with open('customerDetails.txt', 'w') as file:  # Open the file in write mode
        for bill in bill_records:  # Iterate through each bill in the bill_records
            customer_name = bill['Customer']  # Extract customer name from the bill
            bill_date = bill['Date']  # Extract bill date from the bill
            consignment_list = '|'.join(bill['Consignments'])  # Create a string of consignments separated by '|'
            parcel_list = '|'.join(['|'.join(parcel) for parcel in bill['Parcels']])  # Create a string of parcels separated by '|'

            # Write the formatted data to the file in a specific format
            file.write(f"{customer_name},{bill_date},{consignment_list},{parcel_list}\n")

def view_bill_by_consignment(consignment_num):
    with open('customerDetails.txt', 'r') as file:
        lines = file.readlines()
        found = False
        current_consignment = None

        for line in lines:
            line = line.strip()
            if line.startswith("Consignment:"):
                current_consignment = line.split(": ")[1]
            elif line.startswith("Parcels:"):
                parcels = line.split(": ")[1]
                if current_consignment == consignment_num:
                    found = True
                    print(f"Consignment Number: {current_consignment}")
                    print(f"Parcels: {parcels}")
                    print()
                    break

        if not found:
            print(f"No bill found for Consignment Number: {consignment_num}")
            print()

def view_bill():
    consignment_num = input("Enter the consignment number to view the bill: ")
    print()
    view_bill_by_consignment(consignment_num)

def view_bill_with_total():
    with open('customerDetails.txt', 'r') as file:
        lines = file.readlines()
        bill_records = []   # Initialize an empty list to store bill records
        current_bill = {}   # Initialize an empty dictionary for current bill data
        for line in lines:
            line = line.strip()  # Remove leading/trailing whitespaces
            if line.startswith("Bill Date:"):  # Check if the line indicates the start of a new bill (contains "Bill Date:")
                if current_bill:
                    bill_records.append(current_bill)  # Append the current bill data to the bill_records list if it exists
                current_bill = {"Bill Date": line.split(": ")[1], "Consignment and Parcels": {}, "Total Amount": 0.0}  # Create a new dictionary to store details of the current bill
            elif line.startswith("Consignment:"):  # Check if the line contains consignment information then adds it to the current bill dictionary
                consignment = line.split(": ")[1]
                current_bill["Consignment and Parcels"][consignment] = []
            elif line.startswith("Parcels:"):
                parcels = line.split(": ")[1]
                current_bill["Consignment and Parcels"][list(current_bill["Consignment and Parcels"].keys())[-1]] = parcels.split(", ")
            elif line.startswith("Total price for"):
                total_price = line.split(": ")[1].strip('RM')  # Extract the total price from the line
                price_float = float(total_price)  # Convert to float after cleanup
                current_bill["Total Amount"] += price_float  # Accumulate total amount for the bill
        
        if current_bill:
            bill_records.append(current_bill)

    if not bill_records:
        print("No bills found in the file.")
        print()
    else:
        print("Here's the list of bills with the total amount charged!")
        for index, bill in enumerate(bill_records, start=1):
            print(f"Bill {index}:")
            print(f"Bill Date: {bill.get('Bill Date', 'N/A')}")
            
            consignment_parcels = bill["Consignment and Parcels"]
            for consignment, parcels in consignment_parcels.items():
                print(f"Consignment: {consignment}")
                print(f"Parcels: {', '.join(parcels)}")
                print()
            
            total_amount = bill["Total Amount"]  # Retrieve the total amount for the bill
            print(f"Total Amount for Bill {index}: RM {total_amount:.2f}")  # Display total amount for the bill
            print()

def receive_date():
    while True:
        date_str = input("Enter the date (DD/MM/YYYY): ")
        try:
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
            return date_obj
        except ValueError:
            print("Invalid date format! Please enter the date in (DD/MM/YYYY)")
            print()

def view_bills_by_date_range(start_date, end_date):
    try:
        with open('customerDetails.txt', 'r') as file:
            lines = file.readlines()
            bill_records = []   # Initialize an empty list to store bill records
            current_bill = {}   # Initialize an empty dictionary for current bill data
            for line in lines:
                line = line.strip() # Remove leading/trailing whitespaces
                if line.startswith("Bill Date:"):   # Check if the line indicates the start of a new bill (contains "Bill Date:")
                    if current_bill:
                        bill_records.append(current_bill)   # Append the current bill data to the bill_records list if it exists
                    current_bill = {"Bill Date": line.split(": ")[1], "Consignment and Parcels": {}, "Total Amount": 0.0}    # Create a new dictionary to store details of the current bill
                elif line.startswith("Consignment:"):   # Check if the line contains consignment information then adds it to the current bill dictionary
                    current_bill["Consignment and Parcels"][line.split(": ")[1]] = []
                elif line.startswith("Parcels:"):
                    parcels = line.split(": ")[1]
                    current_bill["Consignment and Parcels"][list(current_bill["Consignment and Parcels"].keys())[-1]] = parcels.split(", ")
            
            if current_bill:
                bill_records.append(current_bill)

        if not bill_records:
            print("No bills found in the file.")
            print()
        else:
            print(f"Here are the bills within the date range {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}:")
            for index, bill in enumerate(bill_records, start=1):
                bill_date = datetime.strptime(bill.get('Bill Date', ''), '%d/%m/%Y')
                if start_date <= bill_date <= end_date:
                    print(f"Bill {index}:")
                    print(f"Bill Date: {bill.get('Bill Date', 'N/A')}")
                    total_amount = 0  # Initialize total amount for the bill
                    for consignment, parcels in bill.get("Consignment and Parcels", {}).items():
                        print(f"Consignment: {consignment}")
                        print(f"Parcels: {', '.join(parcels)}")
                        for parcel in parcels:
                            total_price_line = f"Total price for Parcel {parcel} in Consignment {consignment} (incl. tax)"
                            total_price = None
                            for line in lines:
                                if total_price_line in line:
                                    total_price = line.split(": ")[1].strip('RM \n')  # Clean up the string
                                    price_float = float(total_price)  # Convert to float after cleanup
                                    total_amount += price_float  # Accumulate total amount for the bill
                                    break
                        print()
                    print(f"Total Amount for Bill {index}: RM {total_amount:.2f}")  # Display total amount for the bill
                    print()

    except ValueError as e:
        print(f"ValueError: {e}")
        print("An issue occurred while processing the date range.")
        print("Please ensure the date range is correctly formatted (DD/MM/YYYY) and contains valid dates.")
        print()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Please check your code logic and inputs.")
        print()

while True:
    bill_options()
    selected_option = receive_bill_options()
    
    if selected_option == 1:
        print("****Please check whether the customer exists in the database before creating a bill.****")

        while True:
            user_choice = first_menu()

            if user_choice == '1':
                customer_name = input("Enter a customer's name to check if it exists in the database: ")
                if check_customer(customer_name):
                    bill_menu(customer_name)
                else:
                    print(f"The customer '{customer_name}' you have entered, does not exist in the database.")

            elif user_choice == '2':
                print("Returning to previous menu.")
                print()
                break
            else:
                print("Invalid input. Please enter a valid input!")
                print()

    elif selected_option == 2:
        add_and_calculate_parcel_prices()
    elif selected_option == 3:
        modify_consignment()
    elif selected_option == 4:
        delete_parcel()
    elif selected_option == 5:
        view_bill()
    elif selected_option == 6:
        view_bill_with_total()
    elif selected_option == 7:
        print("****Viewing bills by date range.****")
        start_date = receive_date()
        end_date = receive_date()
        print()
        view_bills_by_date_range(start_date, end_date)
    elif selected_option == 8:
        import UserLogin
        UserLogin.continue_login_process()