import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from transactions import Transactions
from database import register_user, login_user

class TransactionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Finance Manager")
        self.transactions = None  # Placeholder for Transactions instance
        self.user_id = None  # Placeholder for logged-in user ID
        self.transaction_type = tk.StringVar(value="Expense")  # Default to Expense
        theme_color = "#4A90E2"  # Blue color
        background_color = "#080808"  # Light gray background
        text_color = "#daeefe"  # Dark gray text
        button_color = "#fa7b62"  # Light gray button color
        button_hover_color = "#70a8cc"  # Darker gray for hover
        # Setup UI components
        self.setup_login_ui()

    def setup_login_ui(self):
        """Setup the login and registration user interface components."""
        self.clear_window()

        tk.Label(self.master, text="Email:").pack()
        self.email_entry = tk.Entry(self.master)
        self.email_entry.pack()

        tk.Label(self.master, text="Password:").pack()
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack()

        tk.Button(self.master, text="Login", command=self.login).pack()
        tk.Button(self.master, text="Register", command=self.show_register_ui).pack()

    def show_register_ui(self):
        """Display the registration user interface."""
        self.clear_window()

        tk.Label(self.master, text="Username:").pack()
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack()

        tk.Label(self.master, text="Email:").pack()
        self.email_entry = tk.Entry(self.master)
        self.email_entry.pack()

        tk.Label(self.master, text="Password:").pack()
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack()

        tk.Button(self.master, text="Register", command=self.register).pack()
        tk.Button(self.master, text="Back to Login", command=self.setup_login_ui).pack()

    def register(self):
        """Handle user registration."""
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        success = register_user(username, email, password)
        
        if success:
            messagebox.showinfo("Success", "Registration successful.")
            self.setup_login_ui()
        else:
            messagebox.showerror("Error", "Registration failed. Email may already be in use.")

    def login(self):
        """Handle user login."""
        email = self.email_entry.get()
        password = self.password_entry.get()
        user_id = login_user(email, password)
        
        if user_id:
            self.user_id = user_id
            self.transactions = Transactions()
            self.setup_main_ui()
        else:
            messagebox.showerror("Error", "Invalid email or password.")

    def setup_main_ui(self):
        """Setup the main user interface components."""
        self.clear_window()
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface components."""
        tk.Label(self.master, text="Select Transaction Type:").pack()
        tk.Radiobutton(self.master, text="Income", variable=self.transaction_type, value="Income", command=self.show_income_sources).pack()
        tk.Radiobutton(self.master, text="Expense", variable=self.transaction_type, value="Expense", command=self.show_expense_categories).pack()

        # Income Sources Checkboxes
        self.income_sources_frame = tk.Frame(self.master)
        self.income_sources = {
            "Trading": tk.BooleanVar(),
            "Investment": tk.BooleanVar(),
            "Salary": tk.BooleanVar(),
            "Other": tk.BooleanVar()
        }
        for source, var in self.income_sources.items():
            tk.Checkbutton(self.income_sources_frame, text=source, variable=var).pack(anchor='w')

        # Expense Categories Checkboxes
        self.expense_categories_frame = tk.Frame(self.master)
        self.expense_categories = {
            "Food": tk.BooleanVar(),
            "Rent": tk.BooleanVar(),
            "Utilities": tk.BooleanVar(),
            "Transportation": tk.BooleanVar(),
            "Healthcare": tk.BooleanVar(),
            "Entertainment": tk.BooleanVar(),
            "Education": tk.BooleanVar(),
            "Other": tk.BooleanVar()
        }
        tk.Label(self.expense_categories_frame, text="Select Expense Categories:").pack()
        for category, var in self.expense_categories.items():
            tk.Checkbutton(self.expense_categories_frame, text=category, variable=var).pack(anchor='w')

        # Entry Fields
        tk.Label(self.master, text="Date (YYYY-MM-DD):").pack()
        self.date_entry = tk.Entry(self.master)
        self.date_entry.pack()
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Set current date

        tk.Label(self.master, text="Amount:").pack()
        self.amount_entry = tk.Entry(self.master)
        self.amount_entry.pack()

        tk.Label(self.master, text="Description:").pack()
        self.description_entry = tk.Entry(self.master)
        self.description_entry.pack()

        # Add Transaction Button
        tk.Button(self.master, text="Add Transaction", command=self.add_transaction).pack()

        # Go to Dashboard Button
        tk.Button(self.master, text="Go to Dashboard", command=self.show_dashboard).pack()

        # Summary Button
        tk.Button(self.master, text="Get Summary", command=self.show_summary).pack()

        # Filter Transactions Button
        tk.Button(self.master, text="Filter Transactions", command=self.filter_transactions).pack()

        # Transaction List
        self.transaction_list = ttk.Treeview(self.master, columns=("Date", "Amount", "Category", "Subcategory", "Description"), show='headings')
        self.transaction_list.heading("Date", text="Date")
        self.transaction_list.heading("Amount", text="Amount")
        self.transaction_list.heading("Category", text="Category")
        self.transaction_list.heading("Subcategory", text="Subcategory")
        self.transaction_list.heading("Description", text="Description")
        self.transaction_list.pack()

        self.load_transactions()
        
    def add_transaction(self):
        """Add a transaction based on user input."""
        date = self.date_entry.get()
        amount = float(self.amount_entry.get())
        category = self.transaction_type.get()
        subcategory = self.get_selected_subcategories()
        description = self.description_entry.get()
        success = self.transactions.load_transactions(self.user_id, date, amount, category, subcategory, description)
        
        if success:
            messagebox.showinfo("Success", "Transaction added successfully.")
            self.load_transactions()
        else:
            messagebox.showerror("Error", "Failed to add transaction.")
        
    def get_selected_subcategories(self):
        """Get selected subcategories based on the transaction type."""
        if self.transaction_type.get() == "Income":
            return ", ".join([source for source, var in self.income_sources.items() if var.get()])
        else:
            return ", ".join([category for category, var in self.expense_categories.items() if var.get()])

    def load_transactions(self):
        """Load transactions into the Treeview."""
        for row in self.transaction_list.get_children():
            self.transaction_list.delete(row)  # Clear existing rows

        transactions = self.transactions.get_transactions(self.user_id, limit=100)  # Limit to 100 transactions for performance
        for transaction in transactions:
            self.transaction_list.insert("", "end", values=transaction)  # Insert transaction details
    
    def show_income_sources(self):
        """Show the income sources frame and hide expense categories."""
        self.expense_categories_frame.pack_forget()  # Hide expense categories frame
        self.income_sources_frame.pack()  # Show income sources frame

    def show_expense_categories(self):
        """Show the expense categories frame and hide income sources."""
        self.income_sources_frame.pack_forget()  # Hide income sources frame
        self.expense_categories_frame.pack()  # Show expense categories frame
        
    def show_dashboard(self):
        """Show the dashboard with an overview of financial metrics."""
        self.clear_window()  # Clear the current UI

        # Fetch summary data
        summary = self.transactions.get_summary(self.user_id)

        # Dashboard title
        tk.Label(self.master, text="Dashboard", font=("Arial", 16, "bold")).pack(pady=10)

        # Display total income
        tk.Label(
            self.master,
            text=f"Total Income: {summary['total_income']}",
            font=("Arial", 12),
            fg="green"
        ).pack(pady=5)

        # Display total expenses
        tk.Label(
            self.master,
            text=f"Total Expenses: {summary['total_expenses']}",
            font=("Arial", 12),
            fg="red"
        ).pack(pady=5)

        # Display net balance
        net_balance_color = "green" if summary["net_balance"] >= 0 else "red"
        tk.Label(
            self.master,
            text=f"Net Balance: {summary['net_balance']}",
            font=("Arial", 12),
            fg=net_balance_color
        ).pack(pady=5)

        # Buttons for navigation
        tk.Button(
            self.master,
            text="Back to Main",
            command=self.setup_main_ui,
            width=15,
            bg="lightblue"
        ).pack(pady=20)


    
    def show_summary(self):
        """Display the summary of transactions."""
        summary = self.transactions.get_summary(self.user_id)
        summary_message = (
            f"Total Income: {summary['total_income']}\n"
            f"Total Expenses: {summary['total_expenses']}\n"
            f"Net Balance: {summary['net_balance']}"
        )
        messagebox.showinfo("Summary", summary_message)

    def filter_transactions(self):
        """Filter transactions based on the selected date."""
        date = self.date_entry.get()
        filtered_transactions = self.transactions.filter_transactions(self.user_id, date)

        for row in self.transaction_list.get_children():
            self.transaction_list.delete(row)  # Clear existing rows

        for transaction in filtered_transactions:
            self.transaction_list.insert("", "end", values=transaction)  # Insert filtered transaction details

    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.master.winfo_children():
            widget.destroy()

    def on_close(self):
        """Handle application close event."""
        if self.transactions:
            self.transactions.close()
        self.master.destroy()
