import tkinter as tk
from tkinter import ttk, messagebox
from viewmodels.settings_viewmodel import SettingsViewModel

class TransactionViewer(tk.Toplevel):
    def __init__(self, master, viewmodel):
        super().__init__(master)
        self.master = master
        self.viewmodel = viewmodel
        self.settings_viewmodel = SettingsViewModel(viewmodel.language)
        self.title(self.settings_viewmodel.get_translation("view_transactions"))
        self.geometry("800x400")
        self.init_ui()

    def init_ui(self):
        self.tree = ttk.Treeview(self, columns=("ID", "Date", "Type", "Amount", "Category"), show='headings')
        self.tree.heading("ID", text="ID", command=lambda: self.sort_tree("ID", False))
        self.tree.heading("Date", text=self.settings_viewmodel.get_translation("date"), command=lambda: self.sort_tree("Date", False))
        self.tree.heading("Type", text=self.settings_viewmodel.get_translation("type"), command=lambda: self.sort_tree("Type", False))
        self.tree.heading("Amount", text=self.settings_viewmodel.get_translation("amount"), command=lambda: self.sort_tree("Amount", False))
        self.tree.heading("Category", text=self.settings_viewmodel.get_translation("category"), command=lambda: self.sort_tree("Category", False))

        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Date", width=100, anchor=tk.CENTER)
        self.tree.column("Type", width=100, anchor=tk.CENTER)
        self.tree.column("Amount", width=100, anchor=tk.CENTER)
        self.tree.column("Category", width=100, anchor=tk.CENTER)

        self.load_transactions()

        self.tree.pack(expand=True, fill='both')

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=10)

        self.edit_button = tk.Button(self.button_frame, text=self.settings_viewmodel.get_translation("edit"), command=self.edit_transaction)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.button_frame, text=self.settings_viewmodel.get_translation("delete"), command=self.delete_transaction)
        self.delete_button.pack(side=tk.LEFT, padx=5)

    def load_transactions(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        transactions = self.viewmodel.get_transactions()
        for transaction in transactions:
            self.tree.insert("", "end", values=(transaction.id, transaction.date, transaction.type, transaction.amount, transaction.category))

    def sort_tree(self, col, reverse):
        transactions = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        
        if col == "Amount":
            transactions.sort(key=lambda t: float(t[0]), reverse=reverse)
        else:
            transactions.sort(reverse=reverse)

        for index, (val, k) in enumerate(transactions):
            self.tree.move(k, "", index)

        self.tree.heading(col, command=lambda: self.sort_tree(col, not reverse))

    def edit_transaction(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning(self.settings_viewmodel.get_translation("warning"), self.settings_viewmodel.get_translation("select_transaction"))
            return

        transaction_values = self.tree.item(selected_item, "values")
        EditTransactionWindow(self, self.viewmodel, transaction_values)

    def delete_transaction(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning(self.settings_viewmodel.get_translation("warning"), self.settings_viewmodel.get_translation("select_transaction"))
            return

        transaction_id = self.tree.item(selected_item, "values")[0]
        self.viewmodel.delete_transaction(transaction_id)
        self.tree.delete(selected_item)
        messagebox.showinfo(self.settings_viewmodel.get_translation("success"), self.settings_viewmodel.get_translation("transaction_deleted"))

    def refresh_ui(self):
        self.title(self.settings_viewmodel.get_translation("view_transactions"))
        self.tree.heading("Date", text=self.settings_viewmodel.get_translation("date"))
        self.tree.heading("Type", text=self.settings_viewmodel.get_translation("type"))
        self.tree.heading("Amount", text=self.settings_viewmodel.get_translation("amount"))
        self.tree.heading("Category", text=self.settings_viewmodel.get_translation("category"))
        self.edit_button.config(text=self.settings_viewmodel.get_translation("edit"))
        self.delete_button.config(text=self.settings_viewmodel.get_translation("delete"))
        self.load_transactions()

class EditTransactionWindow(tk.Toplevel):
    def __init__(self, master, viewmodel, transaction_values):
        super().__init__(master)
        self.master = master
        self.viewmodel = viewmodel
        self.transaction_values = transaction_values
        self.settings_viewmodel = SettingsViewModel(viewmodel.language)
        self.title(self.settings_viewmodel.get_translation("edit_transaction"))
        self.geometry("400x300")
        self.init_ui()

    def init_ui(self):
        self.label = tk.Label(self, text=self.settings_viewmodel.get_translation("edit_transaction"), font=("Arial", 16))
        self.label.pack(pady=10)

        self.category_var = tk.StringVar(value=self.transaction_values[4])
        self.amount_var = tk.StringVar(value=self.transaction_values[3])
        self.date_var = tk.StringVar(value=self.transaction_values[1])
        self.type_var = tk.StringVar(value=self.transaction_values[2])

        fields = [
            (self.settings_viewmodel.get_translation("category"), self.category_var),
            (self.settings_viewmodel.get_translation("amount"), self.amount_var),
            (self.settings_viewmodel.get_translation("date"), self.date_var),
            (self.settings_viewmodel.get_translation("type"), self.type_var),
        ]
        self.field_widgets = []
        for label, var in fields:
            lbl = tk.Label(self, text=label)
            lbl.pack(anchor="w", padx=10)
            entry = tk.Entry(self, textvariable=var)
            entry.pack(fill="x", padx=10, pady=5)
            self.field_widgets.append((lbl, entry))

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=10)

        self.save_button = tk.Button(self.button_frame, text=self.settings_viewmodel.get_translation("save"), command=self.save_transaction)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = tk.Button(self.button_frame, text=self.settings_viewmodel.get_translation("cancel"), command=self.destroy)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

    def save_transaction(self):
        category = self.category_var.get().strip()
        amount = self.amount_var.get().strip()
        date = self.date_var.get().strip()
        type_ = self.type_var.get().strip()
        if not category or not amount or not date or not type_:
            messagebox.showerror(self.settings_viewmodel.get_translation("validation_error"), self.settings_viewmodel.get_translation("validation_error"))
            return
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror(self.settings_viewmodel.get_translation("validation_error"), self.settings_viewmodel.get_translation("amount_error"))
            return

        transaction_id = self.transaction_values[0]
        self.viewmodel.update_transaction(transaction_id, type_, category, amount, date)
        self.master.refresh_ui()
        self.destroy()