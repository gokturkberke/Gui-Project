import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from viewmodels.settings_viewmodel import SettingsViewModel
import re #match regular expressions
from tkinter import filedialog
from fpdf import FPDF


class TransactionViewer(ttk.Toplevel):
    def __init__(self, master, viewmodel):
        super().__init__(master)
        self.master = master
        self.viewmodel = viewmodel
        self.settings_viewmodel = SettingsViewModel(viewmodel.language)
        self.title(self.settings_viewmodel.get_translation("view_transactions"))
        self.geometry("800x400")
        self.minsize(800,400)
        self.transactions = self.load_transactions()
        self.translate_categories()
        self.init_ui()

    def init_ui(self):
        self.tree = ttk.Treeview(self, columns=("ID", "Date", "Type", "Amount", "Category"), show='headings')
        self.tree.heading("ID", text="ID", command=lambda: self.sort_tree("ID", False))
        self.tree.heading("Date", text=self.settings_viewmodel.get_translation("date"), command=lambda: self.sort_tree("Date", False))
        self.tree.heading("Type", text=self.settings_viewmodel.get_translation("type"), command=lambda: self.sort_tree("Type", False))
        self.tree.heading("Amount", text=self.settings_viewmodel.get_translation("amount"), command=lambda: self.sort_tree("Amount", False))
        self.tree.heading("Category", text=self.settings_viewmodel.get_translation("category"), command=lambda: self.sort_tree("Category", False))

        self.tree.column("ID", width=50, anchor=ttk.CENTER)
        self.tree.column("Date", width=100, anchor=ttk.CENTER)
        self.tree.column("Type", width=100, anchor=ttk.CENTER)
        self.tree.column("Amount", width=100, anchor=ttk.CENTER)
        self.tree.column("Category", width=100, anchor=ttk.CENTER)

        self.tree.pack(expand=True, fill='both')
        
        # Bind the click event to deselect the row
        self.tree.bind("<Button-1>", self.on_tree_click)

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=10)

        self.edit_button = ttk.Button(self.button_frame, text=self.settings_viewmodel.get_translation("edit"), command=self.edit_transaction)
        self.edit_button.pack(side=ttk.LEFT, padx=5)

        self.delete_button = ttk.Button(self.button_frame, text=self.settings_viewmodel.get_translation("delete"), command=self.delete_transaction)
        self.delete_button.pack(side=ttk.LEFT, padx=5)

        self.export_pdf_button = ttk.Button(self.button_frame, text=self.settings_viewmodel.get_translation("export_to_pdf"), command=self.export_to_pdf)
        self.export_pdf_button.pack(side=ttk.LEFT, padx=5)

        self.load_data()

    def load_transactions(self):
        return self.viewmodel.get_transactions()

    def translate_categories(self):
        for transaction in self.transactions:
            transaction.category = self.viewmodel.translate_category(transaction.category)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for transaction in self.transactions:
            transaction_type = self.settings_viewmodel.get_translation(transaction.type.lower())
            self.tree.insert("", "end", values=(transaction.id, transaction.date, transaction_type, transaction.amount, transaction.category))

    def export_to_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return

        transactions = self.viewmodel.get_transactions()

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Transaction Report", ln=True, align="C")

        # Table Header
        pdf.set_font("Arial", style="B", size=10)
        pdf.cell(10, 10, "ID", border=1)
        pdf.cell(40, 10, "Date", border=1)
        pdf.cell(30, 10, "Type", border=1)
        pdf.cell(30, 10, "Amount (USD)", border=1)
        pdf.cell(50, 10, "Category", border=1)
        pdf.ln()

        # Table Content
        pdf.set_font("Arial", size=10)
        for transaction in transactions:
            amount = -transaction.amount if transaction.type == "Expense" else transaction.amount
            pdf.cell(10, 10, str(transaction.id), border=1)
            pdf.cell(40, 10, transaction.date, border=1)
            pdf.cell(30, 10, transaction.type, border=1)
            pdf.cell(30, 10, f"${amount:,.2f}", border=1)  # Negative amount for expenses
            pdf.cell(50, 10, transaction.category, border=1)
            pdf.ln()

        pdf.output(file_path)
        Messagebox.show_info("Export Successful", "Transactions exported to PDF successfully!")

    def sort_tree(self, col, reverse):
        if col.lower() == "amount":
            l = [(float(self.tree.set(k, col)), k) for k in self.tree.get_children("")]
        elif col.lower() == "category":
                l = [(self.tree.set(k, col).lower(), k) for k in self.tree.get_children("")]
        elif col.lower() == "id":
            l = [(int(self.tree.set(k, col)), k) for k in self.tree.get_children("")]
        else:
            l = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            self.tree.move(k, "", index)
        self.tree.heading(col, command=lambda: self.sort_tree(col, not reverse))

    def edit_transaction(self):
        selected_item = self.tree.selection()
        if not selected_item:
            Messagebox.show_warning(
                title=self.settings_viewmodel.get_translation("warning"),
                message=self.settings_viewmodel.get_translation("select_transaction"),
                alert=True,
                width=400,
                height=200
            )
            return

        transaction_values = self.tree.item(selected_item, "values")
        EditTransactionWindow(self, self.viewmodel, transaction_values)

    def delete_transaction(self):
        selected_item = self.tree.selection()
        if not selected_item:
            Messagebox.show_warning(
                title=self.settings_viewmodel.get_translation("warning"),
                message=self.settings_viewmodel.get_translation("select_transaction"),
                alert=True,
                width=400,
                height=200
            )
            return

        transaction_id = self.tree.item(selected_item, "values")[0]
        self.viewmodel.delete_transaction(transaction_id)
        self.tree.delete(selected_item)
        Messagebox.show_info(self.settings_viewmodel.get_translation("delete_trans"), self.settings_viewmodel.get_translation("transaction_deleted"))

    def refresh_ui(self):
        self.title(self.settings_viewmodel.get_translation("view_transactions"))
        self.tree.heading("Date", text=self.settings_viewmodel.get_translation("date"))
        self.tree.heading("Type", text=self.settings_viewmodel.get_translation("type"))
        self.tree.heading("Amount", text=self.settings_viewmodel.get_translation("amount"))
        self.tree.heading("Category", text=self.settings_viewmodel.get_translation("category"))
        self.edit_button.config(text=self.settings_viewmodel.get_translation("edit"))
        self.delete_button.config(text=self.settings_viewmodel.get_translation("delete"))
        self.load_data()

    def on_tree_click(self, event):
        if not self.tree.identify_row(event.y):
            self.tree.selection_remove(self.tree.selection())

