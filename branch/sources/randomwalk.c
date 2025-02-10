#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    int x = 0, y = 0;
    int steps = 1000;

    srand(time(NULL));

#ifndef QUIET
    printf("Random walk simulation (100 steps):\n");
#endif
    for (int i = 0; i < steps; i++) {
        int direction = rand() % 4;

        if (direction == 0) {
            x++;
        } else if (direction == 1) {
            x--;
        } else if (direction == 2) {
            y++;
        } else {
            y--;
        }
#ifndef QUIET
        printf("Step %d: Position (%d, %d)\n", i + 1, x, y);
#endif
    }

#ifndef QUIET
    printf("Final position: (%d, %d)\n", x, y);
#endif
    return 0;
}
