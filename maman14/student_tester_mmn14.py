# Test Suite for MMN14 - Bank Account System

#from bank_account import BankAccount
#from saving_account import SavingAccount
#from checking_account import CheckingAccount
#from business_account import BusinessAccount
from mmn14 import *

# ============== TEST FUNCTIONS ==============

def test_bank_account_class():
    print("=" * 60)
    print("TESTING BankAccount CLASS")
    print("=" * 60)

    passed = 0
    failed = 0

    try:
        acc1 = BankAccount(1, 100)
        print("✓ PASS: constructor")
        passed += 1
    except Exception as e:
        print(f"✗ FAIL: constructor - {e}")
        return 0, 1

    # get_account_id
    try:
        if acc1.get_account_id() == 1:
            print("✓ PASS: get_account_id")
            passed += 1
        else:
            print("✗ FAIL: get_account_id")
            failed += 1
    except Exception as e:
        print(f"✗ FAIL: get_account_id - {e}")
        failed += 1

    # get_balance (should be 100!)
    try:
        if acc1.get_balance() == 100:
            print("✓ PASS: get_balance")
            passed += 1
        else:
            print("✗ FAIL: get_balance")
            failed += 1
    except Exception as e:
        print(f"✗ FAIL: get_balance - {e}")
        failed += 1

    # monthly_fee
    try:
        if acc1.monthly_fee() == 10:
            print("✓ PASS: monthly_fee")
            passed += 1
        else:
            print("✗ FAIL: monthly_fee")
            failed += 1
    except Exception as e:
        print(f"✗ FAIL: monthly_fee - {e}")
        failed += 1

    # __eq__
    try:
        acc2 = BankAccount(1, 100)
        if acc1 == acc2:
            print("✓ PASS: __eq__")
            passed += 1
        else:
            print("✗ FAIL: __eq__")
            failed += 1
    except Exception as e:
        print(f"✗ FAIL: __eq__ - {e}")
        failed += 1

    print(f"\nBankAccount summary: {passed} passed, {failed} failed\n")
    return passed, failed


def test_saving_account_class():
    print("=" * 60)
    print("TESTING SavingAccount CLASS")
    print("=" * 60)

    passed = 0
    failed = 0

    try:
        acc = SavingAccount(2, 200, 0.05)
        print("✓ PASS: constructor")
        passed += 1
    except Exception as e:
        print(f"✗ FAIL: constructor - {e}")
        return 0, 1

    try:
        if acc.monthly_fee() == 0:
            print("✓ PASS: monthly_fee")
            passed += 1
        else:
            print("✗ FAIL: monthly_fee")
            failed += 1
    except Exception as e:
        print(f"✗ FAIL: monthly_fee - {e}")
        failed += 1

    try:
        acc2 = SavingAccount(2, 200, 0.05)
        if acc == acc2:
            print("✓ PASS: __eq__")
            passed += 1
        else:
            print("✗ FAIL: __eq__")
            failed += 1
    except Exception as e:
        print(f"✗ FAIL: __eq__ - {e}")
        failed += 1

    print(f"\nSavingAccount summary: {passed} passed, {failed} failed\n")
    return passed, failed


def test_checking_account_class():
    print("=" * 60)
    print("TESTING CheckingAccount CLASS")
    print("=" * 60)

    passed = 0
    failed = 0

    try:
        acc = CheckingAccount(3, -100, 500)
        print("✓ PASS: constructor")
        passed += 1
    except Exception as e:
        print(f"✗ FAIL: constructor - {e}")
        return 0, 1

    try:
        if acc.monthly_fee() == 15:
            print("✓ PASS: monthly_fee (15% overdraft fee applied)")
            passed += 1
        else:
            print("✗ FAIL: monthly_fee")
            failed += 1
    except Exception as e:
        print(f"✗ FAIL: monthly_fee - {e}")
        failed += 1

    print(f"\nCheckingAccount summary: {passed} passed, {failed} failed\n")
    return passed, failed


def test_business_account_class():
    print("=" * 60)
    print("TESTING BusinessAccount CLASS")
    print("=" * 60)

    passed = 0
    failed = 0

    try:
        acc = BusinessAccount(4, 1000, "ABC", 20000, True)
        print("✓ PASS: constructor")
        passed += 1
    except Exception as e:
        print(f"✗ FAIL: constructor - {e}")
        return 0, 1

    try:
        if acc.monthly_fee() == 80:
            print("✓ PASS: monthly_fee")
            passed += 1
        else:
            print("✗ FAIL: monthly_fee")
            failed += 1
    except Exception as e:
        print(f"✗ FAIL: monthly_fee - {e}")
        failed += 1

    print(f"\nBusinessAccount summary: {passed} passed, {failed} failed\n")
    return passed, failed


