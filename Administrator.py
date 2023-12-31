import json


def load_price():
    try:
        with open('parcel_price.json', 'r') as file:
            prices = json.load(file)
    except FileNotFoundError:
        # Initial setup with fixed prices for UNDER1KG and 1KGTO3KG
        prices = {
            "UNDER1KG": {
                "A": 8.00,
                "B": 9.00,
                "C": 10.00,
                "D": 11.00,
                "E": 12.00
            },
            "1KGTO3KG": {
                "A": 16.00,
                "B": 18.00,
                "C": 20.00,
                "D": 22.00,
                "E": 24.00
            },
            "OVER3KG": {
                "A": None,
                "B": None,
                "C": None,
                "D": None,
                "E": None
            }
        }
    return prices

# program to save prices information
def save_prices(prices):
    with open('parcel_price.json', 'w') as file:
        json.dump(prices, file, indent=4)


# program to add price of parcel
def add_price(destination, price):
    prices = load_price()
    if destination not in prices['OVER3KG']:
        print("Error: Invalid Zone/Destination. please enter the right destination(a,b,c,d,e).")
    else:
        if price <= 0:
            print("Error: Price must be a positive numeric value.")
        else:
            if prices['OVER3KG'][destination] is None:
                prices['OVER3KG'][destination] = price
                save_prices(prices)
                print(f"Price for {destination} in 'OVER3KG' added successfully.")
            else:
                print(f"Error: Price for {destination} in 'OVER3KG' already exists.")


# program to modify the price of parcel
def modify_price(destination, new_price):
    prices = load_price()
    if destination not in prices['OVER3KG']:
        print("Error: Invalid Zone/Destination. please enter the right destination(a,b,c,d,e).")
    else:
        if price <= 0:
            print("Error: Price must be a positive numeric value.")
        else:
            current_price = prices['OVER3KG'][destination]
            if current_price is not None:
                prices['OVER3KG'][destination] = new_price
                save_prices(prices)
                print(f"Price for {destination} in 'OVER3KG' modified successfully.")
            else:
                print(f"Error: price in Zone {destination} has not exist. please add the price first.")


# program to delete price of parcel
def delete_price(destination):
    prices = load_price()
    if destination not in prices['OVER3KG']:
        print("Error: Invalid Zone/Destination. please enter the right destination(a,b,c,d,e).")
    else:
        if destination in prices['OVER3KG']:
            prices['OVER3KG'][destination] = None
            save_prices(prices)
            print(f"Price for {destination} in 'OVER3KG' deleted successfully.")
        else:
            print(f"Error: No price found for{destination} in 'OVER3KG'.")


# program to check price of parcel
def check_price(weight_category, destination):
    prices = load_price()
    if weight_category not in prices:
        print(f"Error: No such weight category '{weight_category}' exists.")
        return
    if destination not in prices[weight_category]:
        print("Error: Invalid Zone/Destination. please enter the right destination(a,b,c,d,e).")
    else:
        price = prices[weight_category][destination]
        if price is not None:
            print(f"price for Zone {destination} in {weight_category}: RM{price}")
        else:
            print(f"No price found for Zone {destination} in {weight_category}.")


# program to view all price of parcel
def view_prices():
    prices = load_price()
    for weight_category, destination in prices.items():
        print(f"{weight_category}: {destination}")

# User data structure: [username, role, password]
users = []

# File to store user data
data_file = "user_data.json"

def read_user_data():
    try:
        with open(data_file, "r") as file:
            data = json.load(file)
            for user_data in data:
                users.append(user_data)
    except FileNotFoundError:
        # If the file is not found, it will be created when writing data.
        pass

def write_user_data():
    with open(data_file, "w") as file:
        json.dump(users, file)

# Initialize users by reading data from the file
read_user_data()

def login(username, password):
    return any(user[0] == username and user[2] == password for user in users)

def add_user(username, role, password):
    if not any(user[0] == username for user in users):
        # Set the role to "operator" by default for new users
        users.append([username, "operator", password])
        print(f"User {username} added with operator role.")
        write_user_data()  # Update the file after adding a user
    else:
        print("User already exists.")

def assign_admin_role(username):
    user_found = False
    for user in users:
        if user[0] == username:
            user[1] = "administrator"
            user_found = True
            print(f"Administrator role assigned to {username}.")
            write_user_data()  # Update the file after modifying user role
            break

    if not user_found:
        print("User not found.")

