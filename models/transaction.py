class Transaction:
    def __init__(self, type, category, amount, date, id=None):
        self.id = id
        self.type = type
        self.category = category
        self.amount = amount
        self.date = date