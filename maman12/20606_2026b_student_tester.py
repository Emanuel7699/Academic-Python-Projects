# Test Suite for All Functions
from mmn12 import *

import io
from unittest.mock import patch

# ============== TEST FUNCTIONS ==============

def test_count_circles():
    """Test the count_circles function with various inputs"""
    print("=" * 60)
    print("TESTING count_circles() FUNCTION")
    print("=" * 60)

    test_cases = [
        ([5,5,1,9,0,7,6,2,3,1], 5, "Example from the question"),
        ([0,1,2,3,4], 5, "Each element points to itself"),
        ([1,2,0], 3, "3-cycle"),
        ([2,0,1], 3, "3-cycle different order"),
        ([1,0,3,2], 4, "Two cycles of length 2"),
        ([1,2,3,4,4], 1, "Only last element is cycle"),
    ]

    passed = failed = 0

    for lst, expected, description in test_cases:
        result = count_circles(lst)
        status = "✔ PASS" if result == expected else "✘ FAIL"

        if result == expected:
            passed += 1
        else:
            failed += 1

        print(f"{status}: {description}")
        print(f"  Input: {lst}")
        print(f"  Expected: {expected}, Got: {result}\n")

    print(f"count_circles() Summary: {passed} passed, {failed} failed\n")
    return passed, failed


# --------------------------------------------------

def test_longest_sub_list():
    """Test longest_sub_list function"""
    print("=" * 60)
    print("TESTING longest_sub_list() FUNCTION")
    print("=" * 60)

    test_cases = [
        ([-1, 1, -1, -5, 2, 2], [-1,1,-1], "Alternating then break"),
        ([-2,-2,1,1,2,-7,2,3,3], [2,-7,2], "Middle alternating"),
        ([4,5,4,3,2,1], [4], "No alternation"),
        ([1,-1,1,-1,1], [1,-1,1,-1,1], "Full alternating"),
        ([1,-1,1,1,-1], [1,-1,1], "First max"),
    ]

    passed = failed = 0

    for lst, expected, description in test_cases:
        result = longest_sub_list(lst)
        status = "✔ PASS" if result == expected else "✘ FAIL"

        if result == expected:
            passed += 1
        else:
            failed += 1

        print(f"{status}: {description}")
        print(f"  Input: {lst}")
        print(f"  Expected: {expected}, Got: {result}\n")

    print(f"longest_sub_list() Summary: {passed} passed, {failed} failed\n")
    return passed, failed


# --------------------------------------------------

def test_find_num():
    """Test find_num function"""
    print("=" * 60)
    print("TESTING find_num() FUNCTION")
    print("=" * 60)

    range_lst = [(4,1), (12,0), (20,1), (102,2)]

    test_cases = [
        (range_lst, 5, 0, "Found in first range"),
        (range_lst, 101, 3, "Found in last range"),
        (range_lst, 15, -1, "Not found"),
        (range_lst, 105, -1, "Outside range"),
        (range_lst, 12, 1, "Single element range"),
    ]

    passed = failed = 0

    for r_lst, num, expected, description in test_cases:
        result = find_num(r_lst, num)
        status = "✔ PASS" if result == expected else "✘ FAIL"

        if result == expected:
            passed += 1
        else:
            failed += 1

        print(f"{status}: {description}")
        print(f"  Input: {num}")
        print(f"  Expected: {expected}, Got: {result}\n")

    print(f"find_num() Summary: {passed} passed, {failed} failed\n")
    return passed, failed


# --------------------------------------------------

def test_identity_matrix():
    """Test identity_matrix function"""
    print("=" * 60)
    print("TESTING identity_matrix() FUNCTION")
    print("=" * 60)

    test_cases = [
        ([[1]], True, "1x1 matrix"),
        ([[1,0],[0,1]], True, "2x2 identity"),
        ([[1,0],[1,1]], False, "Not identity"),
        ([[1,0,0],[0,1,0],[0,0,1]], True, "3x3 identity"),
        ([[1,0],[0,1,0]], False, "Not square"),
    ]

    passed = failed = 0

    for mat, expected, description in test_cases:
        try:
            result = identity_matrix(mat)
            ok = result == expected
        except Exception:
            ok = False
            result = "Exception"

        status = "✔ PASS" if ok else "✘ FAIL"

        if ok:
            passed += 1
        else:
            failed += 1

        print(f"{status}: {description}")
        print(f"  Expected: {expected}, Got: {result}\n")

    # TypeError test
    try:
        identity_matrix([[1,0],[0,1.0]])
        print("✘ FAIL: TypeError not raised")
        failed += 1
    except TypeError:
        print("✔ PASS: TypeError raised correctly")
        passed += 1

    print(f"identity_matrix() Summary: {passed} passed, {failed} failed\n")
    return passed, failed


