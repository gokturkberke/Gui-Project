class TransactionViewModel:
    def __init__(self, transaction_id, amount, date, description):
        self.transaction_id = transaction_id
        self.amount = amount
        self.date = date
        self.description = description

    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'amount': self.amount,
            'date': self.date,
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            transaction_id=data.get('transaction_id'),
            amount=data.get('amount'),
            date=data.get('date'),
            description=data.get('description')
        )

    def __str__(self):
        return f"Transaction(id={self.transaction_id}, amount={self.amount}, date={self.date}, description={self.description})"