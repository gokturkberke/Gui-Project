import tkinter as tk
from tkinter import messagebox

class TransactionView(tk.Toplevel):
    def __init__(self, master, transaction_type, viewmodel):
        super().__init__(master)
        self.viewmodel = viewmodel
        self.transaction_type = transaction_type
        self.title(f"Add {transaction_type}")
        self.geometry("400x300")
        self.init_ui()

    def init_ui(self):
        tk.Label(self, text=f"Add {self.transaction_type}", font=("Arial", 16)).pack(pady=10)
        self.category_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.date_var = tk.StringVar()
        fields = [
            ("Category", self.category_var),
            ("Amount", self.amount_var),
            ("Date (YYYY-MM-DD)", self.date_var),
        ]
        for label, var in fields:
            tk.Label(self, text=label).pack(anchor="w", padx=10)
            tk.Entry(self, textvariable=var).pack(fill="x", padx=10, pady=5)
        tk.Button(self, text="Save", command=self.save_transaction).pack(pady=20)

    def save_transaction(self):
        category = self.category_var.get().strip()
        amount = self.amount_var.get().strip()
        date = self.date_var.get().strip()
        if not category or not amount or not date:
            messagebox.showerror("Validation Error", "All fields are required!")
            return
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Validation Error", "Amount must be a valid number!")
            return
        self.viewmodel.save_transaction(self.transaction_type, category, amount, date)
        messagebox.showinfo("Success", f"{self.transaction_type} added successfully!")
        self.destroy()