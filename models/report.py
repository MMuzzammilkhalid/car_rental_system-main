import json
from tabulate import tabulate

def load_json(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return []

def show_users():
    users = load_json("data/users.json")
    print("\n========== USERS ==========")
    if not users:
        print("No user data found.")
        return

    table = []
    for u in users:
        table.append([
            u["username"],
            u["first_name"],
            u["last_name"],
            f"${u['balance']:.2f}",
            len(u.get("rentals", []))
        ])

    print(tabulate(table, headers=["Username", "First Name", "Last Name", "Balance", "Total Rentals"], tablefmt="grid"))

def show_cars():
    cars = load_json("data/cars.json")
    print("\n========== CARS ==========")
    if not cars:
        print("No car data found.")
        return

    table = []
    for c in cars:
        table.append([
            c["car_id"],
            c["brand"],
            c["model"],
            c["seating_capacity"],
            f"${c['rental_price']:.2f}",
            "Yes" if c["available"] else "No"
        ])

    print(tabulate(table, headers=["ID", "Brand", "Model", "Seats", "Price/Day", "Available"], tablefmt="grid"))

def show_rentals():
    rentals = load_json("data/rentals.json")
    print("\n========== RENTALS ==========")
    if not rentals:
        print("No rental data found.")
        return

    table = []
    for username, rental_list in rentals.items():
        for r in rental_list:
            table.append([
                username,
                r["car_id"],
                r["start_date"],
                r["end_date"],
                r["status"].capitalize(),
                r.get("return_date", "-"),
                f"${r['total_cost']:.2f}",
                f"${r.get('fine_amount', 0):.2f}"
            ])

    print(tabulate(table, headers=["Username", "Car ID", "Start", "End", "Status", "Returned", "Cost", "Fine"], tablefmt="grid"))

if __name__ == "__main__":
    show_users()
    show_cars()
    show_rentals()
