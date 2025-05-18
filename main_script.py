from models.customer import Customer
from models.admin import Admin
from models.car import Car
from models.rental import RentalManager
from tabulate import tabulate
import json
import os
import time

# Helper functions for file management
def load_users():
    if not os.path.exists("data"):
        os.makedirs("data")
        
    if not os.path.exists("data/users.json") or os.stat("data/users.json").st_size == 0:
        return []
    
    try:
        with open("data/users.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading users: {e}")
        return []

def save_users(users):
    if not os.path.exists("data"):
        os.makedirs("data")
        
    try:
        with open("data/users.json", "w") as f:
            json.dump(users, f, indent=4)
    except Exception as e:
        print(f"Error saving users: {e}")

def save_user(customer):
    users = load_users()
    for u in users:
        if u["username"] == customer.username:
            print("Username already exists.")
            return False
    users.append(customer.__dict__)
    save_users(users)
    print("Customer registered successfully.")
    return True

def initialize_system():
    """Setup initial data directories and sample data if needed"""
    # Create data directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Add sample cars if no cars exist
    if not os.path.exists("data/cars.json") or os.stat("data/cars.json").st_size == 0:
        sample_cars = [
            Car("1001", "Toyota", "Corolla", 5, 50.0),
            Car("1002", "Honda", "Civic", 5, 55.0),
            Car("1003", "Ford", "Mustang", 4, 85.0),
            Car("1004", "Tesla", "Model 3", 5, 95.0),
            Car("1005", "BMW", "X5", 7, 120.0)
        ]
        Car.save_cars(sample_cars)
        print("Sample cars added to the system.")
    
    # Add default admin if no admins exist
    if not os.path.exists("data/admins.json") or os.stat("data/admins.json").st_size == 0:
        default_admin = Admin("admin", "admin123", "System", "Admin")
        Admin.save_admin(default_admin)
        print("Default admin account created (username: admin, password: admin123)")

def main_menu():
    """Display the main menu and handle user interactions"""
    # Initialize the system on first run
    initialize_system()
    
    while True:
        print("\n" + "="*50)
        print("           WELCOME TO CAR RENTAL SYSTEM           ")
        print("="*50 + "\n")
        print("1. Login")
        print("2. Register")
        print("3. View Available Cars")
        print("4. Exit")
        
        choice = input("\nChoose an option: ")
        
        if choice == '1':
            login()
        elif choice == '2':
            register()
        elif choice == '3':
            Car.display_available_cars()
            input("\nPress Enter to continue...")
        elif choice == '4':
            print("\nThank you for using the Car Rental System. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")

def register():
    print("\n=== REGISTRATION ===")

    while True:
        role = input("Register as (admin/customer): ").lower()
        if role in ['admin', 'customer']:
            break
        print("Invalid role. Please enter 'admin' or 'customer'.")

    username = input("Create username: ")
    password = input("Create password: ")
    first_name = input("First name: ")
    last_name = input("Last name: ")

    # Prevent duplicate usernames across admins and customers
    existing_admins = Admin.load_admins()
    for a in existing_admins:
        if a["username"] == username:
            print("This username is already taken by an admin.")
            return

    if role == "admin":
        admin = Admin(username, password, first_name, last_name)
        Admin.save_admin(admin)
    elif role == "customer":
        users = load_users()
        for u in users:
            if u["username"] == username:
                print("This username already exists.")
                return

        try:
            balance = float(input("Enter starting balance: $"))
            if balance < 0:
                print("Balance cannot be negative. Using $0 as starting balance.")
                balance = 0.0

            customer = Customer(username, password, first_name, last_name, balance)
            success = save_user(customer)

            if success:
                print(f"Welcome, {first_name}! Your account has been created.")
                time.sleep(1)
        except ValueError:
            print("Invalid balance amount. Please enter a number.")


def login():
    print("\n=== LOGIN ===")
    username = input("Username: ")
    password = input("Password: ")

    # Check admin login first
    admins = Admin.load_admins()
    for a in admins:
        if a["username"] == username and a["password"] == password:
            print("\nAdmin login successful.")
            time.sleep(0.5)
            admin_menu()
            return

    # Check if username is accidentally duplicated
    for a in admins:
        if a["username"] == username:
            print("This username belongs to an admin. Incorrect password.")
            return

    # Check customer login
    users = load_users()
    for u in users:
        if u["username"] == username and u["password"] == password:
            print("\nCustomer login successful.")
            time.sleep(0.5)
            customer = Customer(**u)
            customer_menu(customer)
            return

    print("Login failed. Incorrect username or password.")

def admin_menu():
    while True:
        print("\n" + "="*50)
        print("                  ADMIN PANEL                  ")
        print("="*50 + "\n")
        print("1. Add New Car")
        print("2. Remove Car")
        print("3. View All Cars")
        print("4. View Rental Reports")
        print("5. View System Report")  # <-- new admin-only option
        print("6. Logout")

        choice = input("\nChoose an option: ")

        if choice == '1':
            Admin.add_car()
        elif choice == '2':
            Admin.remove_car()
        elif choice == '3':
            Car.display_all_cars()
            input("\nPress Enter to continue...")
        elif choice == '4':
            Admin.view_rentals()
        elif choice == '5':
            show_system_report()  # <-- new function call
            input("\nPress Enter to continue...")
        elif choice == '6':
            print("Logging out as Admin.")
            break
        else:
            print("Invalid choice. Please select from 1 to 6.")

