import random

class SudokuBoard:
    def __init__(self, board=None, difficulty="medium"):
        self.difficulty = difficulty
        if board:
            self.board = board
            self.original_board = [row[:] for row in board]
            self.solution_board = [row[:] for row in board]  # Safe copy
        else:
            self.board = [[0 for _ in range(9)] for _ in range(9)]
            self.original_board = [[0 for _ in range(9)] for _ in range(9)]
            self.solution_board = [[0 for _ in range(9)] for _ in range(9)]

    def generate(self):
        difficulty_mapping = {
            "easy": 30,
            "medium": 40,
            "hard": 50,
            "advanced": 55
        }
        empty_cells = difficulty_mapping.get(self.difficulty, 40)

        # Step 1: Solve the board fully
        self.solve()

        # Step 2: Copy full solution to solution_board
        self.solution_board = [row[:] for row in self.board]

        # Step 3: Remove numbers to create the puzzle
        self._remove_numbers(empty_cells)

        # Step 4: Copy puzzle state to original_board (for user resets)
        self.original_board = [row[:] for row in self.board]

    def solve(self, i=0, j=0):
        if i == 9:
            i, j = 0, j + 1
            if j == 9:
                return True

        if self.board[i][j] != 0:
            return self.solve(i + 1, j)

        for num in random.sample(range(1, 10), 9):
            if self._is_valid(num, (i, j)):
                self.board[i][j] = num
                if self.solve(i + 1, j):
                    return True
                self.board[i][j] = 0

        return False

    def _is_valid(self, num, pos):
        row, col = pos

        # Check row
        if any(self.board[row][i] == num for i in range(9) if i != col):
            return False

        # Check column
        if any(self.board[i][col] == num for i in range(9) if i != row):
            return False

        # Check 3x3 box
        box_x, box_y = col // 3, row // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.board[i][j] == num and (i, j) != pos:
                    return False

        return True

    def is_move_valid(self, number, position):
        return self._is_valid(number, position)

    def _remove_numbers(self, count):
        removed = 0
        while removed < count:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                removed += 1

    def clear_user_inputs(self):
        self.board = [row[:] for row in self.original_board]

    def get_cell_hint(self, row, col):
        # ✅ Always use solution_board!
        if self.board[row][col] != 0:
            return None  # Already filled

        return self.solution_board[row][col]