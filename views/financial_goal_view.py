import ttkbootstrap as ttk
from tkinter import messagebox
from viewmodels.main_viewmodel import MainViewModel
from viewmodels.settings_viewmodel import SettingsViewModel

class FinancialGoalView(ttk.Toplevel):
    def __init__(self, master, viewmodel):
        super().__init__(master)
        self.master = master
        self.viewmodel = viewmodel
        self.settings_viewmodel = SettingsViewModel(viewmodel.language)
        self.title(self.get_translation("financial_goal"))
        self.geometry("400x400")
        self.init_ui()

    def get_translation(self, key):
        return self.settings_viewmodel.get_translation(key)

    def submit_goal(self):
        goal = self.goal_entry.get()
        if self.viewmodel.set_financial_goal(goal):
            messagebox.showinfo("Success", f"Your financial goal of ${goal} has been set!")
        else:
            messagebox.showerror("Error", "Please enter a valid number.")
    
    def init_ui(self):
        self.goal_label = ttk.Label(self, text=self.get_translation("enter_your_financial_goal"))
        self.goal_label.pack(pady=10)

        self.goal_entry = ttk.Entry(self)
        self.goal_entry.pack(pady=10)

        self.submit_button = ttk.Button(self, text=self.get_translation("submit"), command=self.submit_goal)
        self.submit_button.pack(pady=10)