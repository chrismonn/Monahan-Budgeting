import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import io
from PIL import Image, ImageTk

# Function to calculate budget and save data to table
def calculate_budget():
    """
    Calculate the budget based on user inputs, update progress bar,
    display a message, add data to table, and create/display a pie chart.
    """
    try:
        # Get user inputs
        income = float(income_entry.get())
        savings_goal = float(savings_goal_entry.get())
        
        # Get expense data from the table
        expense_data = []
        for child in expense_frame.winfo_children():
            if isinstance(child, tk.Frame):
                expense_category = child.children['expense_category_var'].get()  # Retrieve the selected category from StringVar
                expense_amount = float(child.children['expense_amount'].get())
                expense_data.append((expense_category, expense_amount))
        
        # Calculate total expenses
        total_expenses = sum(amount for category, amount in expense_data)

        # Calculate balance
        balance = income - total_expenses

        # Update the progress bar
        progress['value'] = (balance / savings_goal) * 100 if savings_goal else 0
        root.update_idletasks()

        # Show message based on balance and savings goal
        if balance >= savings_goal:
            messagebox.showinfo("Budget", f"Congratulations! Your balance of {balance} meets your savings goal of {savings_goal}.")
        else:
            messagebox.showinfo("Budget", f"Your balance is {balance}, which is less than your savings goal of {savings_goal}. Keep saving!")
        
        # Add data to table
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for category, amount in expense_data:
            tree.insert('', 'end', values=(date_time, income, category, amount, savings_goal, balance))

        # Create and display Pie Chart
        create_pie_chart(income, total_expenses, expense_data)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers")

# Function to create and display Pie Chart
def create_pie_chart(income, total_expenses, expense_data):
    """
    Create a pie chart based on income, total expenses, and expense data
    and display it along with a legend.
    """
    # Create a Figure and a subplot
    fig, ax = plt.subplots(figsize=(8, 6))

    # Generate colors for the pie chart
    colors = plt.cm.tab10.colors[:len(expense_data)]

    labels = [category for category, _ in expense_data]
    sizes = [amount for _, amount in expense_data]
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title('Income vs Expenses')

    # Create legend
    legend_labels = [f"{category}: ${amount}" for category, amount in expense_data]
    legend = ax.legend(legend_labels, loc="center left", bbox_to_anchor=(1, 0.5), fontsize='small')

    # Adjust legend size to fit within the window
    plt.subplots_adjust(right=0.65)

    # Convert plot to an image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img = Image.open(buf)

    # Display the image on a Tkinter Label
    photo = ImageTk.PhotoImage(img)
    pie_label.config(image=photo)
    pie_label.image = photo

# Function to add a new row for entering expense
def add_expense_row():
    """
    Add a new row for entering expense category and amount.
    """
    new_row = tk.Frame(expense_frame, bg='green')
    new_row.pack(anchor='center', pady=5)

    expense_category_var = tk.StringVar(root)
    expense_category_var.set(expense_categories[0])  # default value
    expense_category_menu = tk.OptionMenu(new_row, expense_category_var, *expense_categories)
    expense_category_menu.config(width=15)
    expense_category_menu.pack(side='left')

    expense_amount_entry = tk.Entry(new_row)
    expense_amount_entry.pack(side='left')

    new_row.children['expense_category_var'] = expense_category_var  # Assign StringVar to the frame
    new_row.children['expense_amount'] = expense_amount_entry

# Create GUI window
root = tk.Tk()
root.title("Monahan Budgeting")
root.configure(background='green')  # Background color set to green

# Centering the user input options
frame = tk.Frame(root, bg='green')
frame.pack(expand=True)

# Labels and entries for user inputs
income_label = tk.Label(frame, text="Income:")
income_label.pack(anchor='center')
income_entry = tk.Entry(frame)
income_entry.pack(anchor='center')

# Dropdown menu for expense categories
expense_categories = ['Housing', 'Transportation', 'Food', 'Utilities', 'Healthcare', 'Entertainment', 'Clothing', 'Others']
expense_category_label = tk.Label(frame, text="Expense Category:")
expense_category_label.pack(anchor='center')

# Frame to hold expense inputs
expense_frame = tk.Frame(frame, bg='green')
expense_frame.pack(anchor='center')

add_expense_row()  # Initial row for entering expense

# Button to add more expenses
add_expense_button = tk.Button(frame, text="Add Expense", command=add_expense_row)
add_expense_button.pack(anchor='center', pady=5)

savings_goal_label = tk.Label(frame, text="Savings Goal:")
savings_goal_label.pack(anchor='center')
savings_goal_entry = tk.Entry(frame)
savings_goal_entry.pack(anchor='center')

# Button to calculate budget
calculate_button = tk.Button(root, text="Calculate Budget", command=calculate_budget)
calculate_button.pack()

# Progress bar
progress = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
progress.pack()

# Table to display data
columns = ('Date', 'Income', 'Expense Category', 'Expense Amount', 'Savings Goal', 'Balance')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.pack()

# Label to display the pie chart
pie_label = tk.Label(root)
pie_label.pack()

root.mainloop()