def customer_menu(customer):
    """Display customer menu and handle customer interactions"""
    while True:
        print(f"\n" + "="*50)
        print(f"    Welcome, {customer.first_name.upper()} {customer.last_name.upper()}!    ")
        print(f"    Your current balance: ${customer.balance:.2f}    ")
        print("="*50 + "\n")
        print("1. View Available Cars")
        print("2. Rent a Car")
        print("3. Return a Car")
        print("4. Add Balance")
        print("5. View Rental History")
        print("6. View Personal Info")
        print("7. View Rental Policy")
        print("8. Logout")
        
        choice = input("\nChoose an option: ")
        
        if choice == '1':
            Car.display_available_cars()
            input("\nPress Enter to continue...")
        elif choice == '2':
            # Check if user already has an active rental
            has_active = False
            for rental in customer.rentals:
                if rental.get("status") == "active":
                    print("\nYou already have an active rental. You can only rent one car at a time.")
                    has_active = True
                    break
            
            if not has_active:
                RentalManager.display_fine_policy()
                Car.display_available_cars()
                car_id = input('\nEnter Car ID to rent (or 0 to cancel): ')
                
                if car_id == '0':
                    continue
                    
                start_date = input('Enter Start Date (YYYY-MM-DD): ')
                end_date = input('Enter End Date (YYYY-MM-DD): ')
                customer.rent_car(car_id, start_date, end_date)
                
            input("\nPress Enter to continue...")
        elif choice == '3':
            # Check if user has any active rentals
            active_rentals = []
            for rental in customer.rentals:
                if rental.get("status") == "active":
                    car = Car.get_car_by_id(rental.get("car_id"))
                    if car:
                        active_rentals.append((rental.get("car_id"), f"{car.brand} {car.model}"))
            
            if not active_rentals:
                print("\nYou don't have any active rentals to return.")
            else:
                print("\n=== YOUR ACTIVE RENTALS ===")
                for car_id, car_info in active_rentals:
                    print(f"ID: {car_id} - {car_info}")
                
                car_id = input('\nEnter Car ID to return (or 0 to cancel): ')
                
                if car_id == '0':
                    continue
                    
                return_date = input('Enter Return Date (YYYY-MM-DD): ')
                customer.return_car(car_id, return_date)
                
            input("\nPress Enter to continue...")
        elif choice == '4':
            try:
                amount = float(input('\nEnter amount to add to your balance: $'))
                if amount <= 0:
                    print("Amount must be positive.")
                else:
                    customer + amount  # Using operator overloading
                    update_customer_balance(customer)
            except ValueError:
                print("Invalid amount. Please enter a number.")
                
            input("\nPress Enter to continue...")
        elif choice == '5':
            customer.view_rental_history()
            input("\nPress Enter to continue...")
        elif choice == '6':
            customer.view_profile()
            input("\nPress Enter to continue...")
        elif choice == '7':
            RentalManager.display_fine_policy()
            input("\nPress Enter to continue...")
        elif choice == '8':
            print("\nLogging out. Thank you for using our service!")
            update_customer_balance(customer)
            break
        else:
            print("Invalid choice. Please select 1 to 8.")
            
def update_customer_balance(customer):
    """Update customer balance in the stored data"""
    users = load_users()
    for user in users:
        if user["username"] == customer.username:
            user["balance"] = customer.balance
            break
    save_users(users)



def load_json(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except:
        return []

def show_system_report():
    users = load_json("data/users.json")
    cars = load_json("data/cars.json")
    rentals = load_json("data/rentals.json")

    print("\n========== USERS ==========")
    if users:
        user_table = [
            [u["username"], u["first_name"], u["last_name"], f"${u['balance']:.2f}", len(u.get("rentals", []))]
            for u in users
        ]
        print(tabulate(user_table, headers=["Username", "First", "Last", "Balance", "Rentals"], tablefmt="grid"))
    else:
        print("No users found.")

    print("\n========== CARS ==========")
    if cars:
        car_table = [
            [c["car_id"], c["brand"], c["model"], c["seating_capacity"], f"${c['rental_price']:.2f}", "Yes" if c["available"] else "No"]
            for c in cars
        ]
        print(tabulate(car_table, headers=["ID", "Brand", "Model", "Seats", "Price/Day", "Available"], tablefmt="grid"))
    else:
        print("No cars found.")

    print("\n========== RENTALS ==========")
    if rentals:
        rental_table = []
        for user, rental_list in rentals.items():
            for r in rental_list:
                rental_table.append([
                    user, r["car_id"], r["start_date"], r["end_date"], r["status"],
                    r.get("return_date", "-"), f"${r['total_cost']:.2f}", f"${r.get('fine_amount', 0):.2f}"
                ])
        print(tabulate(rental_table, headers=["User", "Car ID", "Start", "End", "Status", "Returned", "Cost", "Fine"], tablefmt="grid"))
    else:
        print("No rentals found.")


if __name__ == "__main__":
    main_menu()
