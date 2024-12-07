from models.translations import TRANSLATIONS

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