#!/usr/bin/python

"""
Find if an array of integers contains a triplet that sums to X

This was presented to me with X=0 but, really, X could be any number.  And, of course,
this is just a variant on the same problem, but for a pair of integers.  The only
interesting difference is that there's a more conclusively best answer for a triplet.  


[Hash solution]

You can, of course, just map the "pair of integers" solution over.  

 - Iterate over the array and insert all integers into a hash
 - Iterate over the array with two nested for-loops to exhaustively search each pair
   and identify if the complementary triplet exists in the hash

Note that you will need to do some corner case handling if the integers are not
guaranteed to be unique.  This isn't an especially interesting variant (just additional
bookkeeping in our hash and an extra conditional check), so we'll ignore it for now,
confident in the knowledge that we could do it if we wanted to.  

Time:  O(n^2)
Space:  O(n)


[Sorting solution]

The sorting solution also has an analog in the "pair of integers" problem.  However, I
did not remember it in the room.  For a triplet:

 - Sort your array; O(n * log n)
 - Iterate over the array starting at the least element (or the obvious analog at the 
   largest element)
   - Using pointers to the next least element and the greatest element, do a "collapse"
     search for your triplet.  That is, if the sum of the three current values exceeds
     X, move the pointer to the greatest element "inward" (decreasing it).  If the sum
     is less than X, move the pointer of the middle element "inward" (increasing it).  
     If the sum is ever X, return True.  

Time:  O(n^2)
Space:  O(1)

"""

import sys


def summing_triplets_hash(array, target=0):
    """
    The "bad" hash solution

    Preconditions:  Contents of array and target must be integer values
    """

    int_lookup = {}
    # populate the hash
    for x in array:
        if x in int_lookup:
            int_lookup[x] += 1
        else:
            int_lookup[x] = 1

    # iterate over all pairs in array
    for index_y, y in enumerate(array):
        for z in array[index_y+1:]:
            # x + y + z = target  =>  x = target - y - z
            if (target - y - z) in int_lookup:
                return True

    # return False if we never found such a triplet
    return False


def summing_triplets_sort(array, target=0):
    """
    The better sorting solution

    Preconditions:  Contents of array and target must be integer values
    """

    # Note:  We assume this uses a reasonable implementation of a sorting algorithm
    array.sort()

    # find a triplet
    for index_x, x in enumerate(array[:-2]):
        index_y = index_x + 1
        index_z = len(array) - 1

        while index_y < index_z:
            current_sum = x + array[index_y] + array[index_z]
            # if sum is greater than target, decrease the value of "z"
            if current_sum > target:
                index_z -= 1
            # else, if sum is less than target, increase the value of "y"
            elif current_sum < target:
                index_y += 1
            else:
                return True

    # return False if we never found such a triplet
    return False


def main(argv):
    if len(argv) > 2:
        sys.stderr.write("Usage: %s [number]" % (argv[0],))
        return 1

    if len(argv) == 2:
        target_sum = int(argv[1])
    else:
        target_sum = 0

    # some sample arrays
    sample_array_1 = [-2, -1, 0 , 5, 8, 29, 42, 43, 3]
    sample_array_2 = [0 , 5, 8, 29, 42, 43, 3]
    sample_array_3 = [0 , 5, 8, 29, 42, 43, -85]

    for array in [sample_array_1, sample_array_2, sample_array_3]:
        print "Checking array for triplet summing to %d" % (target_sum)
        print "%r\n" % (array)

        print "Hash-based solver returned:  %r" % (summing_triplets_hash(array, target_sum))
        print "Sort-based solver returned:  %r" % (summing_triplets_sort(array, target_sum))
        print ""


if __name__ == "__main__":
    sys.exit(main(sys.argv))












