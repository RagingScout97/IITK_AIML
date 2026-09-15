# Task Manager with User Authentication

IITK AIML Foundations, Programming Refresher course-end project.

Code explanation and demo: [https://youtu.be/IBJkR-gxmcg](https://youtu.be/IBJkR-gxmcg)

## What this is

A Python menu program. You register, log in, then add / view / complete / delete your own tasks. Passwords go into `users.json` as a hash, not plain text. Tasks go into `tasks.json` keyed by username, so one user cannot see another user's list.

Each task in memory looks like this:

```python
{'id': 1, 'description': 'Finish the CEP writeup', 'status': 'Pending'}
```

## Run it

Python 3. Open this folder first (so it finds the JSON files):

```bat
cd task_manager_with_user_authentication
python task_manager_with_user_authentication.py
```

On start it calls `load_users` and `load_tasks`. Missing files just means you start empty.

## Menus

First screen:

1. Register
2. Login
3. Exit

After login:

1. Add a Task
2. View Tasks
3. Mark a Task as Completed
4. Delete a Task
5. Logout

Register asks for a username and password. Username has to be new. The password is hashed with SHA-256 plus a random salt before it is written.

Login checks the typed password against the stored hash. Same error for a missing user and a wrong password, so you don't get a hint.

Add asks for a description, gives the next free ID for that user, sets status to `Pending`, and writes `tasks.json` right away. The spec said store the task in a file, so I didn't wait for a separate Save option like the expense tracker.

View prints ID, description, and status. Complete and delete both ask for the task ID from your own list only.

## Files

| File | What |
|---|---|
| `task_manager_with_user_authentication.py` | the program |
| `users.json` | usernames, salt, password hash |
| `tasks.json` | tasks grouped by username |

Logout just goes back to Register / Login. Exit writes both files again and quits.

## Notes

Password is typed with `getpass`, so nothing shows on screen while you type. Username and the rest still use normal `input`. IDs stay unique for that user even after a delete; the next add uses max ID + 1.
