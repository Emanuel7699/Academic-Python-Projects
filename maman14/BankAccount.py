class BankAccount:

    BASIC_MONTHLY_FEE = 10

    def __init__(self, account_id, balance = 0):
        self.account_id = account_id
        self.balance = balance

    def get_balance(self):
        return self.balance

    def get_account_id(self):
        return self.account_id


    def __eq__(self, other):
        if not isinstance(other, BankAccount):
            return NotImplemented

        return self.account_id == other.account_id and self.balance == other.balance

    def __str__(self):
        return f"account_id: {self.account_id}, balance: {str(self.balance)}"

    def monthly_fee(self):
        return BankAccount.BASIC_MONTHLY_FEE