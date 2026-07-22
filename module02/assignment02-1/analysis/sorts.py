# Sharie Rhea
# 07.14.26
# SNHU CS680

import sys

# increase recursion depth for merge and quick sort
sys.setrecursionlimit(200000)


def insertionsort(array, comp_func):
    """
    Sort a list of elements in O(n^2) time by iterating over the list and inserting each element into order
    one at a time.
    """
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        # shift elements over until we find one that is less than or equal to the key to insert
        while j >= 0 and not comp_func(array[j], key):
            array[j + 1] = array[j]
            j -= 1
        # insert the new element (key) into the sub array
        array[j + 1] = key


def mergesort(array, comp_func):
    """
    Sort a list of elements in O(n lg n) time by recursively dividing the array
    in half until only one element is present. Then, recombine halves such that
    they are sorted until the full list has been reconstructed.
    """
    # an empty list or one with only 1 element is already sorted
    if len(array) <= 1:
        return array

    # divide the array in half and sort each side
    mid = len(array) // 2
    left = mergesort(array[:mid], comp_func)
    right = mergesort(array[mid:], comp_func)

    # recombine
    return merge(left, right, comp_func)


def merge(left, right, comp_func):
    """
    The main work for mergesort. Recombine two sorted subarrays by appending the
    smallest element available until one list is empty. Then, tack on the other list.
    """
    result = []
    i = j = 0
    # while there are still elements in both arrays
    while i < len(left) and j < len(right):
        if comp_func(left[i], right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    # one of the lists is empty, no need to continue comparing
    # just tack on both lists
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quicksort(array, comp_func):
    """
    Sort a list of elements in O(n lg n) time by partitioning the array into
    two smaller subarrays and recursively sorting them, plus a middle section equal to the pivot.
    """
    # an empty list or one with only 1 element is already sorted
    if len(array) <= 1:
        return array

    # choose the center element as the pivot
    pivot = array[len(array) // 2]
    # build the left array (containing elements less than the pivot)
    left = [x for x in array if comp_func(x, pivot)]
    # build middle portion (elements equal to the pivot)
    middle = [x for x in array if not comp_func(x, pivot) and not comp_func(pivot, x)]
    # build the right array (elements greater than the pivot)
    right = [x for x in array if comp_func(pivot, x)]

    # recursive call to sort the remaining left and right portions
    return quicksort(left, comp_func) + middle + quicksort(right, comp_func)
