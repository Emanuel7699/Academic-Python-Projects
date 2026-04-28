# Test Suite for All Functions
from mmn11 import *

import io
from unittest.mock import patch

# ============== TEST FUNCTIONS ==============

def test_calc():
    """Test the calc function with various inputs"""
    print("=" * 60)
    print("TESTING calc() FUNCTION")
    print("=" * 60)

    test_cases = [
        # Addition tests
        (5, 3, "+", 8, "Simple addition"),
        (0, 0, "+", 0, "Adding zeros"),
        (-5, 3, "+", -2, "Adding negative and positive"),
        (-5, -3, "+", -8, "Adding two negatives"),
        (100, 200, "+", 300, "Large numbers addition"),

        # Subtraction tests
        (10, 3, "-", 7, "Simple subtraction"),
        (3, 10, "-", -7, "Subtraction resulting in negative"),
        (0, 5, "-", -5, "Subtracting from zero"),
        (-5, -3, "-", -2, "Subtracting negatives"),
        (100, 100, "-", 0, "Subtracting equal numbers"),

        # Multiplication tests
        (5, 3, "*", 15, "Simple multiplication"),
        (0, 100, "*", 0, "Multiplying by zero"),
        (-5, 3, "*", -15, "Negative times positive"),
        (-5, -3, "*", 15, "Negative times negative"),
        (12, 12, "*", 144, "Square number"),

        # Division tests
        (10, 2, "/", 5.0, "Simple division"),
        (15, 3, "/", 5.0, "Division with no remainder"),
        (10, 3, "/", 10 / 3, "Division with remainder"),
        (0, 5, "/", 0.0, "Zero divided by number"),
        (10, 0, "/", None, "Division by zero"),
        (-10, 2, "/", -5.0, "Negative division"),
        (100, 10, "/", 10.0, "Large number division"),
        (1, 3, "/", 1 / 3, "Fraction result"),

        # Invalid operator tests
        (5, 3, "%", "invalid", "Modulo operator (invalid)"),
        (5, 3, "^", "invalid", "Power operator (invalid)"),
        (5, 3, "add", "invalid", "Word operator (invalid)"),
        (5, 3, "", "invalid", "Empty operator"),
        (5, 3, "++", "invalid", "Double operator"),
    ]

    passed = 0
    failed = 0

    for num1, num2, operator, expected, description in test_cases:
        result = calc(num1, num2, operator)
        status = "✓ PASS" if result == expected else "✗ FAIL"

        if result == expected:
            passed += 1
        else:
            failed += 1

        print(f"{status}: {description}")
        print(f"  Input: calc({num1}, {num2}, '{operator}')")
        print(f"  Expected: {expected}, Got: {result}")
        print()

    print(f"calc() Summary: {passed} passed, {failed} failed\n")
    return passed, failed

def test_compute_calcs():
    print("=" * 60)
    print("TESTING compute_calcs() FUNCTION")
    print("=" * 60)

    tests = [
        # (inputs, expected_substring)
        (["3", "5", "+"], "3 + 5 = 8"),                     # normal add
        (["10", "0", "/"], "Can't divide by zero"),         # divide by zero
        (["7", "2", "-"], "7 - 2 = 5"),                     # subtraction
        (["4", "3", "*"], "4 * 3 = 12"),                    # multiplication
        (["9", "1", "%"], "The requested calculation is invalid")  # invalid op
    ]

    passed = 0
    failed = 0

    for i, (inputs, expected) in enumerate(tests, 1):
        with patch("builtins.input", side_effect=inputs), \
             patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            compute_calcs(1)
            output = fake_out.getvalue().strip()

        if expected.replace(" ","") in output.replace(" ",""):
            print(f" ✓ PASS Test {i}  | Inputs: {inputs} | Output: {output}")
            passed += 1
        else:
            print(f"✗ FAIL Test {i}  | Inputs: {inputs} | Output: {output}")
            print(f"   Expected to contain: '{expected}'")
            failed += 1

    print(f"\nSummary: {passed} passed, {failed} failed.")
    return passed, failed