# --------------------------------------------------

def test_create_sub_matrix():
    """Test create_sub_matrix function"""
    print("=" * 60)
    print("TESTING create_sub_matrix() FUNCTION")
    print("=" * 60)

    mat = [
        [1,0,0,0,0],
        [0,1,0,0,0],
        [0,0,1,0,0],
        [0,0,0,1,0],
        [1,0,0,0,1]
    ]

    test_cases = [
        (mat, 3, [[1,0,0],[0,1,0],[0,0,1]], "Center 3x3"),
        (mat, 1, [[1]], "Center 1x1"),
    ]

    passed = failed = 0

    for m, size, expected, description in test_cases:
        try:
            result = create_sub_matrix(m, size)
            ok = result == expected
        except Exception:
            ok = False
            result = "Exception"

        status = "✔ PASS" if ok else "✘ FAIL"

        if ok:
            passed += 1
        else:
            failed += 1

        print(f"{status}: {description}")
        print(f"  Expected: {expected}, Got: {result}\n")

    # IndexError test
    try:
        create_sub_matrix([[1,2],[3]], 1)
        print("✘ FAIL: IndexError not raised")
        failed += 1
    except IndexError:
        print("✔ PASS: IndexError raised correctly")
        passed += 1

    print(f"create_sub_matrix() Summary: {passed} passed, {failed} failed\n")
    return passed, failed


# --------------------------------------------------

def test_max_identity_matrix():
    """Test max_identity_matrix function"""
    print("=" * 60)
    print("TESTING max_identity_matrix() FUNCTION")
    print("=" * 60)

    mat1 = [
        [1,0,0,0,0],
        [0,1,0,0,0],
        [0,0,1,0,0],
        [0,0,0,1,0],
        [1,0,0,0,1]
    ]

    mat2 = [
        [1,0,0,0,0,0,0],
        [0,1,0,0,0,0,0],
        [0,0,1,0,0,0,0],
        [0,0,0,1,1,0,0],
        [0,0,0,0,1,0,0],
        [0,0,0,0,0,1,0],
        [0,0,0,0,0,0,1]
    ]

    mat3 = [
        [1,0,0],
        [0,1,0],
        [0,0,1.0]
    ]

    test_cases = [
        (mat1, 3, "Example 1"),
        (mat2, 1, "Example 2"),
    ]

    passed = failed = 0

    for mat, expected, description in test_cases:
        result = max_identity_matrix(mat)
        status = "✔ PASS" if result == expected else "✘ FAIL"

        if result == expected:
            passed += 1
        else:
            failed += 1

        print(f"{status}: {description}")
        print(f"  Expected: {expected}, Got: {result}\n")

    # Exception handling test (TypeError message)
    with patch('sys.stdout', new=io.StringIO()) as fake_out:
        result = max_identity_matrix(mat3)
        output = fake_out.getvalue()

    if "Not all values are integer" in output and result == 0:
        print("✔ PASS: TypeError handling correct")
        passed += 1
    else:
        print("✘ FAIL: TypeError handling incorrect")
        failed += 1

    print(f"max_identity_matrix() Summary: {passed} passed, {failed} failed\n")
    return passed, failed


# --------------------------------------------------

def run_all_tests():
    total_passed = total_failed = 0

    for test_func in [
        test_count_circles,
        test_longest_sub_list,
        test_find_num,
        test_identity_matrix,
        test_create_sub_matrix,
        test_max_identity_matrix
    ]:
        p, f = test_func()
        total_passed += p
        total_failed += f

    print("=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"TOTAL PASSED: {total_passed}")
    print(f"TOTAL FAILED: {total_failed}")


if __name__ == "__main__":
    run_all_tests()