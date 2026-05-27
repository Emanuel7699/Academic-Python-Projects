class BankAccount:

    BASIC_MONTHLY_FEE = 10

    # Initializes a new bank account with an ID and an optional initial balance.
    def __init__(self, account_id, balance = 0):
        self._account_id = account_id
        self._balance = balance

    # Returns the current balance of the account.
    def get_balance(self):
        return self._balance

    # Returns the account ID.
    def get_account_id(self):
        return self._account_id

    # Checks if this account has the same ID and balance as another account.
    def __eq__(self, other):
        if not isinstance(other, BankAccount):
            return NotImplemented

        return self._account_id == other.get_account_id() and self._balance == other.get_balance()

    # Returns a string representation of the account's details.
    def __str__(self):
        return f"account_id: {self._account_id}, balance: {str(self._balance)}"

    # Returns the basic monthly management fee for the bank account.
    def monthly_fee(self):
        return BankAccount.BASIC_MONTHLY_FEE