def test_is_armstrong():
    """Test the is_armstrong function"""
    print("=" * 60)
    print("TESTING is_armstrong() FUNCTION")
    print("=" * 60)





    test_cases = [
        # Single digit (all are Armstrong numbers)

        (0, True, "Single digit - 0"),
        (1, True, "Single digit - 1"),
        (5, True, "Single digit - 5"),
        (9, True, "Single digit - 9"),

        # Two digit numbers (none are Armstrong)
        (10, False, "Two digits - not Armstrong"),
        (25, False, "Two digits - not Armstrong"),
        (99, False, "Two digits - not Armstrong"),

        # Three digit Armstrong numbers
        (153, True, "Three digits - Armstrong (1³+5³+3³=153)"),
        (370, True, "Three digits - Armstrong (3³+7³+0³=370)"),
        (371, True, "Three digits - Armstrong (3³+7³+1³=371)"),
        (407, True, "Three digits - Armstrong (4³+0³+7³=407)"),

        # Three digit non-Armstrong
        (100, False, "Three digits - not Armstrong"),
        (152, False, "Three digits - not Armstrong"),
        (999, False, "Three digits - not Armstrong"),

        # Four digit Armstrong numbers
        (1634, True, "Four digits - Armstrong (1⁴+6⁴+3⁴+4⁴=1634)"),
        (8208, True, "Four digits - Armstrong (8⁴+2⁴+0⁴+8⁴=8208)"),
        (9474, True, "Four digits - Armstrong (9⁴+4⁴+7⁴+4⁴=9474)"),

        # Four digit non-Armstrong
        (1000, False, "Four digits - not Armstrong"),
        (1633, False, "Four digits - not Armstrong"),
        (9999, False, "Four digits - not Armstrong"),
        # Five digit Armstrong numbers

        (54748, True, "Five digits - Armstrong"),
        (92727, True, "Five digits - Armstrong"),
        (93084, True, "Five digits - Armstrong"),

        # Five digit non-Armstrong
        (10000, False, "Five digits - not Armstrong"),
        (54747, False, "Five digits - not Armstrong"),


    ]

    passed = 0
    failed = 0

    for num, expected, description in test_cases:
        result = is_armstrong(num)
        status = "✓ PASS" if result == expected else "✗ FAIL"

        if result == expected:
            passed += 1
        else:
            failed += 1

        print(f"{status}: {description}")
        print(f"  Input: is_armstrong({num})")
        print(f"  Expected: {expected}, Got: {result}")
        print()


    print(f"is_armstrong() Summary: {passed} passed, {failed} failed\n")
    return passed, failed


def test_count_armstrong_numbers():
    """Test the count_armstrong_numbers function"""
    print("=" * 60)
    print("TESTING count_armstrong_numbers() FUNCTION")
    print("=" * 60)

    # The known Armstrong numbers in range [100, 10000) are:
    # 153, 370, 371, 407, 1634, 8208, 9474
    expected_count = 16

    result = count_armstrong_numbers()
    status = "✓ PASS" if result == expected_count else "✗ FAIL"

    print(f"{status}: Count Armstrong numbers from 1 to 9999")
    print(f"  Expected: {expected_count}, Got: {result}")

    # List the actual Armstrong numbers in this range
    armstrong_list = []
    for i in range(1, 10000):
        if is_armstrong(i):
            armstrong_list.append(i)

    print(f"  Armstrong numbers found: {armstrong_list}")
    print()
    passed=0
    failed=0

    expected_output= "1\n2\n3\n4\n5\n6\n7\n8\n9\n153\n370\n371\n407\n1634\n8208\n9474"
    with patch("builtins.input"), \
            patch("sys.stdout", new_callable=io.StringIO) as fake_out:
        count_armstrong_numbers()
        output = fake_out.getvalue().strip()
    if expected_output.replace(" ", "").replace("\n","") in output.replace(" ", "").replace("\n",""):
        print(f" ✓ PASS Test Print |  Output: {output}")
        passed += 1
    else:
        print(f"✗ FAIL Test Print  |  Output: {output}")
        print(f"   Expected to contain: '{expected_output}'")
        failed += 1





    if result == expected_count:
        passed +=1
        print(f"count_armstrong_numbers() Summary: {passed} passed, {failed} failed\n")
        return passed,failed
    else:
        print(f"count_armstrong_numbers() Summary: {passed} passed, {failed} failed\n")
        return passed,failed


