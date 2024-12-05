TRANSLATIONS = {
    "en": {
        "title": "Personal Finance Manager",
        "add_income": "Add Income",
        "add_expense": "Add Expense",
        "view_transactions": "View Transactions",
        "budget_overview": "Budget Overview",
        "settings": "Settings",
        "add_transaction": "Add {type}",
        "edit_transaction": "Edit Transaction",
        "category": "Category",
        "amount": "Amount",
        "date": "Date (YYYY-MM-DD)",
        "type": "Type",
        "save": "Save",
        "cancel": "Cancel",
        "success": "{type} added successfully!",
        "transaction_deleted": "Transaction deleted successfully!",
        "validation_error": "All fields are required!",
        "amount_error": "Amount must be a valid number!",
        "language_changed": "Language set to {language}!",
        "generate_chart": "Generate Chart",
        "language_settings": "Language Settings",
        "edit": "Edit",
        "delete": "Delete",
        "warning": "Warning",
        "select_transaction": "Please select a transaction to edit or delete."
    },
    "tr": {
        "title": "Kişisel Finans Yöneticisi",
        "add_income": "Gelir Ekle",
        "add_expense": "Gider Ekle",
        "view_transactions": "Hareketleri Görüntüle",
        "budget_overview": "Bütçe Genel Görünümü",
        "settings": "Ayarlar",
        "add_transaction": "{type} Ekle",
        "edit_transaction": "İşlemi Düzenle",
        "category": "Kategori",
        "amount": "Tutar",
        "date": "Tarih (YYYY-AA-GG)",
        "type": "Tür",
        "save": "Kaydet",
        "cancel": "İptal",
        "success": "{type} başarıyla eklendi!",
        "transaction_deleted": "İşlem başarıyla silindi!",
        "validation_error": "Tüm alanlar doldurulmalıdır!",
        "amount_error": "Tutar geçerli bir sayı olmalıdır!",
        "language_changed": "Dil {language} olarak ayarlandı!",
        "generate_chart": "Grafik Oluştur",
        "language_settings": "Dil Ayarları",
        "edit": "Düzenle",
        "delete": "Sil",
        "warning": "Uyarı",
        "select_transaction": "Lütfen düzenlemek veya silmek için bir işlem seçin."
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