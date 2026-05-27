from BankAccount import BankAccount

class SavingAccount(BankAccount):

    NO_MONTHLY_FEE = 0

    # Initializes a saving account with an ID, balance, and annual interest rate.
    def __init__(self, account_id, balance, interest_rate):
        super().__init__(account_id, balance)
        self._interest_rate = interest_rate

    # Returns the annual interest rate of the account.
    def get_interest_rate(self):
        return self._interest_rate

    # Checks if this saving account has the same properties as another.
    def __eq__(self, other):
        if not isinstance(other, SavingAccount):
            return NotImplemented

        return super().__eq__(other) and  self._interest_rate == other.get_interest_rate()

    # Returns a string representation of the saving account's details.
    def __str__(self):
        return f"{super().__str__()}, interest_rate: {self._interest_rate}"

    # Returns the monthly management fee for the saving account (exempt from fees).
    def monthly_fee(self):
        return SavingAccount.NO_MONTHLY_FEE