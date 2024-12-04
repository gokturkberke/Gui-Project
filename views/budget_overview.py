import tkinter as tk
from tkinter import ttk

class BudgetOverview(tk.Toplevel):
    def __init__(self, master, viewmodel):
        super().__init__(master)
        self.master = master
        self.viewmodel = viewmodel
        self.title(self.get_translation("budget_overview"))
        self.geometry("600x400")
        self.init_ui()

    def init_ui(self):
        self.tree = ttk.Treeview(self, columns=("Category", "Allocated", "Spent", "Remaining"), show='headings')
        self.tree.heading("Category", text=self.get_translation("category"))
        self.tree.heading("Allocated", text=self.get_translation("allocated"))
        self.tree.heading("Spent", text=self.get_translation("spent"))
        self.tree.heading("Remaining", text=self.get_translation("remaining"))

        budget_data = self.viewmodel.get_budget_overview()
        for category, data in budget_data.items():
            self.tree.insert("", "end", values=(category, data['allocated'], data['spent'], data['remaining']))

        self.tree.pack(expand=True, fill='both')

    def get_translation(self, key, **kwargs):
        return self.viewmodel.get_translation(key, **kwargs)

    def refresh_ui(self):
        self.title(self.get_translation("budget_overview"))
        self.tree.heading("Category", text=self.get_translation("category"))
        self.tree.heading("Allocated", text=self.get_translation("allocated"))
        self.tree.heading("Spent", text=self.get_translation("spent"))
        self.tree.heading("Remaining", text=self.get_translation("remaining"))