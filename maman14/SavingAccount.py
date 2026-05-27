from BankAccount import BankAccount

class SavingAccount(BankAccount):

    NO_MONTHLY_FEE = 0

    def __init__(self, account_id, balance, interest_rate):
        super().__init__(account_id, balance)
        self._interest_rate = interest_rate

    def get_interest_rate(self):
        return self._interest_rate

    def __eq__(self, other):
        if not isinstance(other, SavingAccount):
            return NotImplemented

        return super().__eq__(other) and  self._interest_rate == other.get_interest_rate()

    def __str__(self):
        return f"{super().__str__()}, interest_rate: {self._interest_rate}"

    def monthly_fee(self):
        return SavingAccount.NO_MONTHLY_FEE