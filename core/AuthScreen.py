import hashlib
from core.constants import *
from core.constants import AVATARS


class AuthScreen:
    def __init__(self, screen, user_manager, login_success_callback, click_sound):
        # Store references to dependencies
        self.screen = screen
        self.user_manager = user_manager
        self.login_success_callback = login_success_callback
        self.click_sound = click_sound

        self.mode = 'login'  # 'login' or 'create' mode

        # User input state
        self.username = ''
        self.password = ''
        self.error_message = ''
        self.selected_avatar = list(AVATARS.keys())[0]  # Default avatar selected

        # Load fonts (scaled by 1.3)
        self.title_font = pygame.font.Font("assets/fonts/nunito_bold_italic.ttf", int(60 * 1.3))  # 78
        self.label_font = pygame.font.Font("assets/fonts/nunito_bold.ttf", int(22 * 1.3))  # 29
        self.input_font = pygame.font.Font("assets/fonts/nunito_bold.ttf", int(22 * 1.3))  # 29
        self.button_font = pygame.font.Font("assets/fonts/nunito_bold.ttf", int(22 * 1.3))  # 29

        # Preload and scale avatar images (scaled by 1.3)
        self.avatar_images = {
            name: pygame.transform.scale(image, (int(40 * 1.3), int(40 * 1.3)))  # 52x52
            for name, image in AVATARS.items()
        }

        # Focus state
        self.active_input = 'username'

        # UI element placeholders (for clicks)
        self.login_button = None
        self.switch_mode_button = None
        self.username_box = None
        self.password_box = None
        self.avatar_start_y = None  # Y position where avatars start to render

    def draw(self):
        self.screen.fill(NIGHT)  # Fill background

        # --- Title ---
        title_surf = self.title_font.render("DOKU+", True, WHITE)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, int(70 * 1.3)))  # 91
        self.screen.blit(title_surf, title_rect)

        current_y = title_rect.bottom + int(20 * 1.3)  # 26

        # --- Username Label & Box ---
        username_label = self.label_font.render("Username", True, WHITE)
        self.screen.blit(username_label, (WIDTH // 2 - int(100 * 1.3), current_y))
        current_y += int(35 * 1.3)  # 46

        self.username_box = pygame.Rect(WIDTH // 2 - int(100 * 1.3), current_y, int(200 * 1.3), int(40 * 1.3))
        pygame.draw.rect(self.screen, WHITE, self.username_box, border_radius=int(5 * 1.3))
        pygame.draw.rect(self.screen, BLACK, self.username_box, 2, border_radius=int(5 * 1.3))
        username_text = self.input_font.render(self.username, True, BLACK)
        self.screen.blit(username_text, (self.username_box.x + int(5 * 1.3), self.username_box.y + int(5 * 1.3)))
        current_y += int(55 * 1.3)  # 72

        # --- Password Label & Box ---
        password_label = self.label_font.render("Password", True, WHITE)
        self.screen.blit(password_label, (WIDTH // 2 - int(100 * 1.3), current_y))
        current_y += int(35 * 1.3)  # 46

        self.password_box = pygame.Rect(WIDTH // 2 - int(100 * 1.3), current_y, int(200 * 1.3), int(40 * 1.3))
        pygame.draw.rect(self.screen, WHITE, self.password_box, border_radius=int(5 * 1.3))  # 7
        pygame.draw.rect(self.screen, BLACK, self.password_box, 2, border_radius=int(5 * 1.3))
        password_hidden = '*' * len(self.password)
        password_text = self.input_font.render(password_hidden, True, BLACK)
        self.screen.blit(password_text, (self.password_box.x + int(5 * 1.3), self.password_box.y + int(5 * 1.3)))
        current_y += int(65 * 1.3)

        # --- Avatar Selection (Create Mode Only) ---
        self.avatar_start_y = current_y
        if self.mode == 'create':
            self.screen.blit(self.label_font.render
                             ("Choose Avatar:", True, WHITE), (WIDTH // 2 - int(100 * 1.3), current_y))
            current_y += int(40 * 1.3)  # 52

            avatars_per_row = 4
            avatar_spacing = int(50 * 1.3)  # 65
            avatar_size = int(40 * 1.3)  # 52
            start_x = WIDTH // 2 - (avatars_per_row * avatar_spacing) // 2

            for i, (name, avatar_image) in enumerate(self.avatar_images.items()):
                row = i // avatars_per_row
                col = i % avatars_per_row
                x = start_x + col * avatar_spacing
                y = current_y + row * avatar_spacing

                avatar_rect = pygame.Rect(x, y, avatar_size, avatar_size)
                self.screen.blit(avatar_image, avatar_rect)

                # Draw circular highlight for selected avatar
                center = avatar_rect.center
                radius = avatar_size // 2 + 1
                pygame.draw.circle(self.screen, BLACK, center, radius, 3) if name == self.selected_avatar else None

        # --- Bottom Buttons ---
        button_y_start = HEIGHT - int(140 * 1.3)  # 182

        # Display error message above buttons if any
        if self.error_message:
            error_text = self.label_font.render(self.error_message, True, MUSTARD)
            self.screen.blit(error_text, (WIDTH // 2 - error_text.get_width() // 2, button_y_start - int(50 * 1.3)))

        # Login or Create Account Button
        self.login_button = pygame.Rect(WIDTH // 2 - int(100 * 1.3), button_y_start, int(200 * 1.3), int(50 * 1.3))
        pygame.draw.rect(self.screen, MUSTARD, self.login_button, border_radius=int(5 * 1.3))
        pygame.draw.rect(self.screen, BLACK, self.login_button, 2, border_radius=int(5 * 1.3))
        btn_text = "Create Account" if self.mode == 'create' else "Login"
        btn_surf = self.button_font.render(btn_text, True, BLACK)
        self.screen.blit(btn_surf, btn_surf.get_rect(center=self.login_button.center))

        # Switch Mode Button
        self.switch_mode_button = pygame.Rect(WIDTH // 2 - int(100 * 1.3),
                                              button_y_start + int(60 * 1.3), int(200 * 1.3), int(40 * 1.3))
        pygame.draw.rect(self.screen, GRAY, self.switch_mode_button, border_radius=int(5 * 1.3))
        pygame.draw.rect(self.screen, BLACK, self.switch_mode_button, 2, border_radius=int(5 * 1.3))
        switch_text = "Switch to Login" if self.mode == 'create' else "Switch to Create"
        switch_surf = self.button_font.render(switch_text, True, BLACK)
        self.screen.blit(switch_surf, switch_surf.get_rect(center=self.switch_mode_button.center))

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # --- Input field focus ---
            if self.username_box and self.username_box.collidepoint(event.pos):
                self.active_input = 'username'
            elif self.password_box and self.password_box.collidepoint(event.pos):
                self.active_input = 'password'

            # --- Buttons ---
            if self.login_button and self.login_button.collidepoint(event.pos):
                self.click_sound.play()
                self.attempt_auth()
            elif self.switch_mode_button and self.switch_mode_button.collidepoint(event.pos):
                self.click_sound.play()
                self.switch_mode()

            # --- Avatar selection (Create mode only) ---
            if self.mode == 'create' and self.avatar_start_y is not None:
                avatars_per_row = 4
                avatar_spacing = int(50 * 1.3)
                avatar_size = int(40 * 1.3)
                start_x = WIDTH // 2 - (avatars_per_row * avatar_spacing) // 2

                for i, name in enumerate(AVATARS):
                    row = i // avatars_per_row
                    col = i % avatars_per_row
                    x = start_x + col * avatar_spacing
                    y = self.avatar_start_y + int(40 * 1.3) + row * avatar_spacing
                    avatar_rect = pygame.Rect(x, y, avatar_size, avatar_size)
                    if avatar_rect.collidepoint(event.pos):
                        self.click_sound.play()
                        self.selected_avatar = name

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Pressing Enter should trigger the login or create
                self.click_sound.play()
                self.attempt_auth()
            elif self.active_input == 'username':
                if event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                else:
                    self.username += event.unicode
            elif self.active_input == 'password':
                if event.key == pygame.K_BACKSPACE:
                    self.password = self.password[:-1]
                elif event.key != pygame.K_RETURN:
                    self.password += event.unicode

    def switch_mode(self):
        # Toggle between login/create
        self.mode = 'create' if self.mode == 'login' else 'login'
        self.error_message = ''

    def attempt_auth(self):
        password_hash = hashlib.sha256(self.password.encode()).hexdigest()

        if self.mode == 'create':
            # Check for existing user
            if self.user_manager.user_exists(self.username):
                self.error_message = "Username already exists."
                return
            if len(self.username) < 3 or len(self.password) < 3:
                self.error_message = "Username & Password too short."
                return

            # Create new user
            self.user_manager.add_user(self.username, password_hash, self.selected_avatar)

            # Auto login after creation
            if self.login_success_callback:
                self.login_success_callback(self.username, self.selected_avatar)

            # Reset input fields
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

            # Successful login
            if self.login_success_callback:
                avatar = self.user_manager.get_avatar(self.username)
                self.login_success_callback(self.username, avatar)

            # Reset input fields
            self.username = ''
            self.password = ''
            self.error_message = ''
