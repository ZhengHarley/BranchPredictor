#include <stdio.h>
#include <stdbool.h>

int main() {
    int count = 0;
    int num = 2;

#ifndef QUIET
    printf("First 100 prime numbers:\n");
#endif

    while (count < 100) {
        bool is_prime = true;

        for (int i = 2; i <= num / 2; i++) {
            if (num % i == 0) {
                is_prime = false;
                break;
            }
        }

        if (is_prime) {
#ifndef QUIET
            printf("%d\n", num);
#endif
            count++;
        }

        num++;
    }

    return 0;
}
