TRANSLATIONS = {
    "en": {
        "title": "Personal Finance Manager",
        "add_income": "Add Income",
        "add_expense": "Add Expense",
        "view_transactions": "View Transactions",
        "budget_overview": "Budget Overview",
        "settings": "Settings",
        "add_transaction": "Add {type}",
        "category": "Category",
        "amount": "Amount",
        "date": "Date (YYYY-MM-DD)",
        "save": "Save",
        "success": "{type} added successfully!",
        "validation_error": "All fields are required!",
        "amount_error": "Amount must be a valid number!",
        "language_changed": "Language set to {language}!",
        "generate_chart": "Generate Chart",
        "language_settings": "Language Settings",
    },
    "tr": {
        "title": "Kişisel Finans Yöneticisi",
        "add_income": "Gelir Ekle",
        "add_expense": "Gider Ekle",
        "view_transactions": "Hareketleri Görüntüle",
        "budget_overview": "Bütçe Genel Görünümü",
        "settings": "Ayarlar",
        "add_transaction": "{type} Ekle",
        "category": "Kategori",
        "amount": "Tutar",
        "date": "Tarih (YYYY-AA-GG)",
        "save": "Kaydet",
        "success": "{type} başarıyla eklendi!",
        "validation_error": "Tüm alanlar doldurulmalıdır!",
        "amount_error": "Tutar geçerli bir sayı olmalıdır!",
        "language_changed": "Dil {language} olarak ayarlandı!",
        "generate_chart": "Grafik Oluştur",
        "language_settings": "Dil Ayarları",
    }
}

class SettingsViewModel:
    def __init__(self, language="en"):
        self.language = language

    def set_language(self, lang):
        self.language = lang

    def get_translation(self, key, **kwargs):
        translation = TRANSLATIONS.get(self.language, {}).get(key, key)
        try:
            return translation.format(**kwargs)
        except KeyError:
            return translation