import getpass
import hashlib
import json
import os

USERS_FILE = "users.json"
TASKS_FILE = "tasks.json"


def ask_for_text(prompt_text):
    while True:
        typed = input(prompt_text).strip()
        if typed:
            return typed
        print("Cannot be empty.")


def ask_for_id(prompt_text):
    typed = input(prompt_text).strip()
    try:
        return int(typed)
    except ValueError:
        return None


def ask_for_password(prompt_text):
    while True:
        try:
            typed = getpass.getpass(prompt_text).strip()
        except Exception:
            typed = input(prompt_text).strip()
        if typed:
            return typed
        print("Cannot be empty.")


def hash_password(password, salt):
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def load_json(filepath, default):
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        return default
    if data is None:
        return default
    return data


def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def load_users(filepath):
    data = load_json(filepath, {})
    if not isinstance(data, dict):
        return {}
    return data


def save_users(filepath, users):
    save_json(filepath, users)


def load_tasks(filepath):
    data = load_json(filepath, {})
    if not isinstance(data, dict):
        return {}

    tasks_by_user = {}
    for username, tasks in data.items():
        if not isinstance(tasks, list):
            continue
        kept = []
        for task in tasks:
            if not isinstance(task, dict):
                continue
            if "id" not in task or "description" not in task or "status" not in task:
                continue
            try:
                task_id = int(task["id"])
            except (TypeError, ValueError):
                continue
            desc = str(task["description"]).strip()
            status = str(task["status"]).strip()
            if not desc:
                continue
            if status != "Completed":
                status = "Pending"
            kept.append(
                {
                    "id": task_id,
                    "description": desc,
                    "status": status,
                }
            )
        tasks_by_user[username] = kept
    return tasks_by_user


def save_tasks(filepath, tasks_by_user):
    save_json(filepath, tasks_by_user)


def next_id(tasks):
    if len(tasks) == 0:
        return 1
    biggest = 0
    for task in tasks:
        tid = int(task["id"])
        if tid > biggest:
            biggest = tid
    return biggest + 1


def find_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def register(users):
    print("\n--- Register ---")
    username = ask_for_text("Username: ")
    if username in users:
        print("That username is taken.\n")
        return

    password = ask_for_password("Password: ")
    salt = os.urandom(16).hex()
    users[username] = {
        "salt": salt,
        "hash": hash_password(password, salt),
    }
    save_users(USERS_FILE, users)
    print("Registered. You can log in now.\n")


def login(users):
    print("\n--- Login ---")
    username = ask_for_text("Username: ")
    password = ask_for_password("Password: ")

    rec = users.get(username)
    if rec is None:
        print("Wrong username or password.\n")
        return None

    salt = str(rec.get("salt", ""))
    stored = str(rec.get("hash", ""))
    if hash_password(password, salt) != stored:
        print("Wrong username or password.\n")
        return None

    print("Logged in as " + username + ".\n")
    return username


def add_task(tasks_by_user, username):
    print("\n--- Add a task ---")
    desc = ask_for_text("Task description: ")
    tasks = tasks_by_user.setdefault(username, [])
    task_id = next_id(tasks)
    tasks.append(
        {
            "id": task_id,
            "description": desc,
            "status": "Pending",
        }
    )
    save_tasks(TASKS_FILE, tasks_by_user)
    print("Added task " + str(task_id) + ".\n")


def view_tasks(tasks_by_user, username):
    print("\n--- Your tasks ---")
    tasks = tasks_by_user.get(username, [])
    if len(tasks) == 0:
        print("Nothing here yet.\n")
        return

    for task in tasks:
        print(
            "ID: "
            + str(task["id"])
            + " | "
            + str(task["description"])
            + " | "
            + str(task["status"])
        )
    print()


def mark_completed(tasks_by_user, username):
    print("\n--- Mark completed ---")
    tasks = tasks_by_user.get(username, [])
    if len(tasks) == 0:
        print("No tasks to update.\n")
        return

    task_id = ask_for_id("Task ID: ")
    if task_id is None:
        print("Enter a number.\n")
        return

    task = find_task(tasks, task_id)
    if task is None:
        print("Task ID not found.\n")
        return

    task["status"] = "Completed"
    save_tasks(TASKS_FILE, tasks_by_user)
    print("Task " + str(task_id) + " marked Completed.\n")


def delete_task(tasks_by_user, username):
    print("\n--- Delete a task ---")
    tasks = tasks_by_user.get(username, [])
    if len(tasks) == 0:
        print("No tasks to delete.\n")
        return

    task_id = ask_for_id("Task ID: ")
    if task_id is None:
        print("Enter a number.\n")
        return

    kept = []
    found = False
    for task in tasks:
        if task["id"] == task_id:
            found = True
        else:
            kept.append(task)

    if not found:
        print("Task ID not found.\n")
        return

    tasks_by_user[username] = kept
    save_tasks(TASKS_FILE, tasks_by_user)
    print("Deleted task " + str(task_id) + ".\n")


def display_auth_menu():
    print("Task Manager")
    print("1. Register")
    print("2. Login")
    print("3. Exit")


def display_task_menu(username):
    print("Logged in as " + username)
    print("1. Add a Task")
    print("2. View Tasks")
    print("3. Mark a Task as Completed")
    print("4. Delete a Task")
    print("5. Logout")


def task_menu(username, tasks_by_user):
    while True:
        print()
        display_task_menu(username)
        choice = input("Pick 1-5: ").strip()

        if choice == "1":
            add_task(tasks_by_user, username)
        elif choice == "2":
            view_tasks(tasks_by_user, username)
        elif choice == "3":
            mark_completed(tasks_by_user, username)
        elif choice == "4":
            delete_task(tasks_by_user, username)
        elif choice == "5":
            print("Logged out.\n")
            break
        else:
            print("Pick a number from 1 to 5.\n")


def main():
    users = load_users(USERS_FILE)
    tasks_by_user = load_tasks(TASKS_FILE)

    if len(users) > 0:
        print("Loaded " + str(len(users)) + " user(s) from " + USERS_FILE + ".")
    else:
        print("No users file yet. Start with Register.")

    while True:
        print()
        display_auth_menu()
        choice = input("Pick 1-3: ").strip()

        if choice == "1":
            register(users)
        elif choice == "2":
            username = login(users)
            if username is not None:
                task_menu(username, tasks_by_user)
        elif choice == "3":
            save_users(USERS_FILE, users)
            save_tasks(TASKS_FILE, tasks_by_user)
            print("Bye.\n")
            break
        else:
            print("Pick a number from 1 to 3.\n")


if __name__ == "__main__":
    main()
