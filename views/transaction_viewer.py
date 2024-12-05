import tkinter as tk
from tkinter import ttk, messagebox

class TransactionViewer(tk.Toplevel):
    def __init__(self, master, viewmodel):
        super().__init__(master)
        self.master = master
        self.viewmodel = viewmodel
        self.title(self.get_translation("view_transactions"))
        self.geometry("800x400")
        self.init_ui()

    def init_ui(self):
        self.tree = ttk.Treeview(self, columns=("ID", "Date", "Type", "Amount", "Category"), show='headings')
        self.tree.heading("ID", text="ID", command=lambda: self.sort_tree("ID", False))
        self.tree.heading("Date", text=self.get_translation("date"), command=lambda: self.sort_tree("Date", False))
        self.tree.heading("Type", text=self.get_translation("type"), command=lambda: self.sort_tree("Type", False))
        self.tree.heading("Amount", text=self.get_translation("amount"), command=lambda: self.sort_tree("Amount", False))
        self.tree.heading("Category", text=self.get_translation("category"), command=lambda: self.sort_tree("Category", False))

        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Date", width=100, anchor=tk.CENTER)
        self.tree.column("Type", width=100, anchor=tk.CENTER)
        self.tree.column("Amount", width=100, anchor=tk.CENTER)
        self.tree.column("Category", width=100, anchor=tk.CENTER)

        transactions = self.viewmodel.get_transactions()
        for transaction in transactions:
            self.tree.insert("", "end", values=(transaction.id, transaction.date, transaction.type, transaction.amount, transaction.category))

        self.tree.pack(expand=True, fill='both')

        self.delete_button = tk.Button(self, text=self.get_translation("delete"), command=self.delete_transaction)
        self.delete_button.pack(pady=10)

    def sort_tree(self, col, reverse):
        transactions = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        
        if col == "Amount":
            transactions.sort(key=lambda t: float(t[0]), reverse=reverse)
        else:
            transactions.sort(reverse=reverse)

        for index, (val, k) in enumerate(transactions):
            self.tree.move(k, "", index)

        self.tree.heading(col, command=lambda: self.sort_tree(col, not reverse))

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