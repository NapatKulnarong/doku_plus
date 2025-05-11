from core.Menu import *
from core.SudokuGame import *
from core.SudokuRenderer import *
from core.constants import *
from features.StatsTracker import StatsTracker
from features.PointTracker import PointTracker
from core.AuthScreen import AuthScreen
from core.UserManager import UserManager
from core.Leaderboard import Leaderboard
from core.PlayScreen import PlayScreen
from core.HowToPlay import HowToPlay
from core.GameStatsScreen import GameStatsScreen
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

        # Initialize sound effects
        pygame.mixer.init()
        self.level_up_sound = pygame.mixer.Sound("assets/sounds/level_up.mp3")
        self.click_sound = pygame.mixer.Sound("assets/sounds/click.mp3")
        self.exit_sound = pygame.mixer.Sound("assets/sounds/exit.mp3")
        self.hint_sound = pygame.mixer.Sound("assets/sounds/hint.mp3")

        # Initialize UI components
        self.play_screen = PlayScreen(self.screen, self.click_sound)
        self.how_to_play_screen = HowToPlay(self.screen)
        self.leaderboard_screen = Leaderboard(self.screen, self.user_manager)
        self.menu = Menu(self.screen)
        self.game = None
        self.renderer = SudokuRenderer(self.screen)

        # Track current screen state: "auth", "menu", or "play"
        self.state = "auth"

        # Track overall stats like hints, wins, time
        self.stats_tracker = StatsTracker()

        # Create the login/authentication screen
        self.auth_screen = AuthScreen(
            self.screen,
            self.user_manager,
            self.handle_login_success,
            self.click_sound
        )

        # Track and animate "level up" celebration
        self.level_up_message_timer = 0

        self.game_stats_screen = GameStatsScreen(self.screen)

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
            # AUTH SCREEN
            if self.state == "auth":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    else:
                        self.auth_screen.handle_event(event)
                self.auth_screen.draw()

            # MAIN MENU
            elif self.state == "menu":
                self.menu.draw(self.point_tracker, self.logged_in_user, self.user_avatar)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        action = self.menu.handle_click(event.pos)
                        if action == "play":
                            self.click_sound.play()
                            self.state = "play_select"
                        elif action == "leaderboard":
                            self.state = "leaderboard"
                        elif action == "stats":
                            self.state = "stats"  # Add this state transition
                        elif action == "exit":
                            self.click_sound.play()
                            running = False
                        elif action == "logout":
                            self.click_sound.play()
                            self.logged_in_user = None
                            self.user_avatar = None
                            self.point_tracker = None
                            self.state = "auth"
                        elif action == "howto":
                            self.click_sound.play()
                            self.state = "howto"

            # GAME STATS SCREEN
            elif self.state == "stats":
                # Only generate stats once when entering this screen
                if not hasattr(self, 'stats_generated'):
                    self.game_stats_screen.generate_stats_once()
                    self.stats_generated = True

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    else:
                        result = self.game_stats_screen.handle_event(event)
                        if result == "menu":
                            self.state = "menu"
                            self.stats_generated = False  # Reset for next visit

                self.game_stats_screen.draw()

            # PLAY SELECTION SCREEN (Easy, Medium, Hard, Advanced)
            elif self.state == "play_select":
                self.play_screen.draw()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        result = self.play_screen.handle_click(event.pos)
                        if result == "menu":
                            self.state = "menu"
                        elif result in ["easy", "medium", "hard", "advanced"]:
                            self.game = SudokuGame(
                                difficulty=result,
                                point_tracker=self.point_tracker,
                                renderer=self.renderer
                            )
                            self.game.start_new_game()
                            self.state = "play"

            # LEADERBOARD SCREEN
            elif self.state == "leaderboard":
                self.leaderboard_screen.draw()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    else:
                        result = self.leaderboard_screen.handle_event(event)
                        if result == "menu":
                            self.state = "menu"

            # HOW TO PLAY SCREEN
            elif self.state == "howto":
                self.how_to_play_screen.draw()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    else:
                        result = self.how_to_play_screen.handle_event(event)
                        if result == "menu":
                            self.state = "menu"

            # GAME SCREEN
            elif self.state == "play":
                self.game.timer.update()
                self.renderer.draw_board(
                    self.game.board,
                    self.game.selected_cell,
                    self.game.last_hint
                )

                pause_button, hint_button, exit_button = self.renderer.draw_elements(
                    self.game.timer.get_time_string(),
                    not self.game.timer.running,
                    self.game.hints_used,
                    self.game.count_filled_cells(),
                    self.level_up_message_timer > 0
                )

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        if y < HEIGHT - 60:
                            self.game.select_cell(event.pos)
                        else:
                            if pause_button.collidepoint(event.pos):
                                self.click_sound.play()
                                self.game.toggle_pause()
                                self.renderer.set_paused(self.game.timer.running is False)
                            elif hint_button.collidepoint(event.pos):
                                hint = self.game.get_hint()
                                if hint:
                                    self.hint_sound.play()
                                    print(f"Hint: {hint}")
                            elif exit_button.collidepoint(event.pos):
                                self.exit_sound.play()
                                self.state = "menu"

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = "menu"
                        elif event.key in [
                            pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                            pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9
                        ]:
                            self.game.input_number(int(pygame.key.name(event.key)))
                        elif event.key in [pygame.K_DELETE, pygame.K_BACKSPACE]:
                            self.game.delete_input()
                        elif event.key == pygame.K_c:
                            self.game.clear_board()
                        elif event.key == pygame.K_h:
                            hint = self.game.get_hint()
                            if hint:
                                self.hint_sound.play()
                                print(f"Hint: {hint}")

                self.renderer.update_display()

                if self.level_up_message_timer > 0:
                    self.level_up_message_timer -= 1

                if self.game.is_completed():
                    stats = self.game.get_completion_stats()
                    self.stats_tracker.log_game(
                        self.game.difficulty,
                        stats["time"],
                        stats["mistakes"],
                        stats["hints"],
                        win=True,
                        filled_cells=stats["points"]
                    )
                    level_up = self.point_tracker.add_points(stats["points"])
                    if level_up:
                        self.level_up_sound.play()
                        self.level_up_message_timer = 180
                    self.renderer.draw_game_over_screen(
                        time_str=stats["time"],
                        hints_used=stats["hints"],
                        mistakes=stats["mistakes"],
                        points_gained=stats["points"]
                    )
                    pygame.time.wait(2000)
                    self.state = "menu"

        pygame.quit()


# Entry point for the game
if __name__ == "__main__":
    controller = GameController()
    controller.run()
