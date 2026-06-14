# Import the main graphical user interface (GUI) library and give it a short nickname 'tk'
import tkinter as tk
# Import specific modules from tkinter for pop-up input boxes and alert messages
from tkinter import simpledialog, messagebox
# Import the built-in Python library for managing local SQL databases
import sqlite3
# Import the data visualization library and give it the standard nickname 'plt'
import matplotlib.pyplot as plt


# ==========================================
# 1. THE BLUEPRINT (Object-Oriented Class)
# ==========================================
# Define a new class called Transaction to act as a blueprint for our data
class Transaction:
    # The initialization method that runs automatically when a new Transaction is created
    def __init__(self, t_type, amount, date, description, category="None"):
        # Convert the transaction type (income/expense) to lowercase for consistency in the database
        self.type = t_type.lower()
        # Convert the amount input into a decimal number (float) to prevent math errors later
        self.amount = float(amount)
        # Store the date string exactly as provided by the user
        self.date = date
        # Convert the description into a string just to be safe
        self.description = str(description)
        # Store the category, defaulting to "None" if one isn't provided
        self.category = category

    # Define a method that allows this specific transaction object to save itself
    def save_to_db(self, db_connection):
        # Create a cursor object to execute SQL commands through the provided database connection
        cursor = db_connection.cursor()
        # Execute an SQL INSERT command using placeholders (?) to securely pass in the object's data
        cursor.execute(
            "INSERT INTO transactions (type, amount, date, description, category) VALUES (?, ?, ?, ?, ?)",
            (self.type, self.amount, self.date, self.description, self.category)
        )
        # Commit (save) the changes permanently to the database file
        db_connection.commit()


