#include <stdio.h>

int fibonacci(int n) {
    if (n <= 1) {
        return n;
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}

int main() {
#ifndef QUIET
    printf("Fibonacci sequence up to 25th number:\n");
#endif
    for (int i = 0; i < 25; i++) {
        int f = fibonacci(i);
#ifndef QUIET
        printf("%d ", f);
#endif
    }
#ifndef QUIET
    printf("\n");
#endif
    return 0;
}
