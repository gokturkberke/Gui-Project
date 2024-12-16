import glob

class I18N:
    def __init__(self, language_code):
        if language_code in self.get_available_languages():
            self.translations = self.load_data_from_file(language_code)
        else:
            raise NotImplementedError("Unsupported language. Add missing language file.")

    @staticmethod
    def get_available_languages():
        language_files = glob.glob("*.lng")
        language_codes = []

        for f in language_files:
            language_code = f.replace("data_", "").replace(".lng", "")
            language_codes.append(language_code)

        return language_codes

    @staticmethod
    def load_data_from_file(language_code):
        language_file = f"data_{language_code}.lng"
        language_data = {}
        try:
            with open(language_file, encoding="utf-8") as f:
                for line in f:
                    (key, val) = line.strip().split("=")
                    language_data[key] = val
        except FileNotFoundError:
            raise ValueError("Language file not found.")

        return language_data

    @staticmethod
    def get_language_name(language_code):
        language_file = f"data_{language_code}.lng"
        try:
            with open(language_file, encoding="utf-8") as f:
                for line in f:
                    (key, val) = line.strip().split("=")
                    if key == "language":
                        return val

                raise ValueError("The language key was not found.")
        except FileNotFoundError:
            raise ValueError("Language file not found.")

TRANSLATIONS = {
    "en": {
        "category_error": "Category must contain only letters and spaces.",
        "date": "Date",
        "type": "Type",
        "category": "Category",
        "amount": "Amount",
        "Salary": "Salary",
        "Freelance Work": "Freelance Work",
        "Rental Income" : "Rental Income",
        "Gift Card": "Gift Card",
        "Housing - Rent": "Housing - Rent",
        "House Bills": "House Bills",
        "Car Fuel": "Car Fuel",
        "Car Maintenance": "Car Maintenance",
        "Transport pass": "Transport pass",
        "Food - Groceries": "Food - Groceries",
        "Dining Out": "Dining Out",
        "Healthcare": "Healthcare",
        "Education - Tuition": "Education - Tuition",
        "Saving Account": "Saving Account",
        "Online Subscriptions": "Online Subscriptions",
        "Credit Card Payment": "Credit Card Payment",
        "Clothing": "Clothing",
    },
    "tr": {
        "category_error": "Kategori sadece harfler ve boşluklar içermelidir.",
        "date": "Tarih",
        "type": "Tür",
        "category": "Kategori",
        "amount": "Miktar",
        "Salary": "Maaş",
        "Freelance Work": "Serbest Çalışma",
        "Rental Income" : "Kira Geliri",
        "Gift Card": "Hediye Kartı",
        "Housing - Rent": "Kira",
        "House Bills": "Ev Faturaları",
        "Car Fuel": "Araba Yakıtı",
        "Car Maintenance": "Araba Bakımı",
        "Transport pass": "Ulaşım Kartı",
        "Food - Groceries": "Yiyecek - Market",
        "Dining Out": "Dışarıda Yemek",
        "Healthcare": "Sağlık Hizmeti",
        "Education - Tuition": "Okul Ücreti",
        "Saving Account": "Tasarruf Hesabı",
        "Online Subscriptions": "Online Abonelikler",
        "Credit Card Payment": "Kredi Kartı Ödemesi",
        "Clothing": "Giyim",
    }
}

class SettingsViewModel:
    def __init__(self, language_code="en"):
        self.i18n = I18N(language_code)
        self.translations = self.i18n.translations

    def set_language(self, lang):
        self.i18n = I18N(lang)
        self.translations = self.i18n.translations

    def get_translation(self, key, **kwargs):
        translation = self.translations.get(key, key)
        try:
            return translation.format(**kwargs)
        except KeyError:
            return translation