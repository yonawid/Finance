import tkinter as tk
from tkinter import simpledialog, messagebox
import sqlite3
import matplotlib.pyplot as plt


# ==========================================
# 1. THE BLUEPRINT (Object-Oriented Class)
# ==========================================
class Transaction:
    def __init__(self, t_type, amount, date, description, category="None"):
        # The class validates and standardizes the data
        self.type = t_type.lower()
        self.amount = float(amount)
        self.date = date
        self.description = str(description)
        self.category = category

    def save_to_db(self, db_connection):
        """A new method that allows the object to save itself to SQL."""
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO transactions (type, amount, date, description, category) VALUES (?, ?, ?, ?, ?)",
            (self.type, self.amount, self.date, self.description, self.category)
        )
        db_connection.commit()


# ==========================================
# 2. DATABASE SETUP
# ==========================================
def setup_db():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type TEXT,
                        amount REAL,
                        date TEXT,
                        description TEXT,
                        category TEXT)''')
    conn.commit()
    return conn


db_conn = setup_db()


# ==========================================
# 3. APPLICATION LOGIC (The Connection)
# ==========================================
def add_income():
    amount = simpledialog.askfloat("Input", "Enter the Amount:")
    if not amount: return

    date = simpledialog.askstring("Input", "Enter the Date (e.g., 2023-10-01):")
    description = simpledialog.askstring("Input", "Enter the Description:")

    # STEP 1: Create the Transaction Object
    new_income = Transaction("income", amount, date, description)

    # STEP 2: Tell the object to save itself to the database
    new_income.save_to_db(db_conn)

    messagebox.showinfo("Success", "Income added to database!")


def add_expense():
    amount = simpledialog.askfloat("Input", "Enter the Amount:")
    if not amount: return

    category = simpledialog.askstring("Input", "Enter the Category (e.g., Food, Rent):")
    date = simpledialog.askstring("Input", "Enter the Date:")
    description = simpledialog.askstring("Input", "Enter the Description:")

    # STEP 1: Create the Transaction Object
    new_expense = Transaction("expense", amount, date, description, category)

    # STEP 2: Tell the object to save itself
    new_expense.save_to_db(db_conn)

    messagebox.showinfo("Success", "Expense added to database!")


def view_summary():
    cursor = db_conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='income'")
    income = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='expense'")
    expense = cursor.fetchone()[0] or 0

    balance = income - expense
    summary_text = f"Total Income: ${income:.2f}\nTotal Expense: ${expense:.2f}\n\nBalance: ${balance:.2f}"
    messagebox.showinfo("Financial Summary", summary_text)


def show_pie_chart():
    cursor = db_conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE type='expense' GROUP BY category")
    data = cursor.fetchall()

    if not data:
        messagebox.showwarning("No Data", "Add some expenses first!")
        return

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.figure(figsize=(6, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title("Spending by Category")
    plt.show()


# ==========================================
# 4. GUI WINDOW SETUP
# ==========================================
root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("300x350")
root.configure(padx=20, pady=20)

title_label = tk.Label(root, text="Finance Tracker", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

btn_income = tk.Button(root, text="1. Add Income", command=add_income, width=20, bg="#e6f2ff")
btn_income.pack(pady=5)

btn_expense = tk.Button(root, text="2. Add Expense", command=add_expense, width=20, bg="#ffe6e6")
btn_expense.pack(pady=5)

btn_summary = tk.Button(root, text="3. View Summary", command=view_summary, width=20)
btn_summary.pack(pady=5)

btn_chart = tk.Button(root, text="4. View Spending Chart", command=show_pie_chart, width=20, bg="#e6ffe6",
                      font=("Arial", 10, "bold"))
btn_chart.pack(pady=15)

btn_exit = tk.Button(root, text="Exit", command=root.destroy, width=20)
btn_exit.pack(pady=5)

root.mainloop()
