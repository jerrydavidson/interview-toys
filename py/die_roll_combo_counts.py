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

"""

import sys


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




if __name__ == "__main__":
    sys.exit(main(sys.argv))


