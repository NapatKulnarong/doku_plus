from core.constants import *

class HowToPlay:
    def __init__(self, screen):
        self.screen = screen
        # Scaled fonts (56*1.3=73, 19*1.3=25, 20*1.3=26)
        self.title_font = pygame.font.Font("assets/fonts/nunito_bold_italic.ttf", int(56 * 1.3))
        self.body_font = pygame.font.Font("assets/fonts/nunito_bold.ttf", int(19 * 1.3))
        self.button_font = pygame.font.Font("assets/fonts/nunito_bold.ttf", int(20 * 1.3))
        # Scaled back button (100*1.3=130, 80*1.3=104, 200*1.3=260, 50*1.3=65)
        self.back_button = pygame.Rect(WIDTH // 2 - int(100 * 1.3), HEIGHT - int(80 * 1.3), int(200 * 1.3), int(50 * 1.3))
    def draw(self):
        self.screen.fill(NIGHT)

        # Title (60*1.3=78)
        title = self.title_font.render("How To Play", True, WHITE)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, int(60 * 1.3))))

        # Instruction Box (40*1.3=52, 120*1.3=156, 400*1.3=520)
        box_x = int(40 * 1.3)
        box_y = int(120 * 1.3)
        box_width = WIDTH - 2 * box_x
        box_height = int(400 * 1.3)

        instruction_box = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(self.screen, GRAPE, instruction_box)  # GRAPE fill
        pygame.draw.rect(self.screen, BLACK, instruction_box, 2)  # Black border

        # Instruction Text (20*1.3=26, 35*1.3=46)
        instructions = [
            "• Fill every row, column, and 3×3 box with 1–9",
            "• Click a cell to select it",
            "• Type 1–9 to place numbers",
            "• Backspace/Delete to erase",
            "• Press H or click Hint to reveal a cell (no points)",
            "• Press C to clear your inputs",
            "• Earn 1 point per correct move",
            "• Level up every 100 points",
            "• Choose difficulty: Easy -> Advanced",
            "• Press ESC or click below to go back"
        ]

        for i, line in enumerate(instructions):
            rendered = self.body_font.render(line, True, BLACK)
            self.screen.blit(rendered, (box_x + int(20 * 1.3), box_y + int(20 * 1.3) + i * int(35 * 1.3)))

        # Back Button (border_radius 5*1.3=7)
        pygame.draw.rect(self.screen, GRAY, self.back_button, border_radius=int(5 * 1.3))
        pygame.draw.rect(self.screen, BLACK, self.back_button, 2, border_radius=int(5 * 1.3))
        label = self.button_font.render("Back to Menu", True, BLACK)
        self.screen.blit(label, label.get_rect(center=self.back_button.center))

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "menu"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                return "menu"
        return None