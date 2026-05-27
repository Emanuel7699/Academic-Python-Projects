from BankAccount import BankAccount

class CheckingAccount(BankAccount):

    MINUS = 0
    MINUS_FEE_RATE = 0.05

    # Initializes a checking account with an ID, balance, and an optional overdraft limit.
    def __init__(self, account_id, balance, overdraft_limit = 0):
        super().__init__(account_id, balance)
        self._overdraft_limit = overdraft_limit

    # Returns the overdraft limit of the account.
    def get_overdraft_limit(self):
        return self._overdraft_limit

    # Checks if this checking account has the same properties as another.
    def __eq__(self, other):
        if not isinstance(other, CheckingAccount):
            return NotImplemented

        return super().__eq__(other) and  self._overdraft_limit == other.get_overdraft_limit()

    # Returns a string representation of the checking account's details.
    def __str__(self):
        return f"{super().__str__()}, overdraft_limit: {self._overdraft_limit}"

    # Returns the monthly management fee, including a penalty if the balance is negative.
    def monthly_fee(self):
        if self.get_balance() < CheckingAccount.MINUS: return super().monthly_fee() - (self.get_balance() * CheckingAccount.MINUS_FEE_RATE)
        return super().monthly_fee()