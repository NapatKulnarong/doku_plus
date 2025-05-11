import pygame
from core.constants import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.Font("assets/fonts/nunito_bold_italic.ttf", int(72 * 1.3))  # 94
        self.button_font = pygame.font.Font("assets/fonts/nunito_bold.ttf", int(32 * 1.3))  # 47
        self.status_font = pygame.font.Font("assets/fonts/nunito_bold.ttf", int(28 * 1.3))  # 36

        self.buttons = ["Play", "Leaderboard", "How to Play", "Statistics", "Exit Game", "Logout"]
        self.button_rects = []

        self.button_colors = {
            "Play": (MUSTARD, BLACK),
            "Leaderboard": (EGGYOLK, BLACK),
            "How to Play": (GRAPE, BLACK),
            "Statistics": (LIGHT_BLUE, BLACK),
            "Exit Game": (RED, WHITE),
            "Logout": (SMOKE, WHITE),
        }

        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("assets/sounds/click.mp3")

    def draw(self, point_tracker, username=None, avatar=None):
        self.screen.fill(NIGHT)

        title_surface = self.title_font.render("DOKU+", True, WHITE)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 8))
        self.screen.blit(title_surface, title_rect)

        current_y = title_rect.bottom + int(10 * 1.3)  # 13

        if avatar and avatar in AVATARS:
            avatar_img = pygame.transform.scale(AVATARS[avatar], (int(40 * 1.3), int(40 * 1.3)))  # 52x52
            avatar_x = WIDTH // 2 - int(70 * 1.3)  # 91
            avatar_y = current_y
            avatar_rect = pygame.Rect(avatar_x, avatar_y, int(40 * 1.3), int(40 * 1.3))  # 52x52

            # Draw circular white border behind avatar
            pygame.draw.circle(self.screen, WHITE, avatar_rect.center, int(22 * 1.3))  # 29

            # Draw avatar image (square on top of white circle)
            self.screen.blit(avatar_img, (avatar_x, avatar_y))

            avatar_x = WIDTH // 2 - int(70 * 1.3)  # 91
            avatar_y = current_y
            avatar_rect = pygame.Rect(avatar_x, avatar_y, int(40 * 1.3), int(40 * 1.3))  # 52x52

            self.screen.blit(avatar_img, (avatar_x, avatar_y))
            pygame.draw.circle(self.screen, WHITE, avatar_rect.center, int(20 * 1.3), 2)  # 26

            name_surface = self.status_font.render(username, True, WHITE)
            name_rect = name_surface.get_rect(midleft=(avatar_rect.right + int(10 * 1.3), avatar_rect.centery))  # 13
            self.screen.blit(name_surface, name_rect)

            current_y = avatar_rect.bottom + int(10 * 1.3)  # 13

        if point_tracker:
            level = point_tracker.get_level()
            points = point_tracker.get_points()
            points_surface = self.status_font.render(f"Level {level} ({points}/100)", True, WHITE)
            points_rect = points_surface.get_rect(center=(WIDTH // 2, current_y + int(20 * 1.3)))  # 26
            self.screen.blit(points_surface, points_rect)
            current_y = points_rect.bottom + int(20 * 1.3)  # 26

        button_width = int((WIDTH // 2.5) * 1.3)  # ~280 (instead of 351)
        button_height = int(45 * 1.3)  # ~58 (instead of 72)
        spacing = int(10 * 1.3)  # 13 (instead of 16)
        total_height = len(self.buttons) * button_height + (len(self.buttons) - 1) * spacing
        start_y = current_y + int(20 * 1.3)  # 26

        self.button_rects.clear()
        mouse_pos = pygame.mouse.get_pos()

        for i, text in enumerate(self.buttons):
            rect = pygame.Rect(
                (WIDTH - button_width) // 2,
                start_y + i * (button_height + spacing),
                button_width,
                button_height
            )
            self.button_rects.append(rect)

            bg_color, text_color = self.button_colors.get(text, (LIGHT_BLUE, BLACK))
            if rect.collidepoint(mouse_pos):
                bg_color = tuple(max(0, c - 40) for c in bg_color)

            pygame.draw.rect(self.screen, bg_color, rect, border_radius=int(5 * 1.3))  # 7
            pygame.draw.rect(self.screen, BLACK, rect, 2, border_radius=int(5 * 1.3))  # 7

            text_surface = self.button_font.render(text, True, text_color)
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

    def handle_click(self, pos):
        for index, rect in enumerate(self.button_rects):
            if rect.collidepoint(pos):
                self.click_sound.play()
                match self.buttons[index]:
                    case "Play":
                        return "play"
                    case "Leaderboard":
                        return "leaderboard"
                    case "How to Play":
                        return "howto"
                    case "Statistics":  # Add this case
                        return "stats"  # Change this to match the new state
                    case "Exit Game":
                        return "exit"
                    case "Logout":
                        return "logout"
        return None