import pygame
from core.constants import *


class Leaderboard:
    def __init__(self, screen, user_manager):
        self.screen = screen
        self.user_manager = user_manager
        self.font = pygame.font.Font("assets/fonts/nunito_bold.ttf", int(20 * 1.3))
        self.title_font = pygame.font.Font("assets/fonts/nunito_bold_italic.ttf", int(54 * 1.3))
        self.header_font = pygame.font.Font("assets/fonts/nunito_bold.ttf", int(22 * 1.3))
        self.back_button = pygame.Rect(WIDTH // 2 - int(100 * 1.3),
                                       HEIGHT - int(70 * 1.3),
                                       int(200 * 1.3), int(45 * 1.3))

        self.scroll_offset = 0
        self.visible_rows = 10  # Show 10 rows max (same count, but rows are taller)

    def draw(self):
        self.screen.fill(NIGHT)

        # Title
        title = self.title_font.render("Leaderboard", True, WHITE)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, int(50 * 1.3))))

        # Table settings
        headers = ["Rank", "Username", "Level"]
        col_widths = [int(80 * 1.3), int(280 * 1.3), int(100 * 1.3)]
        row_height = int(40 * 1.3)
        header_height = int(50 * 1.3)
        padding = int(10 * 1.3)

        table_width = sum(col_widths)
        table_height = header_height + self.visible_rows * row_height
        start_x = WIDTH // 2 - table_width // 2
        start_y = int(100 * 1.3)

        # Draw table background
        table_rect = pygame.Rect(start_x - padding, start_y - padding,
                                 table_width + 2 * padding, table_height + 2 * padding)
        pygame.draw.rect(self.screen, EGGYOLK, table_rect)
        pygame.draw.rect(self.screen, BLACK, table_rect, 2)

        # Draw header
        for i, header in enumerate(headers):
            text = self.header_font.render(header, True, BLACK)
            rect = text.get_rect(center=(start_x + sum(col_widths[:i]) + col_widths[i] // 2, start_y + row_height // 2))
            self.screen.blit(text, rect)

        # Player data
        all_players = self.user_manager.get_top_users()
        total_players = len(all_players)
        visible_players = all_players[self.scroll_offset:self.scroll_offset + self.visible_rows]

        # Draw each visible row
        for i, (name, stats) in enumerate(visible_players):
            row_y = start_y + header_height + i * row_height
            values = [str(self.scroll_offset + i + 1), name, str(stats.get("level", 1))]
            for col, val in enumerate(values):
                text = self.font.render(val, True, BLACK)
                rect = text.get_rect(center=(start_x + sum(col_widths[:col]) + col_widths[col] // 2,
                                             row_y + row_height // 2))
                self.screen.blit(text, rect)

        # Draw back button (already scaled in __init__)
        pygame.draw.rect(self.screen, GRAY, self.back_button, border_radius=int(5 * 1.3))
        pygame.draw.rect(self.screen, BLACK, self.back_button, 2, border_radius=int(5 * 1.3))
        back_text = self.font.render("Back to Menu", True, BLACK)
        self.screen.blit(back_text, back_text.get_rect(center=self.back_button.center))

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                return "menu"

        elif event.type == pygame.KEYDOWN:
            total_users = len(self.user_manager.get_top_users())
            if event.key == pygame.K_DOWN and self.scroll_offset + self.visible_rows < total_users:
                self.scroll_offset += 1
            elif event.key == pygame.K_UP and self.scroll_offset > 0:
                self.scroll_offset -= 1

        return None
