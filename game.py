import random
import numpy as np

class Game2048:
    def __init__(self, size=4):
        """
        Initialize the 2048 game.
        :param size: Size of the grid (default: 4x4)
        """
        self.size = size
        self.grid = np.zeros((size, size), dtype=int)
        self.score = 0
        self.game_over = False
        self._add_new_tile()
        self._add_new_tile()

    def _add_new_tile(self):
        """
        Add a new tile to the grid at a random empty position.
        """
        empty_positions = list(zip(*np.where(self.grid == 0)))
        if empty_positions:
            x, y = random.choice(empty_positions)
            self.grid[x, y] = 2 if random.random() < 0.9 else 4

    def _compress(self, row):
        """
        Compress a single row by sliding non-zero elements to the left.
        :param row: The row to compress
        :return: The compressed row
        """
        row = row[row != 0]
        return np.pad(row, (0, self.size - len(row)), 'constant')

    def _merge(self, row):
        """
        Merge tiles in a row.
        :param row: The row to merge
        :return: The merged row and the score gained
        """
        score_gain = 0
        for i in range(len(row) - 1):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                score_gain += row[i]
                row[i + 1] = 0
        return row, score_gain

    def _move(self, grid):
        """
        Perform a move operation on the grid.
        :param grid: The current grid state
        :return: The updated grid and the score gained
        """
        new_grid = np.zeros_like(grid)
        score_gain = 0

        for i in range(self.size):
            row = grid[i]
            row = self._compress(row)
            row, gain = self._merge(row)
            row = self._compress(row)
            new_grid[i] = row
            score_gain += gain

        return new_grid, score_gain

    def move(self, direction):
        """
        Make a move in the specified direction.
        :param direction: Direction to move ('up', 'down', 'left', 'right')
        """
        if self.game_over:
            return False
        
        original_grid = self.grid.copy() 
        
        # Rotate grid to simulate the direction of movement
        if direction == 'up':
            self.grid = self.grid.T
        elif direction == 'down':
            self.grid = np.fliplr(self.grid.T)
        elif direction == 'right':
            self.grid = np.fliplr(self.grid)

        new_grid, score_gain = self._move(self.grid)

        # Rotate grid back to the original orientation
        if direction == 'up':
            new_grid = new_grid.T
        elif direction == 'down':
            new_grid = np.fliplr(new_grid).T
        elif direction == 'right':
            new_grid = np.fliplr(new_grid)

        self.grid = new_grid
        if not np.array_equal(original_grid, new_grid):
            self.score += score_gain
            self._add_new_tile()
        else:
            return False        

        if not self._can_move():
            self.game_over = True
            
        return True

    def _can_move(self):
        """
        Check if any moves are possible.
        :return: True if a move is possible, False otherwise
        """
        # Check for empty cells
        if np.any(self.grid == 0):
            return True

        # Check for possible merges
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.grid[i, j] == self.grid[i, j + 1] or self.grid[j, i] == self.grid[j + 1, i]:
                    return True

        return False

    def render(self):
        """
        Print the current grid state and score.
        """
        print("Score:", self.score)
        print(self.grid)