def test_decompressed():
    """Test the decompressed function"""
    print("=" * 60)
    print("TESTING decompressed() FUNCTION")
    print("=" * 60)

    test_cases = [
        # Basic decompressed
        ("a3","aaa", "Three consecutive same characters"),
        ("a3b3","aaabbb", "Two groups of same characters"),
        ("a3b3c3", "aaabbbccc", "Three groups of same characters"),

        # No compression needed
        ("a", "a", "Single character"),
        ("ab", "ab", "Two different characters"),
        ("abc", "abc", "All different characters"),
        ("abcdef", "abcdef", "Long string, all different"),

        # Mixed decompressed
        ("a3b", "aaab", "Multiple same, then one different"),
        ("a2b3", "aabbb", "Multiple groups, different counts"),
        ("a3b3c3d4", "aaabbbcccdddd", "Multiple groups with varying counts"),
        ("a2b2c2", "aabbcc", "All pairs"),

        # Edge cases with single characters between groups
        ("a2ba2", "aabaa", "Single char between groups"),
        ("a3ba3b3", "aaabaaabbb", "Complex pattern"),
        ("ab4a", "abbbba", "Single chars at edges"),

        # Long repetitions
        ("a9", "aaaaaaaaa", "Ten same characters"),
        ("a4b4c4d4", "aaaabbbbccccdddd", "Multiple groups of 4"),

        # Real-world examples
        ("hel2o", "hello", "Word with one pair"),
        ("mis2is2ip2i", "mississippi", "Complex word"),
        ("bo2k2e2per", "bookkeeper", "Multiple pairs"),

        # Empty and special cases
        ("", "", "Empty string"),
        ("a2", "aa", "Just two same characters"),
        ("a3", "aaa", "Just three same characters"),
    ]

    passed = 0
    failed = 0

    for input_str, expected, description in test_cases:
        result = decompressed(input_str)
        status = "✓ PASS" if result == expected else "✗ FAIL"

        if result == expected:
            passed += 1
        else:
            failed += 1

        print(f"{status}: {description}")
        print(f"  Input: decompressed('{input_str}')")
        print(f"  Expected: '{expected}', Got: '{result}'")
        print()

    print(f"decompressed() Summary: {passed} passed, {failed} failed\n")
    return passed, failed