# ==========================================
# 2. DATABASE SETUP
# ==========================================
# Define a function that creates and prepares our database file
def setup_db():
    # Connect to a file named 'finance.db' (SQLite will create it if it doesn't exist yet)
    conn = sqlite3.connect("finance.db")
    # Create a cursor to send SQL commands to this database
    cursor = conn.cursor()
    # Execute a multi-line SQL command to create our main data table if it isn't already there
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type TEXT,
                        amount REAL,
                        date TEXT,
                        description TEXT,
                        category TEXT)''')
    # Save the table creation to the database
    conn.commit()
    # Return the active connection so the rest of the app can use it
    return conn

# Call the setup function immediately and store the connection in a global variable
db_conn = setup_db()


# ==========================================
# 3. APPLICATION LOGIC (The Connection)
# ==========================================
# Define what happens when the "Add Income" button is clicked
def add_income():
    # Pop up a window asking for a number and store it in the 'amount' variable
    amount = simpledialog.askfloat("Input", "Enter the Amount:")
    # If the user clicked cancel or left it blank, stop running this function immediately
    if not amount: return

    # Pop up a window asking for the date string
    date = simpledialog.askstring("Input", "Enter the Date (e.g., 2023-10-01):")
    # Pop up a window asking for a description string
    description = simpledialog.askstring("Input", "Enter the Description:")

    # Create a new Transaction object using the inputs we just gathered
    new_income = Transaction("income", amount, date, description)

    # Call the object's own method to save its cleaned data into our active database
    new_income.save_to_db(db_conn)

    # Pop up a success message box to let the user know it worked
    messagebox.showinfo("Success", "Income added to database!")

# Define what happens when the "Add Expense" button is clicked
def add_expense():
    # Pop up a window asking for the expense amount
    amount = simpledialog.askfloat("Input", "Enter the Amount:")
    # Stop the function if no amount was provided
    if not amount: return

    # Pop up a window asking for the category of the expense
    category = simpledialog.askstring("Input", "Enter the Category (e.g., Food, Rent):")
    # Pop up a window asking for the date
    date = simpledialog.askstring("Input", "Enter the Date:")
    # Pop up a window asking for the description
    description = simpledialog.askstring("Input", "Enter the Description:")

    # Create a new Transaction object, passing in all the gathered expense data
    new_expense = Transaction("expense", amount, date, description, category)

    # Tell the new expense object to save itself to the database
    new_expense.save_to_db(db_conn)

    # Alert the user that the save was successful
    messagebox.showinfo("Success", "Expense added to database!")

# Define what happens when the "View Summary" button is clicked
def view_summary():
    # Create a cursor to fetch data from the database
    cursor = db_conn.cursor()
    # Ask the database to add up all amounts where the type is labeled 'income'
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='income'")
    # Fetch that single sum value; if there is no data, default to 0
    income = cursor.fetchone()[0] or 0

    # Ask the database to add up all amounts where the type is labeled 'expense'
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='expense'")
    # Fetch that single sum value; default to 0 if empty
    expense = cursor.fetchone()[0] or 0

    # Calculate the remaining balance by subtracting total expenses from total income
    balance = income - expense
    # Format a multi-line string displaying the totals, forcing 2 decimal places (.2f) for currency
    summary_text = f"Total Income: ${income:.2f}\nTotal Expense: ${expense:.2f}\n\nBalance: ${balance:.2f}"
    # Pop up a message box to display the formatted summary text
    messagebox.showinfo("Financial Summary", summary_text)

# Define what happens when the "View Spending Chart" button is clicked
def show_pie_chart():
    # Create a cursor to talk to the database
    cursor = db_conn.cursor()
    # Ask the database to group expenses by category and sum up the totals for each group
    cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE type='expense' GROUP BY category")
    # Fetch all the grouped results as a list of tuples (e.g., [('Food', 150), ('Rent', 1000)])
    data = cursor.fetchall()

    # If the list is empty (no expenses logged yet)
    if not data:
        # Show a warning pop-up telling the user to add data first
        messagebox.showwarning("No Data", "Add some expenses first!")
        # Stop the function so the chart doesn't try to draw empty data and crash
        return

    # Extract just the category names from the data tuples into a new list
    categories = [row[0] for row in data]
    # Extract just the summed amounts from the data tuples into a new list
    amounts = [row[1] for row in data]

    # Create a new Matplotlib figure window, setting its width and height to 6x6 inches
    plt.figure(figsize=(6, 6))
    # Draw a pie chart using the amounts, labeling them with categories, showing percentages, and rotating the start angle
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    # Add a title to the top of the chart window
    plt.title("Spending by Category")
    # Render and display the actual chart window to the user
    plt.show()


# ==========================================
# 4. GUI WINDOW SETUP
# ==========================================

# Initialize the main Tkinter window (the background canvas for the app)
root = tk.Tk()
# Set the text that appears in the top border/tab of the application window
root.title("Personal Finance Tracker")
# Set the default starting size of the window to 300 pixels wide by 350 pixels tall
root.geometry("300x350")
# Add 20 pixels of empty padding around the inside edges of the window so it doesn't look cramped
root.configure(padx=20, pady=20)

# Create a text label widget for the title, using Arial font, size 16, and bold text
title_label = tk.Label(root, text="Finance Tracker", font=("Arial", 16, "bold"))
# Place the label onto the window, adding 10 pixels of vertical padding around it
title_label.pack(pady=10)

# Create a button labeled "Add Income" that triggers the add_income function and has a light blue background
btn_income = tk.Button(root, text="1. Add Income", command=add_income, width=20, bg="#e6f2ff")
# Place the button onto the window with 5 pixels of vertical padding
btn_income.pack(pady=5)

# Create a button labeled "Add Expense" that triggers the add_expense function and has a light red background
btn_expense = tk.Button(root, text="2. Add Expense", command=add_expense, width=20, bg="#ffe6e6")
# Place the button onto the window with 5 pixels of vertical padding
btn_expense.pack(pady=5)

# Create a standard button labeled "View Summary" that triggers the view_summary function
btn_summary = tk.Button(root, text="3. View Summary", command=view_summary, width=20)
# Place the button onto the window with 5 pixels of vertical padding
btn_summary.pack(pady=5)

# Create a chart button triggering show_pie_chart, with a light green background and bold font to stand out
btn_chart = tk.Button(root, text="4. View Spending Chart", command=show_pie_chart, width=20, bg="#e6ffe6", font=("Arial", 10, "bold"))
# Place the chart button onto the window with 15 pixels of padding to separate it from the top group
btn_chart.pack(pady=15)

# Create an exit button that triggers the built-in root.destroy command to close the program
btn_exit = tk.Button(root, text="Exit", command=root.destroy, width=20)
# Place the exit button onto the window with 5 pixels of vertical padding
btn_exit.pack(pady=5)

# Start the infinite Tkinter event loop that keeps the window open and listening for clicks
root.mainloop()
