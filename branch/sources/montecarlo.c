#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

int main() {
    int total_points = 1000;
    int inside_circle = 0;

    srand(time(NULL));

    for (int i = 0; i < total_points; i++) {
        double x = (double)rand() / RAND_MAX;
        double y = (double)rand() / RAND_MAX;

        if (sqrt(x * x + y * y) <= 1.0) {
            inside_circle++;
        }
    }

    double pi_estimate = 4.0 * inside_circle / total_points;

#ifndef QUIET
    printf("Estimated value of π: %f\n", pi_estimate);
#endif

    return 0;
}
