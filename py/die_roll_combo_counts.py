#!/usr/bin/python

"""
Given a 6-sided die, how many ways could you roll it in succession to sum to a number N?  

This was a dynamic programming problem with at least two parts.  In the first case, we take order to matter.   
In the second case, we assume that it does not.  


Order matters:  

My in-the-room implementation used recursion and was super-crappy.  I'll try to write it up below.  I
discussed using a hash to store intermediate solutions (so we weren't recomputing them each time) but this 
was still not a great solution.  

The much better solution that we discussed afterward was to compute all numbers up to N in order.  Any 
number's "combination count" can be calculated based on the values for the preceding 6 numbers.  Very clean.  


Order does not matter:

I went into the tank on this one.  I couldn't figure out a good way to map the dynamic programming solution
from the previous problems to this one.  I modified the recursive implementation and just went with that, 
knowing it pretty much sucked.  

Update:  I believe that the "order doesn't matter" solution should be solvable with a 2-dimensional array,
where one dimension "adds numbers to the set of possibilities" and the second dimension is the desired 
number to sum to.  A sample corner of the table might look like:

1,2,3,4     1    2    3    5    6
1,2,3       1    2    3    4    5
1,2         1    2    2    3    3
1           1    1    1    1    1

            1    2    3    4    5

The rule for populating this table is a bit funny.  The general rule is that any given element is the
sum of two other elements in the table:

    - The element in the row below it
        - Ex:  the ways to add up to N with 4's certainly includes the case of N where there are no 4's
    - The element in the column "X" units to the left where X is the new value in the set at this row
        - Ex:  the ways to add up to N with another 4 is the same as the ways to add up to "N-4", which
               we've already calculated

The corner cases are that:

    - The bottom row needs to be initialized properly
        - There is no row below it, so the value at this virtual row should be assumed as 0
    - There is a left-side "virtual" column for the "sum to 0" case.  This should be assumed as 1
        - This applies when a new number (or coin?) is added to our set.  When the target sum is
          exactly that number, we must obviously include one instance of the new number as a possible 
          solution.  

I have written the above rules to accommodate a more general case of the problem definition.  The set
need not be contiguous values, nor start with a '1'.  The assumption is only that the set is composed
of positive integer values.  

Optimization:  Based on the rules we've established, we should never actually need more than the 
previous row to calculate the next row.  This significantly improves our space complexity.  

Run-time:  O(N * |set size|)
Space:  O(N)

"""

import sys


def combination_count_unordered_d_prog(n):
    """
    The good dynamic programming solution

    The algorithm implemented here is described in the module doc string above
    """

    # Note:  I decided to use a convention where the column for a "sum target"
    #        was located at index "sum target - 1".  It might be better to
    #        manually populate the "virtual column" for a sum target of 0 to
    #        contain a 1 and then populate counts for "sum targets" at the 
    #        index "sum target".  It's unclear to me if this improves or reduces
    #        readability.  

    # must be a sorted list values
    values = list(range(1,7))

    # initialize base "virtual row" to n 0's
    previous_row = [0] * n

    for value in values:
        # initialize to None as a sort-of sanity check
        current_row = [None] * n

        # iterate through 1 to n
        for sum_target in range(1, n+1):
            # calculate table element for current sum_target
            count_without_new_value = previous_row[sum_target-1]
            
            if value > sum_target:
                count_with_new_value = 0
            elif value == sum_target:
                # include "virtual column" at 0
                count_with_new_value = 1
            else:
                count_with_new_value = current_row[(sum_target - value) - 1]

            current_row[sum_target-1] = count_without_new_value + count_with_new_value

        # each row feeds into the next one
        previous_row = current_row

    return current_row[n-1]


def combination_count_ordered_d_prog(n):
    """
    The good dynamic programming solution
    """
    assert n >= 1

    # calculate each number up to 'n'
    running_solutions = []
    for i in range(1, n + 1):    # 1 ... n
        index = i - 1

        # count the "single roll" case
        if i <= 6:
            accumulator = 1
        else:
            accumulator = 0

        # sum possibilities for rolls between 1 and 6 based on their pre-calculated values
        for j in range(1, 7):    # 1 ... 6
            if index - j >= 0:
                accumulator += running_solutions[index - j]

        running_solutions.append(accumulator)

    return running_solutions[n-1]


def combination_count_ordered_crappy_recursion(n):
    """
    The crappy recursive solution
    """
    assert n >= 1

    accumulator = 0
    for i in range(1, 7):
        if n - i < 0:
            pass
        elif n - i == 0:
            accumulator += 1
        elif n - i == 1:
            accumulator += 1
        else:
            accumulator += combination_count_ordered_crappy_recursion(n - i)

    return accumulator


def combination_count_ordered_crappy_recursion_with_cache(n, previous_solutions=None):
    """
    The crappy recursive solution, but with a cache to prevent recalculations

    I am using a hash for the cache.  In retrospect, it is pretty obvious that
    we need to calculate all previous solutions and, consequently, we could
    store this information in a dense array.  However, this reductive logic
    also leads to the dynamic programming solution that we already have above
    and I think it is helpful for validating correctness to have the two
    separate implementations.  
    """
    assert n >= 1

    if previous_solutions is None:
        previous_solutions = {1: 1}    # seed with base case ... b/c it's nice?

    accumulator = 0
    for i in range(1, 7)[::-1]:    # fancy notation using the stride argument to count from 6 ... 1
        if n - i < 0:
            pass
        elif n - i == 0:
            accumulator += 1
        elif n - i == 1:
            accumulator += 1
        else:
            if (n - i) not in previous_solutions:
                minus_i_count = combination_count_ordered_crappy_recursion_with_cache(n - i, previous_solutions)
                previous_solutions[n - i] = minus_i_count

            accumulator += previous_solutions[n - i]

    return accumulator


def main(argv):
    if len(argv) < 2:
        sys.stderr.write("Usage: %s <number>" % (argv[0],))
        return 1

    number = int(argv[1])

    print "Calculating number of ordered combinations of values between 1 and 6 that will sum to:\n    %d\n" % (number)

    print "Dynamic programming solution:\n    %d\n" % (combination_count_ordered_d_prog(number))

#    print "Slow recursive solution:\n    %d\n" % (combination_count_ordered_crappy_recursion(number))

    print "Less terrible recursive solution:\n    %d\n" % (combination_count_ordered_crappy_recursion_with_cache(number))

    print "Calculating number of unordered combinations of values between 1 and 6 that will sum to:\n    %d\n" % (number)

    print "Dynamic programming solution:\n    %d\n" % (combination_count_unordered_d_prog(number))





if __name__ == "__main__":
    sys.exit(main(sys.argv))


