# Personal Expense Tracker

IITK AIML Foundations, Programming Refresher course-end project.

Demo: [https://www.youtube.com/watch?v=JaVVv1GCE5k](https://www.youtube.com/watch?v=JaVVv1GCE5k)

## What this is

A Python menu program. You log expenses, look at them, check a monthly budget, and store the list in `expenses.csv`. Each row in memory looks like this:

```python
{'date': '2024-09-18', 'category': 'Food', 'amount': 15.50, 'description': 'Lunch with friends'}
```

## Run it

Python 3. Open this folder first (so it finds `expenses.csv`):

```bat
cd personal_expense_tracker
python personal_expense_tracker.py
```

On start it calls `load_expenses`. If the CSV is missing, you start empty.

## Menu

1. Add expense  
2. View expenses  
3. Track budget  
4. Save expenses  
5. Exit  

Add asks for date (`YYYY-MM-DD`), category, amount, description. That goes into the list only. File write happens on 4 or 5. The spec had Save as its own option, so I didn't write the CSV on every add.

View prints date, category, amount, description. Incomplete rows get skipped with a note.

Track budget asks for a monthly amount (or lets you keep / change it). `total_spent_this_month` adds this month's complete rows. Over budget prints `You have exceeded your budget!`. Under budget prints how much is left.

## Files

| File | What |
|---|---|
| `personal_expense_tracker.py` | the program |
| `expenses.csv` | saved expenses (date, category, amount, description) |

Budget is not saved. The problem statement only asked to save expenses, so it lives in memory until you close the program.

## Notes

Date has to be `YYYY-MM-DD`. Something like `9/12/2026` is rejected. Amount must be greater than 0.
