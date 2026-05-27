from CheckingAccount import CheckingAccount

class BusinessAccount(CheckingAccount):

    BUSINESS_MONTHLY_FEE = 100
    TAX_EXEMPT_DISCOUNT_RATE = 0.8

    def __init__(self, account_id, balance, business_name, overdraft_limit = 50000, is_tax_exempt = False):
        super().__init__(account_id, balance,overdraft_limit)
        self._business_name = business_name
        self._is_tax_exempt = is_tax_exempt

    def get_business_name(self):
        return self._business_name

    def get_is_tax_exempt(self):
        return self._is_tax_exempt

    def __eq__(self, other):
        if not isinstance(other, BusinessAccount):
            return NotImplemented

        return super().__eq__(other) and  self._business_name == other.get_business_name() and self._is_tax_exempt == other.get_is_tax_exempt

    def __str__(self):
        return f"{super().__str__()}, business_name: {self._business_name}, is_tax_exempt: {self._is_tax_exempt}"

    def monthly_fee(self):
        if self.get_is_tax_exempt(): return BusinessAccount.BUSINESS_MONTHLY_FEE * BusinessAccount.TAX_EXEMPT_DISCOUNT_RATE
        return self.get_balance() - BusinessAccount.BUSINESS_MONTHLY_FEE