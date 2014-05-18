/* Re-implementing the square root estimator in c++
 */

#include <stdio.h>
#include <math.h>

double DOUBLE_ACCURACY = 0.000000001;

double ACCURACY_THRESHOLD = 0.00001;

/* Estimate equality on two double values */
bool double_equals(double a, double b) {
    return fabs(a - b) < DOUBLE_ACCURACY;
}

/* Estimate the square root of the input within accuracy of ACCURACY_THRESHOLD.
   On negative input, "-1.0" is returned as the "error".  
*/
double square_root(const double number) {
    // error check: number must be greater than 1
    double retval;
    if (double_equals(number, 0.0)) {
        retval = 0.0;
    }
    else if (number < 0.0) {
        retval = -1.0;
    }
    else {
        double lower_bound = 0.0;
        double upper_bound = fmax(number, 1.0);
        double midpoint;

        while (upper_bound - lower_bound > ACCURACY_THRESHOLD) {
            midpoint = (upper_bound + lower_bound) / 2.0;
            if (midpoint * midpoint > number) {
                upper_bound = midpoint;
            }
            else {
                lower_bound = midpoint;
            }
        }

        retval = lower_bound;
    }

    return retval;
}

/* Input: one double value
   Output: None

   Prints messages to stdio regarding the estimated
   square root of the input value
 */
int main(const int argc, const char* argv[])
{
    double input;
    // TODO:  Add error checking for number of arguments
    int sscanf_out = sscanf(argv[1], "%lg", &input);
    // TODO:  Add error checking for translation errors

    printf("Calculating square root of\n%lg\n", input);

    double est_sqrt = square_root(input);

    printf("Estimate:\n%lg\n", est_sqrt);

    return 0;
}