def remove_admin_role(username):
    user_found = False
    for user in users:
        if user[0] == username:
            user[1] = "operator"
            user_found = True
            print(f"Administrator role removed from {username}.")
            write_user_data()  # Update the file after modifying user role
            break

    if not user_found:
        print("User not found.")

def delete_user(username):
    user_found = False
    for user in users:
        if user[0] == username:
            users.remove(user)
            user_found = True
            print(f"User {username} deleted.")
            write_user_data()  # Update the file after deleting a user
            break

    if not user_found:
        print("User not found.")

def view_users(role_filter):
    filtered_users = [user for user in users if role_filter == "all" or user[1] == role_filter]
    if filtered_users:
        print(f"Users with {role_filter} role:")
        for user in filtered_users:
            print(f"Username: {user[0]}, Role: {user[1]}")
    else:
        print(f"No users with {role_filter} role.")

# Add default admin user
add_user("AdminOP", "administrator", "apuadmin")

# Interactive menu
while True:
    print("\n===== Parcel Delivery Service - Administrator Menu =====")
    print("Administrator Verification Check. Please enter credentials.")
    username = input("Enter username: ")
    password = input("Enter password: ")

    if login(username, password):
        print(f"User {username} logged in.")

        # Check the role of the logged-in user
        user_role = [user[1] for user in users if user[0] == username][0]

        if user_role == "operator":
            # Operator can only view users
            print("5. View Users")
            choice = input("Enter your choice (5 to view users, 6 to exit): ")

            if choice == "5":
                role_filter = input("Enter role filter (all/operator/administrator): ")
                view_users(role_filter)

            elif choice == "6":
                print("Exiting the Parcel Delivery Service - Operator Menu. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter 5 to view users or 6 to exit.")

        elif user_role == "administrator":
            # Administrator can access all menu options
            while True:
                print("1. Add User")
                print("2. Assign Administrator Role")
                print("3. Remove Administrator Role")
                print("4. Delete User")
                print("5. View Users")
                print("6. Parcel Pricing Menu")
                print("7. LogOut")

                choice = input("Enter your choice (1-7): ")

                if choice == "1":
                    new_username = input("Enter username to add: ")
                    new_password = input("Enter password: ")
                    add_user(new_username, "operator", new_password)  # Set the role to "operator"
                    print(f"User {new_username} added with operator role.")

                elif choice == "2":
                    new_admin = input("Enter username to assign administrator role: ")
                    assign_admin_role(new_admin)

                elif choice == "3":
                    remove_admin = input("Enter username to remove administrator role: ")
                    remove_admin_role(remove_admin)

                elif choice == "4":
                    del_user = input("Enter username to delete: ")
                    delete_user(del_user)

                elif choice == "5":
                    role_filter = input("Enter role filter (all/operator/administrator): ")
                    view_users(role_filter)

                elif choice == "6":
                    # option to proceed to the program
                    while True:
                        print("\nParcel Pricing Menu")
                        print("1. Add parcel price for above 3kg")
                        print("2. Modify parcel price for above 3kg")
                        print("3. Delete parcel price for above 3kg")
                        print("4. Check parcel price")
                        print("5. View all parcel")
                        print("6. Return to previous menu")

                        # User Input
                        option = input("Enter number of choices (1-6): ")

                        if option == '1':
                            destination = input("Enter Destination/Zone (A,B,C,D,E): ").upper()
                            price = float(input("Enter price: RM"))
                            add_price(destination, price)
                            pass

                        elif option == '2':
                            destination = input("Enter Destination/Zone (A,B,C,D,E): ").upper()
                            new_price = float(input("Enter new price: RM"))
                            modify_price(destination, new_price)
                            pass

                        elif option == '3':
                            destination = input("Enter Destination/Zone (A,B,C,D,E): ").upper()
                            delete_price(destination)
                            pass

                        elif option == '4':
                            weight_category = input("Enter weight category (UNDER1KG,1KGTO3KG,OVER3KG): ").upper()
                            destination = input("Enter Destination/Zone (A,B,C,D,E): ").upper()
                            check_price(weight_category, destination)
                            pass

                        elif option == '5':
                            view_prices()
                            pass

                        elif option == '6':
                            break

                        else:
                            print("The number entered is not in option. Please enter the right number between 1 and 6.")

                elif choice == "7":
                    print("Log out the Parcel Delivery Service - Administrator Menu.")
                    break

                else:
                    print("Invalid choice. Please enter a number between 1 and 7.")

    else:
        print("Invalid username or password. Access denied.")
