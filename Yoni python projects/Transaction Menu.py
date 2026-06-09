import tkinter as tk
from tkinter import simpledialog, messagebox
import sqlite3
import matplotlib.pyplot as plt


# ==========================================
# 1. DATABASE SETUP (Path 3)
# ==========================================
def setup_db():
    """Creates a database file and table if they don't exist."""
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    # Create a table using SQL
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type TEXT,
                        amount REAL,
                        date TEXT,
                        description TEXT,
                        category TEXT)''')
    conn.commit()
    return conn


# Connect to our database right away
db_conn = setup_db()


# ==========================================
# 2. APPLICATION LOGIC
# ==========================================
def add_income():
    # Visual popup windows instead of terminal inputs!
    amount = simpledialog.askfloat("Input", "Enter the Amount:")
    if not amount: return  # Cancel if user closes window

    date = simpledialog.askstring("Input", "Enter the Date (e.g., 2023-10-01):")
    description = simpledialog.askstring("Input", "Enter the Description:")

    # Save directly to the SQL database
    cursor = db_conn.cursor()
    cursor.execute("INSERT INTO transactions (type, amount, date, description, category) VALUES (?, ?, ?, ?, ?)",
                   ("income", amount, date, description, "None"))
    db_conn.commit()
    messagebox.showinfo("Success", "Income added to database!")


def add_expense():
    amount = simpledialog.askfloat("Input", "Enter the Amount:")
    if not amount: return

    category = simpledialog.askstring("Input", "Enter the Category (e.g., Food, Rent):")
    date = simpledialog.askstring("Input", "Enter the Date:")
    description = simpledialog.askstring("Input", "Enter the Description:")

    cursor = db_conn.cursor()
    cursor.execute("INSERT INTO transactions (type, amount, date, description, category) VALUES (?, ?, ?, ?, ?)",
                   ("expense", amount, date, description, category))
    db_conn.commit()
    messagebox.showinfo("Success", "Expense added to database!")


def view_summary():
    cursor = db_conn.cursor()

    # Let SQL do the math for us!
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='income'")
    income = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='expense'")
    expense = cursor.fetchone()[0] or 0

    balance = income - expense

    summary_text = f"Total Income: ${income:.2f}\nTotal Expense: ${expense:.2f}\n\nBalance: ${balance:.2f}"
    messagebox.showinfo("Financial Summary", summary_text)


# ==========================================
# 3. DATA VISUALIZATION (Path 1)
# ==========================================
def show_pie_chart():
    cursor = db_conn.cursor()
    # Get total spent per category
    cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE type='expense' GROUP BY category")
    data = cursor.fetchall()

    if not data:
        messagebox.showwarning("No Data", "Add some expenses first!")
        return

    # Split the data into two lists for Matplotlib
    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    # Draw the pie chart!
    plt.figure(figsize=(6, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title("Spending by Category")
    plt.show()


# ==========================================
# 4. GUI WINDOW SETUP (Path 2)
# ==========================================
# Create the main window
root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("300x350")
root.configure(padx=20, pady=20)

# Create a Title Label
title_label = tk.Label(root, text="Finance Tracker", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Create Clickable Buttons
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

# This line is the new "while loop" that keeps the window open!
root.mainloop()
