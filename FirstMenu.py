def opening_menu():
    while True:
        print("===== Welcome to the UPeeS Parcel Delivery System! =====")
        print("To continue, please select an option: ")
        print("1. User Login")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            from UserLogin import continue_login_process
            continue_login_process()
        elif choice == '2':
            print("Exiting the system. Goodbye!")
            break
        elif choice == 'admin':  # Hidden input to enter the admin menu
            print("Admin access granted! Opening Admin Menu...")
            import Administrator
        else:
            print("Invalid choice! Please select a valid option.")
            
opening_menu()