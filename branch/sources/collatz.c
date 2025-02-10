#include <stdio.h>

void collatz_sequence(int n) {
#ifndef QUIET
    printf("Collatz sequence for %d: ", n);
#endif
    while (n != 1) {
#ifndef QUIET
        printf("%d ", n);
#endif
        if (n % 2 == 0) {
            n /= 2;
        } else {
            n = 3 * n + 1;
        }
    }
#ifndef QUIET
    printf("1\n");
#endif
}

int main() {
    for (int i = 1; i <= 1000; i++) {
        collatz_sequence(i);
    }
    return 0;
}
