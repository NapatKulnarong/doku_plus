from core.constants import *
import pygame


class SudokuRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.Font("assets/fonts/nunito_bold_italic.ttf", 72)
        self.title_font_2 = pygame.font.Font("assets/fonts/nunito_bold.ttf", 60)
        self.board_font = pygame.font.Font("assets/fonts/nunito_bold.ttf", 36)
        self.timer_font = pygame.font.Font("assets/fonts/nunito_bold.ttf", 39)
        self.button_font = pygame.font.Font("assets/fonts/nunito_bold.ttf", 28)
        self.hint_font = pygame.font.Font("assets/fonts/nunito_bold.ttf", 34)
        self.gameover_font = pygame.font.Font("assets/fonts/nunito_bold.ttf", 30)

        # Layout configuration
        self.top_margin = 50
        self.bottom_margin = 100
        self.side_margin = 20

        # Grid calculation
        available_width = WIDTH - 2 * self.side_margin
        available_height = HEIGHT - self.top_margin - self.bottom_margin
        self.cell_size = min(available_width // 9, available_height // 9)

        self.grid_width = self.cell_size * 9
        self.grid_height = self.cell_size * 9
        self.grid_origin_x = (WIDTH - self.grid_width) // 2
        self.grid_origin_y = self.top_margin + 35

    def draw_board(self, board, selected_cell, hint_cell=None):
        self.screen.fill(NIGHT)

        for i in range(9):
            for j in range(9):
                x = self.grid_origin_x + j * self.cell_size
                y = self.grid_origin_y + i * self.cell_size

                # Step 1: Fill cell white
                pygame.draw.rect(self.screen, WHITE, (x, y, self.cell_size, self.cell_size))

                # Step 2: If it's a hint cell, overlay yellow highlight
                if hint_cell and (i, j) == hint_cell:
                    pygame.draw.rect(self.screen, MINT, (x, y, self.cell_size, self.cell_size))

                # Step 3: Draw border
                pygame.draw.rect(self.screen, BLACK, (x, y, self.cell_size, self.cell_size), 1)

                # Step 4: Draw number
                if board.board[i][j] != 0:
                    color = BLACK if board.original_board[i][j] != 0 else TEAL
                    text = self.board_font.render(str(board.board[i][j]), True, color)
                    text_rect = text.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
                    self.screen.blit(text, text_rect)

        # Draw grid lines
        for i in range(10):
            line_width = 3 if i % 3 == 0 else 1
            start_x = self.grid_origin_x + i * self.cell_size
            start_y = self.grid_origin_y + i * self.cell_size

            # Vertical
            pygame.draw.line(self.screen, BLACK, (start_x, self.grid_origin_y),
                             (start_x, self.grid_origin_y + self.grid_height), line_width)
            # Horizontal
            pygame.draw.line(self.screen, BLACK, (self.grid_origin_x, start_y),
                             (self.grid_origin_x + self.grid_width, start_y), line_width)

        # Selected cell highlight
        if selected_cell:
            x = self.grid_origin_x + selected_cell[1] * self.cell_size
            y = self.grid_origin_y + selected_cell[0] * self.cell_size
            pygame.draw.rect(self.screen, RED, (x, y, self.cell_size, self.cell_size), 4)

        # Overlay "Game Paused" when paused
        if getattr(self, 'is_paused', False):
            overlay = pygame.Surface((self.grid_width, self.grid_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 220))  # RGBA: semi-transparent black
            self.screen.blit(overlay, (self.grid_origin_x, self.grid_origin_y))

            pause_text = self.title_font_2.render("GAME PAUSED", True, MUSTARD)
            pause_rect = pause_text.get_rect(center=(
                self.grid_origin_x + self.grid_width // 2,
                self.grid_origin_y + self.grid_height // 2
            ))
            self.screen.blit(pause_text, pause_rect)

    def draw_elements(self, time_string, is_paused, hints_used, current_points, show_level_up=False):
        # Top bar (Time and Points)
        pygame.draw.rect(self.screen, NIGHT, (0, 0, WIDTH, self.top_margin))

        timer_text = self.timer_font.render(f"Time: {time_string}", True, WHITE)
        points_text = self.timer_font.render(f"Points: {current_points}", True, WHITE)
        self.screen.blit(timer_text, (self.side_margin, 20))
        points_rect = points_text.get_rect(topright=(WIDTH - self.side_margin, 20))
        self.screen.blit(points_text, points_rect)

        # Level up message
        if show_level_up:
            level_up_text = self.button_font.render("LEVEL UP!", True, RED)
            level_up_rect = level_up_text.get_rect(center=(WIDTH // 2, self.top_margin // 2))
            self.screen.blit(level_up_text, level_up_rect)

        # Bottom bar
        pygame.draw.rect(self.screen, NIGHT, (0, HEIGHT - self.bottom_margin, WIDTH, self.bottom_margin))
        bottom_y = HEIGHT - self.bottom_margin + 30

        hints_text = self.timer_font.render(f"Hints Used: {hints_used}", True, WHITE)
        self.screen.blit(hints_text, (self.side_margin, bottom_y-10))

        # Buttons: Hint, Pause, Exit
        button_width = 117
        button_height = 52
        gap = 10

        # Right-align buttons
        exit_button = pygame.Rect(WIDTH - self.side_margin - button_width, bottom_y-10, button_width, button_height)
        pause_button = pygame.Rect(exit_button.left - gap - button_width, bottom_y-10, button_width, button_height)
        hint_button = pygame.Rect(pause_button.left - gap - button_width, bottom_y-10, button_width, button_height)

        # Draw Hint button
        pygame.draw.rect(self.screen, LEAF, hint_button)
        pygame.draw.rect(self.screen, BLACK, hint_button, 2)
        hint_text_surf = self.button_font.render("Hint", True, BLACK)
        hint_text_rect = hint_text_surf.get_rect(center=hint_button.center)
        self.screen.blit(hint_text_surf, hint_text_rect)

        # Draw Pause button
        pygame.draw.rect(self.screen, MUSTARD, pause_button)
        pygame.draw.rect(self.screen, BLACK, pause_button, 2)
        pause_text = "Resume" if is_paused else "Pause"
        pause_text_surf = self.button_font.render(pause_text, True, BLACK)
        pause_text_rect = pause_text_surf.get_rect(center=pause_button.center)
        self.screen.blit(pause_text_surf, pause_text_rect)

        # Draw Exit button
        pygame.draw.rect(self.screen, RED, exit_button)
        pygame.draw.rect(self.screen, BLACK, exit_button, 2)
        exit_text_surf = self.button_font.render("Exit", True, WHITE)
        exit_text_rect = exit_text_surf.get_rect(center=exit_button.center)
        self.screen.blit(exit_text_surf, exit_text_rect)

        return pause_button, hint_button, exit_button

    def draw_game_over_screen(self, time_str, hints_used, mistakes, points_gained):
        overlay = pygame.Surface((self.grid_width, self.grid_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))  # Semi-transparent black

        self.screen.blit(overlay, (self.grid_origin_x, self.grid_origin_y))

        # Center the text in the overlay
        lines = [
            f"PUZZLE COMPLETED!",
            f"Time Taken: {time_str}",
            f"Hints Used: {hints_used}",
            f"Mistakes Made: {mistakes}",
            f"Points Gained: {points_gained}"
        ]

        for i, line in enumerate(lines):
            text_surf = self.gameover_font.render(line, True, MUSTARD)
            text_rect = text_surf.get_rect(center=(
                self.grid_origin_x + self.grid_width // 2,
                self.grid_origin_y + 145 + i * 50
            ))
            self.screen.blit(text_surf, text_rect)

        pygame.display.flip()

    def set_paused(self, paused):
        self.is_paused = paused

    @staticmethod
    def update_display():
        pygame.display.flip()
