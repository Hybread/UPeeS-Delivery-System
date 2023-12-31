def opening_menu():
    while True:
        print("===== Welcome to the UPeeS Parcel Delivery System! =====")
        print("To continue, please select an option: ")
        print("1. User Login")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            login("operator", "12345")
            handleOperator()
            break
        elif choice == '2':
            print("Exiting the system. Goodbye!")
            break
        elif choice == 'admin':  # Hidden input to enter the admin menu
            handleAdmin()
            break
        else:
            print("Invalid choice! Please select a valid option.")

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

def handleOperator():
    from Operator import operatorMenu
    operatorMenu()

def handleAdmin():
    print("Admin access granted! Opening Admin Menu...")
    from Administrator import adminMenu
    adminMenu()

# Main function
if __name__ == "__main__":
    opening_menu()