#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
	int t = 0;
	srand(time(NULL));


	for (int i = 0; i < 10000; i++) {
		if (rand() % 2) t++;
	}

#ifndef QUIET
	printf("Total: %i\n", t);
#endif

    return 0;
}
