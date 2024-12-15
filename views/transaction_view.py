import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox

class TransactionView(ttk.Toplevel):
    def __init__(self, master, transaction_type, viewmodel):
        super().__init__(master)
        self.master = master
        self.viewmodel = viewmodel
        self.transaction_type = transaction_type
        self.title(self.get_translation("add_transaction", type=transaction_type))
        self.geometry("400x300")
        self.resizable(False, False)
        self.init_ui()

    def init_ui(self):
        self.label = ttk.Label(self, text=self.get_translation("add_transaction", type=self.transaction_type), font=("Arial", 16))
        self.label.pack(pady=10)
        
        self.category_var = ttk.StringVar()
        self.amount_var = ttk.StringVar()
        # Replace StringVar with DateEntry
        self.date_entry = ttk.DateEntry(self, firstweekday=0, bootstyle="primary")
        
        # Category field
        lbl_category = ttk.Label(self, text=self.get_translation("category"))
        lbl_category.pack(anchor="w", padx=10)
        entry_category = ttk.Entry(self, textvariable=self.category_var)
        entry_category.pack(fill="x", padx=10, pady=5)
        
        # Amount field  
        lbl_amount = ttk.Label(self, text=self.get_translation("amount"))
        lbl_amount.pack(anchor="w", padx=10)
        entry_amount = ttk.Entry(self, textvariable=self.amount_var)
        entry_amount.pack(fill="x", padx=10, pady=5)
        
        # Date field
        lbl_date = ttk.Label(self, text=self.get_translation("date"))
        lbl_date.pack(anchor="w", padx=10)
        self.date_entry.pack(fill="x", padx=10, pady=5)

        self.save_button = ttk.Button(self, text=self.get_translation("save"), command=self.save_transaction)
        self.save_button.pack(pady=20)

    def save_transaction(self):
        category = self.category_var.get().strip()
        amount = self.amount_var.get().strip()
        date = self.date_entry.entry.get().strip()
        if not category or not amount or not date:
            Messagebox.show_error(self.get_translation("validation_error"), self.get_translation("validation_error"))
            return
        try:
            amount = float(amount)
        except ValueError:
            Messagebox.show_error(self.get_translation("validation_error"), self.get_translation("amount_error"))
            return
        self.viewmodel.save_transaction(self.transaction_type, category, amount, date)
        success_msg = self.get_translation("success", type=self.transaction_type)
        Messagebox.show_info(success_msg, self.get_translation("success_title"))
        self.destroy()

    def get_translation(self, key, **kwargs):
        # Translate the transaction type if it exists
        if "type" in kwargs:
            kwargs["type"] = self.viewmodel.get_translation(kwargs["type"].lower())  # Translate 'income' or 'expense'
        return self.viewmodel.get_translation(key, **kwargs)

    def refresh_ui(self):
        self.title(self.get_translation("add_transaction", type=self.transaction_type))
        self.label.config(text=self.get_translation("add_transaction", type=self.transaction_type))
        fields = [
            (self.get_translation("category"), self.category_var),
            (self.get_translation("amount"), self.amount_var),
            (self.get_translation("date"), self.date_var),
        ]
        for (label, var), (lbl, entry) in zip(fields, self.field_widgets):
            lbl.config(text=label)
        self.save_button.config(text=self.get_translation("save"))