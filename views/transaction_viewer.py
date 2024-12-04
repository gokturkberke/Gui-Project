import tkinter as tk
from tkinter import ttk

class TransactionViewer(tk.Toplevel):
    def __init__(self, master, viewmodel):
        super().__init__(master)
        self.master = master
        self.viewmodel = viewmodel
        self.title(self.get_translation("view_transactions"))
        self.geometry("600x400")
        self.init_ui()

    def init_ui(self):
        self.tree = ttk.Treeview(self, columns=("Date", "Type", "Amount", "Category"), show='headings')
        self.tree.heading("Date", text=self.get_translation("date"))
        self.tree.heading("Type", text=self.get_translation("type"))
        self.tree.heading("Amount", text=self.get_translation("amount"))
        self.tree.heading("Category", text=self.get_translation("category"))

        transactions = self.viewmodel.get_transactions()
        for transaction in transactions:
            self.tree.insert("", "end", values=(transaction.date, transaction.type, transaction.amount, transaction.category))

        self.tree.pack(expand=True, fill='both')

    def get_translation(self, key, **kwargs):
        return self.viewmodel.get_translation(key, **kwargs)

    def refresh_ui(self):
        self.title(self.get_translation("view_transactions"))
        self.tree.heading("Date", text=self.get_translation("date"))
        self.tree.heading("Type", text=self.get_translation("type"))
        self.tree.heading("Amount", text=self.get_translation("amount"))
        self.tree.heading("Category", text=self.get_translation("category"))