# ---------------- FUNCTIONS ----------------

def test_average_fee():
    print("=" * 60)
    print("TESTING average_fee()")
    print("=" * 60)

    passed = 0
    failed = 0

    try:
        accounts = [
            BankAccount(1, 100),
            SavingAccount(2, 200, 0.05),
            CheckingAccount(3, -100, 500)
        ]

        result = average_fee(accounts)

        if result >= 0:
            print("✓ PASS: average_fee")
            passed += 1
        else:
            print("✗ FAIL: average_fee")
            failed += 1
    except Exception as e:
        print(f"✗ FAIL: average_fee - {e}")
        failed += 1

    return passed, failed


def test_how_many_tax_exempt():
    print("=" * 60)
    print("TESTING how_many_tax_exempt()")
    print("=" * 60)

    passed = 0
    failed = 0

    try:
        accounts = [
            BusinessAccount(1, 1000, "A" , 20000, True),
            BusinessAccount(2, 2000, "B", 20000),
        ]

        result = how_many_tax_exempt(accounts)

        if result == 1:  # second BusinessAccount is False by default
            print("✓ PASS: how_many_tax_exempt")
            passed += 1
        else:
            print("✗ FAIL: how_many_tax_exempt")
            failed += 1
    except Exception as e:
        print(f"✗ FAIL: how_many_tax_exempt - {e}")
        failed += 1

    return passed, failed


def test_account_type():
    print("=" * 60)
    print("TESTING account_type()")
    print("=" * 60)

    passed = 0
    failed = 0

    try:
        accounts = [
            BankAccount(1, 100),
            SavingAccount(2, 200, 0.05),
            CheckingAccount(3, -100, 500),
            BusinessAccount(4, 1000, "ABC", 20000, True)
        ]

        result = account_type(accounts)

        if isinstance(result, dict) and len(result) == 4:
            print("✓ PASS: account_type")
            passed += 1
        else:
            print("✗ FAIL: account_type")
            failed += 1
    except Exception as e:
        print(f"✗ FAIL: account_type - {e}")
        failed += 1

    return passed, failed


def test_top_balance():
    print("=" * 60)
    print("TESTING top_balance()")
    print("=" * 60)

    passed = 0
    failed = 0

    try:
        accounts = [
            BankAccount(1, 100),
            BankAccount(2, 200)
        ]

        result = top_balance(accounts)

        if result is not None:
            print("✓ PASS: top_balance")
            passed += 1
        else:
            print("✗ FAIL: top_balance")
            failed += 1
    except Exception as e:
        print(f"✗ FAIL: top_balance - {e}")
        failed += 1

    return passed, failed


def test_only_positive_balance():
    print("=" * 60)
    print("TESTING only_positive_balance()")
    print("=" * 60)

    passed = 0
    failed = 0

    try:
        accounts = [
            BankAccount(1, 100),
            SavingAccount(2, 200, 0.05)
        ]

        result = only_positive_balance(accounts)

        if len(result) == 1:
            print("✓ PASS: only_positive_balance")
            passed += 1
        else:
            print("✗ FAIL: only_positive_balance")
            failed += 1
    except Exception as e:
        print(f"✗ FAIL: only_positive_balance - {e}")
        failed += 1

    return passed, failed


# ============== RUN ALL ==============

def run_all_tests():
    results = {}

    results['BankAccount'] = test_bank_account_class()
    results['SavingAccount'] = test_saving_account_class()
    results['CheckingAccount'] = test_checking_account_class()
    results['BusinessAccount'] = test_business_account_class()

    results['average_fee'] = test_average_fee()
    results['how_many_tax_exempt'] = test_how_many_tax_exempt()
    results['account_type'] = test_account_type()
    results['top_balance'] = test_top_balance()
    results['only_positive_balance'] = test_only_positive_balance()

    print("\nFINAL SUMMARY\n" + "=" * 50)

    total_p, total_f = 0, 0

    for name, (p, f) in results.items():
        print(f"{name}: {p} passed, {f} failed")
        total_p += p
        total_f += f

    print("\nTOTAL:", total_p, "passed,", total_f, "failed")


if __name__ == "__main__":
    run_all_tests()