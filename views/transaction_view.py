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
        self.init_ui()

    def init_ui(self):
        self.label = ttk.Label(self, text=self.get_translation("add_transaction", type=self.transaction_type), font=("Arial", 16))
        self.label.pack(pady=10)
        self.category_var = ttk.StringVar()
        self.amount_var = ttk.StringVar()
        self.date_var = ttk.StringVar()
        fields = [
            (self.get_translation("category"), self.category_var),
            (self.get_translation("amount"), self.amount_var),
            (self.get_translation("date"), self.date_var),
        ]
        self.field_widgets = []
        for label, var in fields:
            lbl = ttk.Label(self, text=label)
            lbl.pack(anchor="w", padx=10)
            entry = ttk.Entry(self, textvariable=var)
            entry.pack(fill="x", padx=10, pady=5)
            self.field_widgets.append((lbl, entry))
        self.save_button = ttk.Button(self, text=self.get_translation("save"), command=self.save_transaction)
        self.save_button.pack(pady=20)

    def save_transaction(self):
        category = self.category_var.get().strip()
        amount = self.amount_var.get().strip()
        date = self.date_var.get().strip()
        if not category or not amount or not date:
            Messagebox.show_error(self.get_translation("validation_error"), self.get_translation("validation_error"))
            return
        try:
            amount = float(amount)
        except ValueError:
            Messagebox.show_error(self.get_translation("validation_error"), self.get_translation("amount_error"))
            return
        self.viewmodel.save_transaction(self.transaction_type, category, amount, date)
        Messagebox.show_info(self.get_translation("success"), self.get_translation("success", type=self.transaction_type))
        self.destroy()

    def get_translation(self, key, **kwargs):
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