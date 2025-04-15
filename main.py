# Import required game components and features
from core.Menu import *
from core.SudokuGame import *
from core.SudokuRenderer import *
from core.constants import *
from features.StatsTracker import StatsTracker
from features.PointTracker import PointTracker
from core.AuthScreen import AuthScreen
from core.UserManager import UserManager
import pygame


class GameController:
    def __init__(self):
        # Initialize the game window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Doku+")

        # Store user session info
        self.logged_in_user = None
        self.user_avatar = None

        # Initialize user and point management
        self.user_manager = UserManager()
        self.point_tracker = None  # Created after login

        # Initialize UI components
        self.menu = Menu(self.screen)
        self.game = None
        self.renderer = SudokuRenderer(self.screen)

        # Track current screen state: "auth", "menu", or "play"
        self.state = "auth"

        # Track overall stats like hints, wins, time
        self.stats_tracker = StatsTracker()

        # Initialize sound effects
        pygame.mixer.init()
        self.level_up_sound = pygame.mixer.Sound("assets/sounds/level_up.mp3")
        self.click_sound = pygame.mixer.Sound("assets/sounds/click.mp3")
        self.exit_sound = pygame.mixer.Sound("assets/sounds/exit.mp3")
        self.hint_sound = pygame.mixer.Sound("assets/sounds/hint.mp3")

        # Create the login/authentication screen
        self.auth_screen = AuthScreen(
            self.screen,
            self.user_manager,
            self.handle_login_success,
            self.click_sound
        )

        # Track and animate "level up" celebration
        self.level_up_message_timer = 0

    def handle_login_success(self, username, avatar):
        # Store the login result
        self.logged_in_user = username
        self.user_avatar = avatar

        # Create a point tracker for the logged-in user
        self.point_tracker = PointTracker(self.user_manager, username)

        # Move to the menu screen
        self.state = "menu"

    def run(self):
        running = True
        while running:
            # AUTH SCREEN: Login/Create Account
            if self.state == "auth":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    else:
                        self.auth_screen.handle_event(event)
                self.auth_screen.draw()

            # MENU SCREEN: Difficulty, Logout, Exit
            elif self.state == "menu":
                self.menu.draw(self.point_tracker, self.logged_in_user, self.user_avatar)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        action = self.menu.handle_click(event.pos)

                        # Start new game
                        if action == "play":
                            self.click_sound.play()
                            selected_difficulty = self.menu.get_selection()
                            self.game = SudokuGame(
                                difficulty=selected_difficulty,
                                point_tracker=self.point_tracker,
                                renderer=self.renderer
                            )
                            self.game.start_new_game()
                            self.state = "play"

                        # Exit the app
                        elif action == "exit":
                            self.click_sound.play()
                            running = False

                        # Logout, return to auth
                        elif action == "logout":
                            self.click_sound.play()
                            self.logged_in_user = None
                            self.user_avatar = None
                            self.point_tracker = None
                            self.state = "auth"

            # GAME SCREEN: Sudoku Board Interaction
            elif self.state == "play":
                # Update in-game timer
                self.game.timer.update()

                # Draw the game board
                self.renderer.draw_board(
                    self.game.board,
                    self.game.selected_cell,
                    self.game.last_hint
                )

                # Draw Pause, Hint, Exit buttons and HUD
                pause_button, hint_button, exit_button = self.renderer.draw_elements(
                    self.game.timer.get_time_string(),
                    not self.game.timer.running,
                    self.game.hints_used,
                    self.game.count_filled_cells(),
                    self.level_up_message_timer > 0
                )

                # Handle in-game events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos

                        # Handle board clicks
                        if y < HEIGHT - 60:
                            self.game.select_cell(event.pos)

                        # Handle HUD button clicks
                        else:
                            if pause_button.collidepoint(event.pos):
                                self.click_sound.play()
                                self.game.toggle_pause()
                                self.renderer.set_paused(self.game.timer.running == False)
                            elif hint_button.collidepoint(event.pos):
                                self.hint_sound.play()
                                hint = self.game.get_hint()
                                if hint:
                                    print(f"Hint: {hint}")
                                    self.hint_sound.play()
                            elif exit_button.collidepoint(event.pos):
                                self.exit_sound.play()
                                self.state = "menu"

                    elif event.type == pygame.KEYDOWN:
                        # ESC to return to menu
                        if event.key == pygame.K_ESCAPE:
                            self.state = "menu"

                        # Number input
                        elif event.key in [
                            pygame.K_1, pygame.K_2, pygame.K_3,
                            pygame.K_4, pygame.K_5, pygame.K_6,
                            pygame.K_7, pygame.K_8, pygame.K_9
                        ]:
                            self.game.input_number(int(pygame.key.name(event.key)))

                        # Delete/backspace clears input
                        elif event.key in [pygame.K_DELETE, pygame.K_BACKSPACE]:
                            self.game.delete_input()

                        # 'C' to clear the board
                        elif event.key == pygame.K_c:
                            self.game.clear_board()

                        # 'H' to request a hint
                        elif event.key == pygame.K_h:
                            hint = self.game.get_hint()
                            if hint:
                                print(f"Hint: {hint}")
                                self.hint_sound.play()

                # Redraw updated state
                self.renderer.update_display()

                # Decrease level-up message timer
                if self.level_up_message_timer > 0:
                    self.level_up_message_timer -= 1

                # Check game completion
                if self.game.is_completed():
                    time_taken = self.game.timer.get_time_string()
                    mistakes = self.game.mistakes
                    hints_used = self.game.hints_used
                    difficulty = self.game.difficulty
                    filled_cells = self.game.count_filled_cells()

                    # Log the game stats
                    self.stats_tracker.log_game(
                        difficulty, time_taken, mistakes,
                        hints_used, win=True, filled_cells=filled_cells
                    )

                    # Award points and check level up
                    level_up = self.point_tracker.add_points(filled_cells)
                    if level_up:
                        self.level_up_sound.play()
                        self.level_up_message_timer = 180

                    stats = self.game.get_completion_stats()
                    self.renderer.draw_game_over_screen(
                        time_str=stats["time"],
                        hints_used=stats["hints"],
                        mistakes=stats["mistakes"],
                        points_gained=stats["points"]
                    )
                    pygame.time.wait(2000)  # 2-second delay before returning to menu

                    print("Congratulations! You've solved the puzzle!")
                    self.state = "menu"

        # Exit pygame when done
        pygame.quit()


# Entry point for the game
if __name__ == "__main__":
    controller = GameController()
    controller.run()