class EditTransactionWindow(ttk.Toplevel):
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
        self.category_var = ttk.StringVar(value=self.transaction_values[4])
        self.amount_var = ttk.StringVar(value=self.transaction_values[3])
        # Replace StringVar with DateEntry 
        self.date_entry = ttk.DateEntry(self, firstweekday=0, bootstyle="primary")
        # Set initial date value
        self.date_entry.entry.delete(0, "end")
        self.date_entry.entry.insert(0, self.transaction_values[1])
        
        self.type_var = ttk.StringVar(value=self.transaction_values[2])
        self.type_options = ["Expense", "Income"]

        # Category field
        lbl_category = ttk.Label(self, text=self.settings_viewmodel.get_translation("category"))
        lbl_category.pack(anchor="w", padx=10)
        entry_category = ttk.Entry(self, textvariable=self.category_var)
        entry_category.pack(fill="x", padx=10, pady=5)

        # Amount field
        lbl_amount = ttk.Label(self, text=self.settings_viewmodel.get_translation("amount")) 
        lbl_amount.pack(anchor="w", padx=10)
        entry_amount = ttk.Entry(self, textvariable=self.amount_var)
        entry_amount.pack(fill="x", padx=10, pady=5)

        # Date field
        lbl_date = ttk.Label(self, text=self.settings_viewmodel.get_translation("date"))
        lbl_date.pack(anchor="w", padx=10)
        self.date_entry.pack(fill="x", padx=10, pady=5)

        # Type field
        lbl_type = ttk.Label(self, text=self.settings_viewmodel.get_translation("type"))
        lbl_type.pack(anchor="w", padx=10)
        type_combo = ttk.Combobox(self, textvariable=self.type_var, values=self.type_options, state="readonly")
        type_combo.pack(fill="x", padx=10, pady=5)

        # Button frame
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=10)

        self.save_button = ttk.Button(self.button_frame, text=self.settings_viewmodel.get_translation("save"), command=self.save_transaction)
        self.save_button.pack(side=ttk.LEFT, padx=5)

        self.cancel_button = ttk.Button(self.button_frame, text=self.settings_viewmodel.get_translation("cancel"), command=self.destroy)
        self.cancel_button.pack(side=ttk.LEFT, padx=5)

    def save_transaction(self):
        category = self.category_var.get().strip()
        amount = self.amount_var.get().strip()
        date = self.date_entry.entry.get().strip()
        type_ = self.type_var.get().strip()
        
        if not category or not amount or not date or not type_:
            Messagebox.show_error(self.settings_viewmodel.get_translation("validation_error"), self.settings_viewmodel.get_translation("validation_error"))
            return
        
        if not re.match(r"^[A-Za-z\s]+$", category):
            Messagebox.show_error(self.settings_viewmodel.get_translation("validation_error"), self.settings_viewmodel.get_translation("category_error"))
            return
        
        try:
            amount = float(amount)
        except ValueError:
            Messagebox.show_error(self.settings_viewmodel.get_translation("validation_error"), self.settings_viewmodel.get_translation("amount_error"))
            return

        transaction_id = self.transaction_values[0]
        self.viewmodel.update_transaction(transaction_id, type_, category, amount, date)
        self.master.refresh_ui()
        self.destroy()