import tkinter as tk
from tkinter import messagebox
from viewmodels.settings_viewmodel import SettingsViewModel

class SettingsView(tk.Toplevel):
    def __init__(self, master, viewmodel):
        super().__init__(master)
        self.viewmodel = viewmodel
        self.settings_viewmodel = SettingsViewModel(viewmodel.language)
        self.title(self.settings_viewmodel.get_translation("settings"))
        self.geometry("400x200")
        self.init_ui()

    def init_ui(self):
        tk.Label(self, text=self.settings_viewmodel.get_translation("language_settings")).pack(pady=20)
        tk.Button(self, text="English", command=lambda: self.set_language("en")).pack(pady=5)
        tk.Button(self, text="Türkçe", command=lambda: self.set_language("tr")).pack(pady=5)

    def set_language(self, lang):
        self.settings_viewmodel.set_language(lang)
        self.viewmodel.set_language(lang)
        language_name = "English" if lang == "en" else "Türkçe"
        messagebox.showinfo(self.settings_viewmodel.get_translation("language_changed", language=language_name), self.settings_viewmodel.get_translation("language_changed", language=language_name))