def test_count_sub():
    """Test the count_sub function"""
    print("=" * 60)
    print("TESTING count_sub() FUNCTION")
    print("=" * 60)

    test_cases = [
        # Basic cases
        ("hello", "l", 2, "Single character appearing twice"),
        ("hello", "ll", 1, "Two-character substring appearing once"),
        ("hello", "o", 1, "Single character at end"),
        ("hello", "h", 1, "Single character at start"),

        # No occurrences
        ("hello", "x", 0, "Character not in string"),
        ("hello", "world", 0, "Substring not in string"),
        ("abc", "xyz", 0, "Completely different substring"),

        # Overlapping occurrences
        ("aaa", "aa", 2, "Overlapping occurrences"),
        ("aaaa", "aa", 3, "Multiple overlapping occurrences"),
        ("ababa", "aba", 2, "Overlapping pattern"),
        ("abababa", "aba", 3, "Multiple overlapping patterns"),

        # Full string match
        ("hello", "hello", 1, "Entire string matches"),
        ("test", "test", 1, "Exact match"),

        # Longer than string
        ("hi", "hello", 0, "Substring longer than string"),
        ("", "a", 0, "Empty string, non-empty substring"),

        # Repeated words
        ("the cat in the hat", "the", 2, "Word appearing twice"),
        ("to be or not to be", "to", 2, "Common word repetition"),
        ("banana", "ana", 2, "Overlapping in word"),
        ("banana", "na", 2, "Simple repetition"),

        # Case sensitivity
        ("Hello", "hello", 0, "Case mismatch"),
        ("HELLO", "HELLO", 1, "All uppercase match"),

        # Special patterns
        ("abcabcabc", "abc", 3, "Repeating pattern"),
        ("123123123", "123", 3, "Number pattern"),
        ("a b a b a", "a b", 2, "Pattern with spaces"),

        # Single character strings
        ("a", "a", 1, "Single char, exact match"),
        ("b", "a", 0, "Single char, no match"),

        # Whitespace
        ("hello world", " ", 1, "Space character"),
        ("a  b  c", "  ", 2, "Double space"),
        ("   ", " ", 3, "Multiple spaces overlapping"),

        # Empty substring (edge case)
        #("hello", "", 6, "Empty substring (matches before each char)"),
        #("", "", 1, "Both empty strings"),

        # Long strings
        ("a" * 100, "a", 100, "Long string of same character"),
        ("ab" * 50, "ab", 50, "Repeating two-char pattern"),
        ("abc" * 33, "abc", 33, "Repeating three-char pattern"),
    ]

    passed = 0
    failed = 0

    for string, substring, expected, description in test_cases:
        result = count_sub(string, substring)
        status = "✓ PASS" if result == expected else "✗ FAIL"

        if result == expected:
            passed += 1
        else:
            failed += 1

        print(f"{status}: {description}")
        print(f"  Input: count_sub('{string}', '{substring}')")
        print(f"  Expected: {expected}, Got: {result}")
        print()

    print(f"count_sub() Summary: {passed} passed, {failed} failed\n")
    return passed, failed


def run_all_tests():
    """Run all test functions"""
    print("\n")
    print("*" * 60)
    print("*" + " " * 58 + "*")
    print("*" + "  COMPREHENSIVE TEST SUITE - STARTING ALL TESTS  ".center(58) + "*")
    print("*" + " " * 58 + "*")
    print("*" * 60)
    print("\n")

    results = {}

    passed, failed = test_calc()
    results['calc()'] = passed, failed

    passed, failed =test_compute_calcs()
    results['compute_calcs()'] = passed, failed

    passed, failed =test_is_armstrong()
    results['is_armstrong()'] = passed, failed

    passed, failed =test_count_armstrong_numbers()
    results['count_armstrong_numbers()'] = passed, failed

    passed, failed =test_decompressed()
    results['decompressed()'] = passed, failed

    passed, failed =test_count_sub()
    results['count_sub()'] = passed, failed

    # Print final summary
    print("\n")
    print("=" * 70)
    print("=" * 70)
    print("  FINAL TEST SUMMARY - ALL FUNCTIONS".center(70))
    print("=" * 70)
    print("=" * 70)
    print()

    total_passed = 0
    total_failed = 0

    for func_name, (passed, failed) in results.items():
        total_tests = passed + failed
        pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        status = "✓ ALL PASSED" if failed == 0 else "✗ SOME FAILED"

        print(f"Function: {func_name}")
        print(f"  {status}")
        print(f"  Tests Run: {total_tests}")
        print(f"  Passed: {passed}")
        print(f"  Failed: {failed}")
        print(f"  Success Rate: {pass_rate:.1f}%")
        print()

        total_passed += passed
        total_failed += failed

    print("=" * 70)
    print("  OVERALL STATISTICS".center(70))
    print("=" * 70)
    total_tests = total_passed + total_failed
    overall_pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0

    print(f"Total Functions Tested: {len(results)}")
    print(f"Total Test Cases: {total_tests}")
    print(f"Total Passed: {total_passed}")
    print(f"Total Failed: {total_failed}")
    print(f"Overall Success Rate: {overall_pass_rate:.1f}%")
    print()

    if total_failed == 0:
        print("🎉 " + "ALL TESTS PASSED SUCCESSFULLY!".center(66) + " 🎉")
    else:
        print("⚠️  " + "SOME TESTS FAILED - PLEASE REVIEW ABOVE".center(66) + " ⚠️ ")

    print("=" * 70)
    print("=" * 70)


# Run all tests when script is executed
if __name__ == "__main__":
    run_all_tests()
