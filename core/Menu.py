from core.constants import *
from core.constants import AVATARS
import pygame


class Menu:
    def __init__(self, screen):
        # Initialize Menu screen and fonts
        self.screen = screen
        self.title_font = pygame.font.Font("assets/fonts/nunito_bold_italic.ttf", 72)
        self.button_font = pygame.font.Font("assets/fonts/nunito_bold.ttf", 36)
        self.status_font = pygame.font.Font("assets/fonts/nunito_bold.ttf", 28)

        # Initialize menu buttons and selection
        self.selected_difficulty = "medium"
        self.buttons = ["Easy", "Medium", "Hard", "Advanced", "Exit Game", "Logout"]
        self.button_rects = []

        self.button_colors = {
            "Easy": (MUSTARD, WHITE),
            "Medium": (TIFFANY, WHITE),  # Navy background, white text
            "Hard": (OCEAN, WHITE),  # Orange background
            "Advanced": (WIZARD, WHITE),  # Purple background
            "Exit Game": (RED, WHITE),  # Red background, white text
            "Logout": (SMOKE, WHITE),  # Dark gray, white text
        }

        # Initialize sound effects
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("assets/sounds/click.mp3")

    def draw(self, point_tracker, username=None, avatar=None):
        # Clear the screen with white color
        self.screen.fill(NIGHT)

        # Draw the main title
        title_surface = self.title_font.render("DOKU+", True, WHITE)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 8 - 10))
        self.screen.blit(title_surface, title_rect)

        # Draw Avatar and Username (if user is logged in)
        if avatar and avatar in AVATARS:
            # Scale the avatar image to a fixed size
            scaled_avatar_surface = pygame.transform.scale(AVATARS[avatar], (40, 40))

            # Create a circular avatar surface
            avatar_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(avatar_surface, (255, 255, 255, 255), (20, 20), 20)
            scaled_avatar_surface.set_colorkey((0, 0, 0))  # optional: remove any background
            avatar_surface.blit(scaled_avatar_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

            # Define avatar position
            avatar_x = WIDTH // 2 - 70
            avatar_y = title_rect.bottom + 10
            avatar_rect = pygame.Rect(avatar_x, avatar_y, 40, 40)

            # Draw the circular-masked avatar
            self.screen.blit(avatar_surface, (avatar_x, avatar_y))
            pygame.draw.circle(self.screen, WHITE, avatar_rect.center, 20, 2)

            # Draw the username next to the avatar
            if username:
                name_surface = self.status_font.render(username, True, WHITE)
                name_rect = name_surface.get_rect(midleft=(avatar_rect.right + 10, avatar_rect.centery))
                self.screen.blit(name_surface, name_rect)

            current_y = avatar_rect.bottom + 10
        else:
            # If no avatar, continue layout below title
            current_y = title_rect.bottom + 10

        # Draw the user level and points
        current_level = point_tracker.get_level()
        points = point_tracker.get_points()
        points_text = f"Level {current_level} ({points}/100)"
        points_surface = self.status_font.render(points_text, True, WHITE)
        points_rect = points_surface.get_rect(center=(WIDTH // 2, current_y + 20))
        self.screen.blit(points_surface, points_rect)

        # Calculate the dynamic position for buttons
        total_buttons = len(self.buttons)
        button_width = WIDTH // 2
        button_height = 55
        spacing = 12
        total_height = total_buttons * button_height + (total_buttons - 1) * spacing
        start_y = points_rect.bottom + 20

        # Clear existing button rectangles
        self.button_rects.clear()
        mouse_pos = pygame.mouse.get_pos()

        # Draw all menu buttons
        for i, text in enumerate(self.buttons):
            rect = pygame.Rect(
                (WIDTH - button_width) // 2,
                start_y + i * (button_height + spacing),
                button_width,
                button_height
            )
            self.button_rects.append(rect)

            # Get the button color and text color from the dictionary
            bg_color, text_color = self.button_colors.get(text, (LIGHT_BLUE, BLACK))

            # If hovered, darken the button color
            if rect.collidepoint(mouse_pos):
                bg_color = tuple(max(0, c - 40) for c in bg_color)

            # Draw button background and border
            pygame.draw.rect(self.screen, bg_color, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 2)

            # Draw button text
            text_surface = self.button_font.render(text, True, text_color)
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)

        # Update the display
        pygame.display.flip()

    def handle_click(self, pos):
        # Detect if a button was clicked
        for index, rect in enumerate(self.button_rects):
            if rect.collidepoint(pos):
                self.click_sound.play()
                match index:
                    case 0:
                        self.selected_difficulty = "easy"
                        return "play"
                    case 1:
                        self.selected_difficulty = "medium"
                        return "play"
                    case 2:
                        self.selected_difficulty = "hard"
                        return "play"
                    case 3:
                        self.selected_difficulty = "advanced"
                        return "play"
                    case 4:
                        return "exit"
                    case 5:
                        return "logout"
        return None

    def get_selection(self):
        # Return the selected difficulty level
        return self.selected_difficulty