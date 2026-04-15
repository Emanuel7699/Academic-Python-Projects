

# This function receives a list of indices and returns the total number of elements that belong to a cycle.
def count_circles(lst):
    count = 0
    for i in range(len(lst)):
        idx = i
        for j in range(len(lst)):
            idx = lst[idx]
            if idx == i:
                count += 1
                break
    return count


# This function receives a list and returns the longest contiguous sub-list with alternating signs.
def longest_sub_list(lst):
    right, left, maxRight, maxLeft = 0, 0, 0, 0
    while right < len(lst)-1:
        right += 1

        if lst[right] * lst[right - 1] > 0:
            if (right-1) - left > maxRight - maxLeft:
                maxRight, maxLeft = right - 1, left
            left = right
            continue

        if right - left > maxRight - maxLeft:
            maxRight, maxLeft = right, left

    return lst[maxLeft:maxRight+1]


# This function receives a list of ranges and a number, and returns the index of the range containing the number.
def find_num(range_lst, num):
    for i in range(len(range_lst)):
        center, radius = range_lst[i]

        if center - radius <= num <= center + radius:

            return i

    return -1


# This function receives a matrix and returns True if it is a square identity matrix of integers.
def identity_matrix(mat):
    for i in range(len(mat)):
        if len(mat[i]) != len(mat):
            return False
        for j in range(len(mat[i])):
            if not isinstance(mat[i][j], int):
                raise TypeError("Not all values are integer")
            if (mat[i][j] != 1 and i == j) or (mat[i][j] != 0 and i != j):
                return False
    return True


# This function receives a matrix and a size, and returns a centered sub-matrix of that size.
def create_sub_matrix(mat, size):
    left = len(mat)//2 - size//2
    right = len(mat)//2 + size//2 + 1
    for i in range(len(mat)):
        if len(mat[i]) != len(mat):
            raise IndexError("Not all rows size are equal")
    matReturn = [mat[i][left:right] for i in range(left, right)]
    return matReturn


# This function receives a matrix and returns the size of the largest centered identity matrix found within it.
def max_identity_matrix(mat):
    try:
        maxSize = len(mat)
        minSize = 0
        while maxSize > minSize+1:
            if (identity_matrix(create_sub_matrix(mat, (maxSize+minSize)//2)) == True):
                minSize = (maxSize + minSize) // 2
            else:
                maxSize = (maxSize + minSize) // 2
        return minSize
    except TypeError:
        print("Not all values are integer")
        return 0
    except IndexError:
        print("Not all rows size are equal")
        return 0