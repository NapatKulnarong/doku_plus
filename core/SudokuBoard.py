import random

class SudokuBoard:
    def __init__(self, board=None, difficulty="medium"):
        # Store difficulty level
        self.difficulty = difficulty

        # If a board is provided (e.g. for testing or loading), use it
        if board:
            self.board = board  # The current game board (user may modify this)
            self.original_board = [row[:] for row in board]  # Copy for resets
            self.solution_board = [row[:] for row in board]  # Full solution copy
        else:
            # Create empty 9x9 boards for game start
            self.board = [[0 for _ in range(9)] for _ in range(9)]
            self.original_board = [[0 for _ in range(9)] for _ in range(9)]
            self.solution_board = [[0 for _ in range(9)] for _ in range(9)]

    def generate(self):
        # Map difficulty to number of cells to remove
        difficulty_mapping = {
            "easy": 30,
            "medium": 40,
            "hard": 50,
            "advanced": 55
        }
        empty_cells = difficulty_mapping.get(self.difficulty, 40)

        # Step 1: Solve the board fully to generate a complete board
        self.solve()

        # Step 2: Store the full solution for hint checking later
        self.solution_board = [row[:] for row in self.board]

        # Step 3: Remove some cells to form the playable puzzle
        self._remove_numbers(empty_cells)

        # Step 4: Store puzzle state to allow clearing later
        self.original_board = [row[:] for row in self.board]

    def solve(self, i=0, j=0):
        # Backtracking recursive solver
        if i == 9:
            i, j = 0, j + 1
            if j == 9:
                return True  # Fully solved

        if self.board[i][j] != 0:
            return self.solve(i + 1, j)  # Move to next cell

        for num in random.sample(range(1, 10), 9):  # Try random numbers 1-9
            if self._is_valid(num, (i, j)):
                self.board[i][j] = num
                if self.solve(i + 1, j):
                    return True
                self.board[i][j] = 0  # Backtrack

        return False  # No valid number found

    def _is_valid(self, num, pos):
        row, col = pos

        # --- Row check ---
        if any(self.board[row][i] == num for i in range(9) if i != col):
            return False

        # --- Column check ---
        if any(self.board[i][col] == num for i in range(9) if i != row):
            return False

        # --- 3x3 Box check ---
        box_x, box_y = col // 3, row // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.board[i][j] == num and (i, j) != pos:
                    return False

        return True  # All checks passed

    def is_move_valid(self, number, position):
        # Wrapper for public validation
        return self._is_valid(number, position)

    def _remove_numbers(self, count):
        # Randomly remove `count` number of cells from the full board
        removed = 0
        while removed < count:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                removed += 1

    def clear_user_inputs(self):
        # Reset the board back to its original state (before any user input)
        self.board = [row[:] for row in self.original_board]

    def get_cell_hint(self, row, col):
        # Returns the correct answer for a cell, or None if already filled
        if self.board[row][col] != 0:
            return None  # User has already filled this cell

        return self.solution_board[row][col]  # From solved board