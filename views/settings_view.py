import tkinter as tk
from tkinter import messagebox

class SettingsView(tk.Toplevel):
    def __init__(self, master, viewmodel):
        super().__init__(master)
        self.viewmodel = viewmodel
        self.title("Settings")
        self.geometry("400x200")
        self.init_ui()

    def init_ui(self):
        tk.Label(self, text="Language Settings").pack(pady=20)
        tk.Button(self, text="English", command=lambda: self.set_language("en")).pack(pady=5)
        tk.Button(self, text="Türkçe", command=lambda: self.set_language("tr")).pack(pady=5)

    def set_language(self, lang):
        self.viewmodel.set_language(lang)
        language_name = "English" if lang == "en" else "Türkçe"
        messagebox.showinfo("Language Changed", f"Language set to {language_name}!")