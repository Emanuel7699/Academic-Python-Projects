
# This function fing the missing index in the Arithmetic Progression.
def find_missing_index(lst):
    if len(lst) <= 2:
        raise ValueError("Length of list is less than 2")

    d1 = lst[1] - lst[0]
    d2 = lst[2] - lst[1]
    if abs(d1) > abs(d2):
        d1 = d2
    for i in range(len(lst)-1):
        if lst[i+1] - lst[i] != d1:
            return i+1
    return len(lst)


# This function calculates the number of triples whose product equals num.
def count_triples(lst, num):
    if len(lst) < 3:
        return 0

    triples = 0

    for i in range(len(lst) - 2):
        left = i + 1
        right = len(lst) - 1

        while left < right:
            if lst[i] * lst[left] * lst[right] > num:
                right -= 1
            elif lst[i] * lst[left] * lst[right] < num:
                left += 1
            else:
                triples += 1
                left += 1
                right -= 1
    return triples


# This function calculates the pairs of elements in the list whose sum equals num.
def pair_sublist_sum(lst, num, i=0, j=1):
    if i >= len(lst) - 1:
        return []
    if j >= len(lst):
        return pair_sublist_sum(lst, num, i+1, i+2)
    if (lst[i] + lst[j]) == num:
        return [(lst[i], lst[j])] + pair_sublist_sum(lst, num, i, j+1)
    return pair_sublist_sum(lst,num,i,j+1)


# This function returns the pairs of elements in the list whose sum equals num.
def pair_sum(lst, num):
    if len(lst) < 2:
        return []
    return pair_sublist_sum(lst, num)


# This function calculates the number of triples in the list whose sum equals num.
def rec_sublist_triples_count(lst, num, i=0, j=1, k=2):
    if i >= len(lst) - 2:
        return 0
    if j >= len(lst) - 1:
        return rec_sublist_triples_count(lst, num, i+1, i+2, i+3)
    if k >= len(lst):
        return rec_sublist_triples_count(lst, num, i, j+1, j+2)


    if (lst[i] + lst[j] + lst[k]) == num:
        return 1 + rec_sublist_triples_count(lst, num, i, j, k+1)
    return rec_sublist_triples_count(lst,num,i,j,k+1)

# This function returns the number of triples in the list whose sum equals num.
def count_triples_rec(lst, num):
    if len(lst) < 3:
        return 0
    return rec_sublist_triples_count(lst, num)