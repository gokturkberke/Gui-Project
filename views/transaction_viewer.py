import tkinter as tk
from tkinter import ttk, messagebox

class TransactionViewer(tk.Toplevel):
    def __init__(self, master, viewmodel):
        super().__init__(master)
        self.master = master
        self.viewmodel = viewmodel
        self.title(self.get_translation("view_transactions"))
        self.geometry("600x400")
        self.init_ui()

    def init_ui(self):
        self.tree = ttk.Treeview(self, columns=("ID", "Date", "Type", "Amount", "Category"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text=self.get_translation("date"))
        self.tree.heading("Type", text=self.get_translation("type"))
        self.tree.heading("Amount", text=self.get_translation("amount"))
        self.tree.heading("Category", text=self.get_translation("category"))

        transactions = self.viewmodel.get_transactions()
        for transaction in transactions:
            self.tree.insert("", "end", values=(transaction.id, transaction.date, transaction.type, transaction.amount, transaction.category))

        self.tree.pack(expand=True, fill='both')

        self.delete_button = tk.Button(self, text=self.get_translation("delete"), command=self.delete_transaction)
        self.delete_button.pack(pady=10)

    def delete_transaction(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning(self.get_translation("warning"), self.get_translation("select_transaction"))
            return

        transaction_id = self.tree.item(selected_item, "values")[0]
        self.viewmodel.delete_transaction(transaction_id)
        self.tree.delete(selected_item)
        messagebox.showinfo(self.get_translation("success"), self.get_translation("transaction_deleted"))

    def get_translation(self, key, **kwargs):
        return self.viewmodel.get_translation(key, **kwargs)

    def refresh_ui(self):
        self.title(self.get_translation("view_transactions"))
        self.tree.heading("Date", text=self.get_translation("date"))
        self.tree.heading("Type", text=self.get_translation("type"))
        self.tree.heading("Amount", text=self.get_translation("amount"))
        self.tree.heading("Category", text=self.get_translation("category"))
        self.delete_button.config(text=self.get_translation("delete"))