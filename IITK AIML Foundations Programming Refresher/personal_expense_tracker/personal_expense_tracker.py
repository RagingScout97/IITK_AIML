import csv
import os
from datetime import datetime, date

EXPENSES_FILE = "expenses.csv"


def parse_date(text):
    """Return a date object from YYYY-MM-DD text, or None if invalid."""
    text = text.strip()
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return None


def ask_for_date(prompt_text):
    while True:
        typed = input(prompt_text).strip()
        expense_date = parse_date(typed)
        if expense_date is not None:
            return expense_date
        print("Use YYYY-MM-DD, for example 2024-09-18.")


def ask_for_text(prompt_text):
    while True:
        typed = input(prompt_text).strip()
        if typed:
            return typed
        print("Cannot be empty.")


def ask_for_amount(prompt_text):
    while True:
        typed = input(prompt_text).strip()
        try:
            amount = float(typed)
        except ValueError:
            amount = None
        if amount is None or amount <= 0:
            print("Enter a number greater than 0.")
            continue
        return round(amount, 2)


def load_expenses(filepath):
    """Read expenses from a CSV file into a list of dictionaries."""
    expenses = []
    if not os.path.exists(filepath):
        return expenses

    with open(filepath, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            date_text = (row.get("date") or "").strip()
            category = (row.get("category") or "").strip()
            amount_text = (row.get("amount") or "").strip()
            description = (row.get("description") or "").strip()

            expense_date = parse_date(date_text)
            try:
                amount = float(amount_text)
            except ValueError:
                amount = None

            if (
                expense_date is None
                or not category
                or amount is None
                or not description
            ):
                continue

            expenses.append(
                {
                    "date": expense_date.strftime("%Y-%m-%d"),
                    "category": category,
                    "amount": round(amount, 2),
                    "description": description,
                }
            )
    return expenses


def save_expenses(filepath, expenses):
    """Write all expenses to a CSV file."""
    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["date", "category", "amount", "description"]
        )
        writer.writeheader()
        for expense in expenses:
            writer.writerow(
                {
                    "date": expense.get("date", ""),
                    "category": expense.get("category", ""),
                    "amount": expense.get("amount", ""),
                    "description": expense.get("description", ""),
                }
            )


def expense_is_complete(expense):
    """True if the expense has date, category, amount, and description."""
    for field_name in ("date", "category", "amount", "description"):
        if field_name not in expense:
            return False
        value = expense[field_name]
        if value is None:
            return False
        if isinstance(value, str) and not value.strip():
            return False
    return parse_date(str(expense["date"])) is not None


def add_expense(expenses):
    """Ask the user for expense details and append them to the list."""
    print("\n--- Add expense ---")
    expense_date = ask_for_date("Date (YYYY-MM-DD): ")
    category = ask_for_text("Category (e.g. Food, Travel): ")
    amount = ask_for_amount("Amount: ")
    description = ask_for_text("Short description: ")

    expenses.append(
        {
            "date": expense_date.strftime("%Y-%m-%d"),
            "category": category,
            "amount": amount,
            "description": description,
        }
    )
    print("Saved in memory. Use Save from the menu to write the CSV file.\n")


def view_expenses(expenses):
    """Show all complete expenses; skip incomplete ones with a note."""
    print("\n--- Your expenses ---")
    if len(expenses) == 0:
        print("Nothing here yet.\n")
        return

    shown_count = 0
    for index in range(len(expenses)):
        expense = expenses[index]
        row_number = index + 1
        if not expense_is_complete(expense):
            print(str(row_number) + ". (skipped: missing or bad data)")
            continue
        shown_count = shown_count + 1
        amount = float(expense["amount"])
        print(
            str(row_number)
            + ". "
            + str(expense["date"])
            + " | "
            + str(expense["category"])
            + " | "
            + format(amount, ".2f")
            + " | "
            + str(expense["description"])
        )

    if shown_count == 0:
        print("No complete rows to show.\n")
    else:
        print()


def total_spent_this_month(expenses, reference_date=None):
    """Sum amounts for the calendar month of reference_date (default: today)."""
    if reference_date is None:
        reference_date = date.today()
    year_month = reference_date.strftime("%Y-%m")
    total = 0.0
    for expense in expenses:
        if not expense_is_complete(expense):
            continue
        expense_date = parse_date(str(expense["date"]))
        if expense_date is None or expense_date.strftime("%Y-%m") != year_month:
            continue
        try:
            total = total + float(expense["amount"])
        except (TypeError, ValueError):
            pass
    return round(total, 2)


def track_budget(expenses, monthly_budget):
    """Set or reuse the monthly budget, then compare it with this month's spend."""
    print("\n--- Track budget ---")
    budget = monthly_budget
    if budget is None:
        budget = ask_for_amount("Monthly budget (total for the month): ")
    else:
        change_answer = input(
            "Budget is " + format(budget, ".2f") + ". Type y to change: "
        ).strip().lower()
        if change_answer == "y":
            budget = ask_for_amount("New monthly budget: ")

    year_month = date.today().strftime("%Y-%m")
    spent = total_spent_this_month(expenses)
    print("Spent this month (" + year_month + "): " + format(spent, ".2f"))

    if spent > budget:
        print("You have exceeded your budget!")
        print("Over by " + format(spent - budget, ".2f") + ".")
    else:
        remaining = budget - spent
        print("You have " + format(remaining, ".2f") + " left for the month.")

    print()
    return budget


def display_menu():
    print("Personal Expense Tracker")
    print("1. Add expense")
    print("2. View expenses")
    print("3. Track budget")
    print("4. Save expenses")
    print("5. Exit")


def main():
    expenses = load_expenses(EXPENSES_FILE)
    monthly_budget = None

    if len(expenses) > 0:
        print(
            "Loaded "
            + str(len(expenses))
            + " row(s) from "
            + EXPENSES_FILE
            + "."
        )
    else:
        print("No CSV yet — starting with an empty list.")

    while True:
        print()
        display_menu()
        choice = input("Pick 1–5: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            monthly_budget = track_budget(expenses, monthly_budget)
        elif choice == "4":
            save_expenses(EXPENSES_FILE, expenses)
            print(
                "Wrote "
                + str(len(expenses))
                + " row(s) to "
                + EXPENSES_FILE
                + ".\n"
            )
        elif choice == "5":
            save_expenses(EXPENSES_FILE, expenses)
            print("Saved and quit. Bye.\n")
            break
        else:
            print("Pick a number from 1 to 5.\n")


if __name__ == "__main__":
    main()
