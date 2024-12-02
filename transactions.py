from database import create_connection, create_tables

class Transactions:
    def __init__(self):
        self.connection = create_connection()
        self.cursor = self.connection.cursor()
        create_tables()  # Ensure tables are created

    def load_transactions(self, user_id, date, amount, category, subcategory, description):
        """Add a new transaction to the database."""
        try:
            self.cursor.execute('''
                INSERT INTO transactions (user_id, date, amount, category, subcategory, description)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, date, amount, category, subcategory, description))
            self.connection.commit()
            return True
        except Exception as e:
            print("Error adding transaction:", e)
            return False

    def get_transactions(self, user_id, limit=None):
        """Retrieve all transactions for a given user, with an optional limit."""
        query = 'SELECT date, amount, category, subcategory, description FROM transactions WHERE user_id = ?'
        params = [user_id]
        if limit:
            query += ' LIMIT ?'
            params.append(limit)
        self.cursor.execute(query, tuple(params))
        return self.cursor.fetchall()

    def get_summary(self, user_id):
        """Calculate and return a summary of the user's transactions."""
        self.cursor.execute('''
            SELECT SUM(amount) FROM transactions WHERE user_id = ? AND category = 'Income'
        ''', (user_id,))
        total_income = self.cursor.fetchone()[0] or 0

        self.cursor.execute('''
            SELECT SUM(amount) FROM transactions WHERE user_id = ? AND category = 'Expense'
        ''', (user_id,))
        total_expenses = self.cursor.fetchone()[0] or 0

        net_balance = total_income - total_expenses
        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_balance": net_balance
        }

    def filter_transactions(self, user_id, date):
        """Filter transactions by date for a given user."""
        self.cursor.execute('''
            SELECT date, amount, category, subcategory, description FROM transactions WHERE user_id = ? AND date = ?
        ''', (user_id, date))
        return self.cursor.fetchall()

    def close(self):
        """Close the database connection."""
        self.connection.close()
