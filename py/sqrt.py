#!/usr/bin/python

import sys


FLOAT_EQUALS_DIFF = 0.0000001

def float_equals(a, b):
    # Preconditions: a, b must be floating point values
    return abs(a - b) < FLOAT_EQUALS_DIFF

def find_square_root_bounds(number, starting_lower_bound=2.0):
    # Preconditions: number must be a positive floating point value
    # 
    # Postconditions: returns a pair of floating point values whose squares are
    #                 respectively LTE and GTE the arg "number"
    current_bound = starting_lower_bound
    while current_bound * current_bound < number:
        current_bound *= 2.0
    return (current_bound / 2.0, current_bound)

def main(argv):
    if len(argv) < 2:
        sys.stderr.write("Usage: %s <number>" % (argv[0],))
        return 1

    number = float(argv[1])
    accuracy = 0.001
    assert FLOAT_EQUALS_DIFF < accuracy

    print "Estimating square root of %g with minimum accuracy of %g" % (number, accuracy)

    sqrt = None
    
    # special case: negative numbers or exact matches for 0 or 1
    if float_equals(number, 0.0):
        sqrt = 0.0
    elif number < 0.0:
        sqrt = None
    elif float_equals(number, 1.0):
        sqrt = 1.0
    
    # let's actually compute an estimated square root
    else:
        if number < 1.0:
            lower_bound = 0.0
            upper_bound = 1.0
        else:
            lower_bound, upper_bound = find_square_root_bounds(number)
        
        # special case: early termination on exact matches
        if float_equals(lower_bound * lower_bound, number):
            sqrt = lower_bound
        elif float_equals(upper_bound * upper_bound, number):
            sqrt = upper_bound
        else:
            # binary search within bounds for an accurate estimate
            while upper_bound - lower_bound > accuracy:
                midpoint = (upper_bound + lower_bound) / 2.0
                
                # special case: early termination on exact matches
                if float_equals(midpoint * midpoint, number):
                    lower_bound = midpoint
                    upper_bound = midpoint
                    break
                elif midpoint * midpoint < number:
                    lower_bound = midpoint
                else:
                    upper_bound = midpoint
        
            sqrt = lower_bound
    
    if sqrt is not None:
        print "Calculated estimated square root:\n  %g" % (sqrt)


if __name__ == "__main__":
    sys.exit(main(sys.argv))




