import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from viewmodels.settings_viewmodel import SettingsViewModel

class SettingsView(ttk.Toplevel):
    def __init__(self, master, viewmodel):
        super().__init__(master)
        self.master = master
        self.viewmodel = viewmodel
        self.settings_viewmodel = SettingsViewModel(viewmodel.language)
        self.title(self.settings_viewmodel.get_translation("settings"))
        self.geometry("400x200")
        self.resizable(False, False)
        self.init_ui()

    def init_ui(self):
        self.label = ttk.Label(self, text=self.settings_viewmodel.get_translation("language_settings"))
        self.label.pack(pady=20)
        self.english_button = ttk.Button(self, text="English", command=lambda: self.set_language("en"))
        self.english_button.pack(pady=5)
        self.turkish_button = ttk.Button(self, text="Türkçe", command=lambda: self.set_language("tr"))
        self.turkish_button.pack(pady=5)

    def set_language(self, lang):
        self.settings_viewmodel.set_language(lang)
        self.viewmodel.set_language(lang)
        language_name = self.settings_viewmodel.get_translation("language")
        Messagebox.show_info(self.settings_viewmodel.get_translation("language_changed", language=language_name), self.settings_viewmodel.get_translation("language_changed", language=language_name))
        if self.master.winfo_exists():
            self.master.refresh_ui()
        if self.winfo_exists():
            self.refresh_ui()

    def refresh_ui(self):
        if self.winfo_exists():
            self.title(self.settings_viewmodel.get_translation("settings"))
            self.label.config(text=self.settings_viewmodel.get_translation("language_settings"))
            self.english_button.config(text="English")
            self.turkish_button.config(text="Türkçe")