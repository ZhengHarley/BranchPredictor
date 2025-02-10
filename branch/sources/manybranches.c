#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    srand(time(NULL));
    int t = 0;

    for (int i = 0; i < 1000; i++) {
        int random_value = rand() % 150;

        if (random_value < 10) {
#ifndef QUIET
            printf("Branch 1: random_value = %d\n", random_value);
#endif
            t += 10;
        } else if (random_value < 20) {
#ifndef QUIET
            printf("Branch 2: random_value = %d\n", random_value);
#endif
            t += 20;
        } else if (random_value < 30) {
#ifndef QUIET
            printf("Branch 3: random_value = %d\n", random_value);
#endif
            t += 30;
        } else if (random_value < 40) {
#ifndef QUIET
            printf("Branch 4: random_value = %d\n", random_value);
#endif
            t += 40;
        } else if (random_value < 50) {
#ifndef QUIET
            printf("Branch 5: random_value = %d\n", random_value);
#endif
            t += 50;
        } else if (random_value < 60) {
#ifndef QUIET
            printf("Branch 6: random_value = %d\n", random_value);
#endif
            t += 60;
        } else if (random_value < 70) {
#ifndef QUIET
            printf("Branch 7: random_value = %d\n", random_value);
#endif
            t += 70;
        } else if (random_value < 80) {
#ifndef QUIET
            printf("Branch 8: random_value = %d\n", random_value);
#endif
            t += 80;
        } else if (random_value < 90) {
#ifndef QUIET
            printf("Branch 9: random_value = %d\n", random_value);
#endif
            t += 90;
        } else if (random_value < 100) {
#ifndef QUIET
            printf("Branch 10: random_value = %d\n", random_value);
#endif
            t += 100;
        } else if (random_value < 110) {
#ifndef QUIET
            printf("Branch 11: random_value = %d\n", random_value);
#endif
            t += 110;
        } else if (random_value < 120) {
#ifndef QUIET
            printf("Branch 12: random_value = %d\n", random_value);
#endif
            t += 120;
        } else if (random_value < 130) {
#ifndef QUIET
            printf("Branch 13: random_value = %d\n", random_value);
#endif
            t += 130;
#ifndef QUIET
        } else if (random_value < 140) {
            printf("Branch 14: random_value = %d\n", random_value);
#endif
            t += 140;
        } else {
#ifndef QUIET
            printf("Branch 15: random_value = %d\n", random_value);
#endif
            t += 150;
        }
    }

    return 0;
}
