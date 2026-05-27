from BankAccount import BankAccount

class CheckingAccount(BankAccount):

    MINUS = 0
    MINUS_FEE_RATE = 0.05

    def __init__(self, account_id, balance, overdraft_limit = 0):
        super().__init__(account_id, balance)
        self._overdraft_limit = overdraft_limit

    def get_overdraft_limit(self, overdraft_limit):
        self._overdraft_limit = overdraft_limit

    def __eq__(self, other):
        if not isinstance(other, CheckingAccount):
            return NotImplemented

        return super().__eq__(other) and  self._overdraft_limit == other.get_overdraft_limit()

    def __str__(self):
        return f"{super().__str__()}, overdraft_limit: {self._overdraft_limit}"

    def monthly_fee(self):
        if self.get_balance() < CheckingAccount.MINUS: return super().monthly_fee() - (self.get_balance() * CheckingAccount.MINUS_FEE_RATE)
        return super().monthly_fee()