#include <stdio.h>

int main() {
    int t = 0;
    for (int i = 0; i < 1000; i++) {
        if (i % 4 == 0) t++;
    }

#ifndef QUIET
        printf("%d\n", t);
#endif

    return 0;
}
