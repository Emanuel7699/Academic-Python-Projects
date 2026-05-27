from BusinessAccount import BusinessAccount
from SavingAccount import SavingAccount
from CheckingAccount import CheckingAccount
from BankAccount import BankAccount

def average_fee(accounts):
    if not accounts:
        return 0

    total_fee = 0
    for account in accounts:
        total_fee += account.monthly_fee()

    return total_fee / len(accounts)

def how_many_tax_exempt(accounts):
    count = 0
    for account in accounts:
        if isinstance(account, BusinessAccount):
            if account.get_is_tax_exempt(): count += 1
    return count

def account_type(accounts):
    grades = {"BankAccount": 0, "SavingAccount": 0, "CheckingAccount": 0, "BusinessAccount": 0}
    for account in accounts:
        grades[type(account).__name__] +=1
    return grades

def top_balance(accounts):
    if not accounts:
        return None

    maximum = accounts[0].get_balance()
    for account in accounts:
        if account.get_balance() > maximum:
            maximum = account.balance
    return maximum


def only_positive_balance(accounts):
    positive_accounts = []

    for account in accounts:
        if not isinstance(account, SavingAccount) and account.get_balance() > 0:
            positive_accounts.append(account)

    if len(positive_accounts) == 0:
        return None

    return positive_accounts