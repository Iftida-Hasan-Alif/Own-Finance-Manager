import tkinter as tk
from ui_components import TransactionApp
from database import create_tables

def main():
    create_tables()  # Ensure database tables exist
    
    root = tk.Tk()
    root.geometry("800x600")  # Set fixed window size
    
    app = TransactionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()

if __name__ == "__main__":
    main()
