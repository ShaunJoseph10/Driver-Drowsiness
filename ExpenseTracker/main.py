import json
from datetime import datetime

# Load expenses from file
def load_expenses():
    try:
        with open("expenses.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# Save expenses to file
def save_expenses(expenses):
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)


# Add a new expense
def add_expense(expenses):
    amount = float(input("Enter amount: "))
    category = input("Enter category: ")

    choice = input("Use today's date? (y/n): ")

    if choice.lower() == "y":
        date = datetime.now().strftime("%Y-%m-%d")
    else:
        date = input("Enter date (YYYY-MM-DD): ")

    expense = {
        "amount": amount,
        "category": category,
        "date": date
    }

    expenses.append(expense)
    save_expenses(expenses)

    print("Expense added successfully!")


# Show all expenses
def view_expenses(expenses):
    if not expenses:
        print("No expenses found.")
        return

    print("\n----- All Expenses -----")

    for expense in expenses:
        print(
            f"Amount: ₹{expense['amount']} | "
            f"Category: {expense['category']} | "
            f"Date: {expense['date']}"
        )


# Category-wise summary
def category_summary(expenses):
    if not expenses:
        print("No expenses found.")
        return

    totals = {}

    for expense in expenses:
        category = expense["category"]

        if category not in totals:
            totals[category] = 0

        totals[category] += expense["amount"]

    print("\n----- Category Summary -----")

    for category, total in totals.items():
        print(f"{category}: ₹{total}")


# Overall spending
def overall_summary(expenses):
    total = 0

    for expense in expenses:
        total += expense["amount"]

    print("\nTotal Spending: ₹", total)


# Monthly summary
def monthly_summary(expenses):
    if not expenses:
        print("No expenses found.")
        return

    totals = {}

    for expense in expenses:
        month = expense["date"][:7]  # YYYY-MM

        if month not in totals:
            totals[month] = 0

        totals[month] += expense["amount"]

    print("\n----- Monthly Summary -----")

    for month, total in totals.items():
        print(f"{month}: ₹{total}")


# Main menu
def main():
    expenses = load_expenses()

    while True:
        print("\n===== PERSONAL EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Category Summary")
        print("4. Overall Spending")
        print("5. Monthly Summary")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            category_summary(expenses)

        elif choice == "4":
            overall_summary(expenses)

        elif choice == "5":
            monthly_summary(expenses)

        elif choice == "6":
            print("Thank you for using Expense Tracker!")
            break

        else:
            print("Invalid choice. Try again.")


main()