from core.constants import *


class PlayScreen:
    def __init__(self, screen, click_sound):
        self.screen = screen
        self.click_sound = click_sound

        # Scaled fonts (64*1.3=83, 32*1.3=42)
        self.title_font = pygame.font.Font("assets/fonts/nunito_bold_italic.ttf", int(64 * 1.3))
        self.button_font = pygame.font.Font("assets/fonts/nunito_bold.ttf", int(32 * 1.3))

        self.buttons = ["Easy", "Medium", "Hard", "Advanced", "Back to Menu"]
        self.button_rects = []

        self.button_colors = {
            "Easy": MUSTARD,
            "Medium": TIFFANY,
            "Hard": WATER,
            "Advanced": TARO,
            "Back to Menu": GRAY
        }

    def draw(self):
        self.screen.fill(NIGHT)
        button_width = int(300 * 1.2)
        button_height = int(50 * 1.3)
        spacing = int(15 * 1.3)
        start_y = int(165 * 1.3)

        self.button_rects.clear()
        for i, text in enumerate(self.buttons):
            rect = pygame.Rect(
                (WIDTH - button_width) // 2,
                start_y + i * (button_height + spacing),
                button_width,
                button_height
            )
            self.button_rects.append(rect)

            bg_color = self.button_colors.get(text, LIGHT_BLUE)

            pygame.draw.rect(self.screen, bg_color, rect, border_radius=int(8 * 1.3))
            pygame.draw.rect(self.screen, BLACK, rect, 2, border_radius=int(8 * 1.3))

            text_surf = self.button_font.render(text, True, BLACK)
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)

        pygame.display.flip()

    def handle_click(self, pos):
        for index, rect in enumerate(self.button_rects):
            if rect.collidepoint(pos):
                self.click_sound.play()
                text = self.buttons[index]
                if text == "Back to Menu":
                    return "menu"
                return text.lower()
        return None