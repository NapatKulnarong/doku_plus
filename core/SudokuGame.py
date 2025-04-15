from core.SudokuBoard import *
from core.Timer import *
from core.constants import *

class SudokuGame:
    def __init__(self, difficulty='medium', point_tracker=None, renderer=None):
        self.difficulty = difficulty
        self.board = SudokuBoard(difficulty=self.difficulty)
        self.selected_cell = None
        self.timer = Timer()
        self.mistakes = 0
        self.hints_used = 0
        self.last_hint = None
        self.point_tracker = point_tracker
        self.renderer = renderer
        self.hint_filled_cells = set()  # Stores coordinates of cells filled by hint

    def start_new_game(self):
        self.board = SudokuBoard(difficulty=self.difficulty)
        self.board.generate()
        self.timer.reset()
        self.mistakes = 0

    def select_cell(self, pos):
        if not self.renderer:
            print("Renderer is not set!")
            return

        x, y = pos
        grid_x = x - self.renderer.grid_origin_x
        grid_y = y - self.renderer.grid_origin_y

        if 0 <= grid_x < self.renderer.grid_width and 0 <= grid_y < self.renderer.grid_height:
            col = grid_x // self.renderer.cell_size
            row = grid_y // self.renderer.cell_size
            self.selected_cell = (row, col)
        else:
            self.selected_cell = None

    def input_number(self, number):
        if self.selected_cell:
            row, col = self.selected_cell
            if self.board.original_board[row][col] == 0:
                if self.board.is_move_valid(number, (row, col)):
                    self.board.board[row][col] = number
                else:
                    self.mistakes += 1

    def delete_input(self):
        if self.selected_cell:
            row, col = self.selected_cell
            if self.board.original_board[row][col] == 0:
                self.board.board[row][col] = 0

    def clear_board(self):
        self.board.clear_user_inputs()

    def count_filled_cells(self):
        count = 0
        for i in range(9):
            for j in range(9):
                if self.board.original_board[i][j] == 0 and self.board.board[i][j] != 0:
                    if (i, j) not in self.hint_filled_cells:
                        count += 1
        return count

    def get_hint(self):
        empty_cells = [
            (row, col)
            for row in range(9)
            for col in range(9)
            if self.board.board[row][col] == 0
        ]

        if empty_cells:
            row, col = random.choice(empty_cells)
            hint = self.board.get_cell_hint(row, col)
            if hint:
                self.board.board[row][col] = hint
                self.hints_used += 1
                self.last_hint = (row, col)
                self.hint_filled_cells.add((row, col))
                return (row, col, hint)
        return None

    def is_completed(self):
        board = self.board.board
        for row in board:
            if 0 in row:
                return False
        for row in board:
            if len(set(row)) != 9:
                return False
        for col in range(9):
            column = [board[row][col] for row in range(9)]
            if len(set(column)) != 9:
                return False
        for box_x in range(3):
            for box_y in range(3):
                block = []
                for i in range(box_y * 3, (box_y + 1) * 3):
                    for j in range(box_x * 3, (box_x + 1) * 3):
                        block.append(board[i][j])
                if len(set(block)) != 9:
                    return False
        return True

    def toggle_pause(self):
        if self.timer.running:
            self.timer.pause()
        else:
            self.timer.resume()

    def get_completion_stats(self):
        points_gained = self.count_filled_cells()
        return {
            "time": self.timer.get_time_string(),
            "hints": self.hints_used,
            "mistakes": self.mistakes,
            "points": points_gained
        }