import pygame
import hashlib
from core.constants import *
from core.constants import AVATARS

class AuthScreen:
    def __init__(self, screen, user_manager, login_success_callback, click_sound):
        self.screen = screen
        self.user_manager = user_manager
        self.login_success_callback = login_success_callback
        self.click_sound = click_sound
        self.mode = 'login'

        self.username = ''
        self.password = ''
        self.error_message = ''
        self.selected_avatar = list(AVATARS.keys())[0]

        self.title_font = pygame.font.Font("assets/fonts/nunito_bold_italic.ttf", 60)
        self.label_font = pygame.font.Font("assets/fonts/nunito_bold.ttf", 22)
        self.input_font = pygame.font.Font("assets/fonts/nunito_bold.ttf", 22)
        self.button_font = pygame.font.Font("assets/fonts/nunito_bold.ttf", 22)

        self.avatar_images = {
            name: pygame.transform.scale(image, (40, 40))
            for name, image in AVATARS.items()
        }

        self.active_input = 'username'
        self.login_button = None
        self.switch_mode_button = None
        self.username_box = None
        self.password_box = None
        self.avatar_start_y = None

    def draw(self):
        self.screen.fill(NIGHT)

        title_surf = self.title_font.render("DOKU+", True, WHITE)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 70))
        self.screen.blit(title_surf, title_rect)

        current_y = title_rect.bottom + 20

        username_label = self.label_font.render("Username", True, WHITE)
        self.screen.blit(username_label, (WIDTH // 2 - 100, current_y))
        current_y += 35

        self.username_box = pygame.Rect(WIDTH // 2 - 100, current_y, 200, 40)
        pygame.draw.rect(self.screen, WHITE, self.username_box, border_radius=5)
        pygame.draw.rect(self.screen, BLACK, self.username_box, 2, border_radius=5)
        username_text = self.input_font.render(self.username, True, BLACK)
        self.screen.blit(username_text, (self.username_box.x + 5, self.username_box.y + 5))
        current_y += 55

        password_label = self.label_font.render("Password", True, WHITE)
        self.screen.blit(password_label, (WIDTH // 2 - 100, current_y))
        current_y += 35

        self.password_box = pygame.Rect(WIDTH // 2 - 100, current_y, 200, 40)
        pygame.draw.rect(self.screen, WHITE, self.password_box, border_radius=5)
        pygame.draw.rect(self.screen, BLACK, self.password_box, 2, border_radius=5)
        password_hidden = '*' * len(self.password)
        password_text = self.input_font.render(password_hidden, True, BLACK)
        self.screen.blit(password_text, (self.password_box.x + 5, self.password_box.y + 5))
        current_y += 65

        self.avatar_start_y = current_y
        if self.mode == 'create':
            self.screen.blit(self.label_font.render("Choose Avatar:", True, WHITE), (WIDTH // 2 - 100, current_y))
            current_y += 40

            avatars_per_row = 4
            avatar_spacing = 50
            avatar_size = 40
            start_x = WIDTH // 2 - (avatars_per_row * avatar_spacing) // 2

            for i, (name, avatar_image) in enumerate(self.avatar_images.items()):
                row = i // avatars_per_row
                col = i % avatars_per_row
                x = start_x + col * avatar_spacing
                y = current_y + row * avatar_spacing

                avatar_rect = pygame.Rect(x, y, avatar_size, avatar_size)
                self.screen.blit(avatar_image, avatar_rect)

                center = avatar_rect.center
                radius = avatar_size // 2 + 1
                pygame.draw.circle(self.screen, BLACK, center, radius, 3) if name == self.selected_avatar else None
                # color = RED if name == self.selected_avatar else BLACK
                # # pygame.draw.circle(self.screen, color, center, radius, 2)

        button_y_start = HEIGHT - 140

        if self.error_message:
            error_text = self.label_font.render(self.error_message, True, MUSTARD)
            self.screen.blit(error_text, (WIDTH // 2 - error_text.get_width() // 2, button_y_start - 50))

        self.login_button = pygame.Rect(WIDTH // 2 - 100, button_y_start, 200, 50)
        pygame.draw.rect(self.screen, MUSTARD, self.login_button, border_radius=5)
        pygame.draw.rect(self.screen, BLACK, self.login_button, 2, border_radius=5)
        btn_text = "Create Account" if self.mode == 'create' else "Login"
        btn_surf = self.button_font.render(btn_text, True, BLACK)
        self.screen.blit(btn_surf, btn_surf.get_rect(center=self.login_button.center))

        self.switch_mode_button = pygame.Rect(WIDTH // 2 - 100, button_y_start + 60, 200, 40)
        pygame.draw.rect(self.screen, GRAY, self.switch_mode_button, border_radius=5)
        pygame.draw.rect(self.screen, BLACK, self.switch_mode_button, 2, border_radius=5)
        switch_text = "Switch to Login" if self.mode == 'create' else "Switch to Create"
        switch_surf = self.button_font.render(switch_text, True, BLACK)
        self.screen.blit(switch_surf, switch_surf.get_rect(center=self.switch_mode_button.center))

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.username_box and self.username_box.collidepoint(event.pos):
                self.active_input = 'username'
            elif self.password_box and self.password_box.collidepoint(event.pos):
                self.active_input = 'password'

            if self.login_button and self.login_button.collidepoint(event.pos):
                self.click_sound.play()
                self.attempt_auth()
            elif self.switch_mode_button and self.switch_mode_button.collidepoint(event.pos):
                self.click_sound.play()
                self.switch_mode()

            if self.mode == 'create' and self.avatar_start_y is not None:
                avatars_per_row = 4
                avatar_spacing = 50
                avatar_size = 40
                start_x = WIDTH // 2 - (avatars_per_row * avatar_spacing) // 2

                for i, name in enumerate(AVATARS):
                    row = i // avatars_per_row
                    col = i % avatars_per_row
                    x = start_x + col * avatar_spacing
                    y = self.avatar_start_y + 40 + row * avatar_spacing
                    avatar_rect = pygame.Rect(x, y, avatar_size, avatar_size)
                    if avatar_rect.collidepoint(event.pos):
                        self.click_sound.play()
                        self.selected_avatar = name

        elif event.type == pygame.KEYDOWN:
            if self.active_input == 'username':
                if event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                else:
                    self.username += event.unicode
            elif self.active_input == 'password':
                if event.key == pygame.K_BACKSPACE:
                    self.password = self.password[:-1]
                else:
                    self.password += event.unicode

    def switch_mode(self):
        self.mode = 'create' if self.mode == 'login' else 'login'
        self.error_message = ''

    def attempt_auth(self):
        password_hash = hashlib.sha256(self.password.encode()).hexdigest()

        if self.mode == 'create':
            if self.user_manager.user_exists(self.username):
                self.error_message = "Username already exists."
                return
            if len(self.username) < 3 or len(self.password) < 3:
                self.error_message = "Username & Password too short."
                return

            # Add new user
            self.user_manager.add_user(self.username, password_hash, self.selected_avatar)

            # ✅ Trigger login success callback here
            if self.login_success_callback:
                self.login_success_callback(self.username, self.selected_avatar)

            # Clear state and go to menu
            self.username = ''
            self.password = ''
            self.error_message = ''
            self.switch_mode()

        else:  # Login path
            if not self.user_manager.user_exists(self.username):
                self.error_message = "User not found."
                return
            if not self.user_manager.verify_password(self.username, password_hash):
                self.error_message = "Incorrect password."
                return

            # ✅ Trigger login success callback
            if self.login_success_callback:
                avatar = self.user_manager.get_avatar(self.username)
                self.login_success_callback(self.username, avatar)

            self.username = ''
            self.password = ''
            self.error_message = ''