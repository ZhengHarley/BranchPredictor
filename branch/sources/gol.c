#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define SIZE 10

void print_grid(int grid[SIZE][SIZE]) {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            printf(grid[i][j] ? "O " : ". ");
        }
        printf("\n");
    }
}

int count_neighbors(int grid[SIZE][SIZE], int x, int y) {
    int count = 0;
    for (int i = -1; i <= 1; i++) {
        for (int j = -1; j <= 1; j++) {
            if (i == 0 && j == 0) continue; // Skip the cell itself
            int nx = x + i, ny = y + j;
            if (nx >= 0 && nx < SIZE && ny >= 0 && ny < SIZE) {
                count += grid[nx][ny];
            }
        }
    }
    return count;
}

void update_grid(int grid[SIZE][SIZE]) {
    int new_grid[SIZE][SIZE] = {0};

    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            int neighbors = count_neighbors(grid, i, j);
            if (grid[i][j] == 1 && (neighbors == 2 || neighbors == 3)) {
                new_grid[i][j] = 1; // Survive
            } else if (grid[i][j] == 0 && neighbors == 3) {
                new_grid[i][j] = 1; // Reproduce
            }
        }
    }

    // Copy new_grid back into grid
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            grid[i][j] = new_grid[i][j];
        }
    }
}

int main() {
    int grid[SIZE][SIZE] = {0};

    // Initial pattern
    grid[1][2] = grid[2][3] = grid[3][1] = grid[3][2] = grid[3][3] = 1;

    for (int t = 0; t < 50; t++) {
#ifndef QUIET
        printf("Generation %d:\n", t);
        print_grid(grid);
#endif
        update_grid(grid);
        // usleep(25000);
#ifndef QUIET
        printf("\n");
#endif
    }

    return 0;
}
