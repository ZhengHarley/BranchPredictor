#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int roll_dice() {
    return rand() % 6 + 1;
}

int main() {
    srand(time(NULL));
    int rounds = 1000;
    int total_score = 0;

#ifndef QUIET
    printf("Rolling dice for %d rounds:\n", rounds);
#endif
    for (int i = 1; i <= rounds; i++) {
        int roll1 = roll_dice();
        int roll2 = roll_dice();
        int round_score = roll1 + roll2;

#ifndef QUIET
        printf("Round %d: Roll1 = %d, Roll2 = %d, Total = %d\n", i, roll1, roll2, round_score);
#endif

        if (roll1 == roll2) {
#ifndef QUIET
            printf("Bonus! Double rolled.\n");
#endif
            round_score += 5; // Bonus for rolling doubles
        }

        total_score += round_score;
    }

#ifndef QUIET
    printf("Final total score: %d\n", total_score);
#endif
    return 0;
}
