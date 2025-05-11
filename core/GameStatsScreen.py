import pygame
import os
from core.constants import *
import os.path as path
from features.analytics import graph_generator
import sys
import subprocess


class GameStatsScreen:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.Font("assets/fonts/nunito_bold_italic.ttf", int(56 * 1.3))  # 73
        self.body_font = pygame.font.Font("assets/fonts/nunito_bold.ttf", int(20 * 1.3))  # 26
        self.back_button = pygame.Rect(WIDTH // 2 - int(100 * 1.3), HEIGHT - int(70 * 1.3), int(200 * 1.3),
                                       int(50 * 1.3))
        self.generated_images_folder = "assets/stats_graphs/"
        os.makedirs(self.generated_images_folder, exist_ok=True)

        # Graph configuration - removed width/height since we'll determine dynamically
        self.graphs_config = [
            {"name": "Time Played", "file": "time_played_line.png"},
            {"name": "Mistakes", "file": "mistakes_bar.png"},
            {"name": "Win/Loss", "file": "win_loss_pie.png"},
            {"name": "Hint Usage", "file": "hints_pie.png"},
            {"name": "Time by Difficulty", "file": "time_boxplot.png"},
            {"name": "Correlation", "file": "correlation_matrix.png"},
            {"name": "Time Stats", "file": "time_stats_table.png"}
        ]

        self.scroll_y = 0
        self.scroll_speed = int(30 * 1.7)
        self.total_content_height = 0
        self.stats_generated = False
        self.target_width = int(800 * 1.5)  # Base width for all images

    def generate_stats_once(self):
        if not self.stats_generated:
            if not self.check_images_exist():
                print("Generating stats images...")
                try:
                    from features.analytics import dashboard
                    dashboard.main()
                    self.stats_generated = True
                except Exception as e:
                    print(f"Error generating stats: {e}")
            else:
                self.stats_generated = True

    def check_images_exist(self):
        return all(
            path.exists(path.join(self.generated_images_folder, graph["file"]))
            for graph in self.graphs_config
        )

    def load_and_scale_images(self):
        images = []
        y_offset = 0
        max_width = self.target_width * 0.52

        # First pass to find the maximum width needed
        original_sizes = []
        for config in self.graphs_config:
            filepath = path.join(self.generated_images_folder, config["file"])
            if path.exists(filepath):
                try:
                    original = pygame.image.load(filepath)
                    original_sizes.append((original.get_width(), original.get_height()))
                except:
                    original_sizes.append((0, 0))

        # Second pass to scale all images to same width while maintaining aspect ratio
        for i, config in enumerate(self.graphs_config):
            filepath = path.join(self.generated_images_folder, config["file"])
            if path.exists(filepath) and i < len(original_sizes):
                try:
                    original = pygame.image.load(filepath)
                    orig_width, orig_height = original_sizes[i]

                    if orig_width > 0:  # Only scale if we have valid dimensions
                        # Calculate dimensions to match target width while maintaining aspect ratio
                        scale_factor = max_width / orig_width
                        scaled_width = int(orig_width * scale_factor)
                        scaled_height = int(orig_height * scale_factor)

                        # Use smoothscale for better quality
                        scaled = pygame.transform.smoothscale(original, (scaled_width, scaled_height))

                        x_pos = (WIDTH - scaled_width) // 2
                        images.append({
                            "surface": scaled,
                            "rect": pygame.Rect(x_pos, y_offset, scaled_width, scaled_height),
                            "name": config["name"]
                        })
                        y_offset += scaled_height + int(37 * 1.3)  # Spacing between graphs

                except Exception as e:
                    print(f"Error loading {filepath}: {e}")

        self.total_content_height = y_offset
        return images

    def draw(self):
        self.generate_stats_once()
        self.screen.fill(WHITE)

        # Title
        title = self.title_font.render("Game Statistics", True, BLACK)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, int(20 * 1.3)-20))

        # Create a surface for scrollable content
        content_surface = pygame.Surface((WIDTH, self.total_content_height))
        content_surface.fill(WHITE)

        # Load and draw all graphs
        images = self.load_and_scale_images()
        for img in images:
            # Draw the graph image with antialiasing
            content_surface.blit(img["surface"], img["rect"].topleft)

        # Draw scrollable area
        scroll_area = pygame.Rect(0, int(80 * 1.3), WIDTH, HEIGHT - int(165 * 1.3))
        self.screen.set_clip(scroll_area)
        self.screen.blit(content_surface, (0, int(80 * 1.3) - self.scroll_y))
        self.screen.set_clip(None)

        # Scrollbar if needed
        if self.total_content_height > scroll_area.height:
            scroll_ratio = scroll_area.height / self.total_content_height
            scrollbar_height = scroll_ratio * scroll_area.height
            scrollbar_y = scroll_area.y + (self.scroll_y / self.total_content_height) * scroll_area.height

            pygame.draw.rect(self.screen, GRAY,
                             (WIDTH - int(12 * 1.3), scroll_area.y, int(10 * 1.3), scroll_area.height),
                             border_radius=int(5 * 1.3))
            pygame.draw.rect(self.screen, CARBON,
                             (WIDTH - int(12 * 1.3), scrollbar_y, int(10 * 1.3), scrollbar_height),
                             border_radius=int(5 * 1.3))

        # Back button
        pygame.draw.rect(self.screen, GRAY, self.back_button, border_radius=int(8 * 1.3))
        pygame.draw.rect(self.screen, BLACK, self.back_button, 2, border_radius=int(8 * 1.3))
        back_text = self.body_font.render("Back to Menu", True, BLACK)
        self.screen.blit(back_text, back_text.get_rect(center=self.back_button.center))

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
            elif event.key == pygame.K_UP:
                self.scroll_y = max(0, self.scroll_y - self.scroll_speed)
            elif event.key == pygame.K_DOWN:
                self.scroll_y = min(
                    self.total_content_height - (HEIGHT - int(165 * 1.3)),
                    self.scroll_y + self.scroll_speed
                )

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                return "menu"
            elif event.button == 4:  # Mouse wheel up
                self.scroll_y = max(0, self.scroll_y - self.scroll_speed)
            elif event.button == 5:  # Mouse wheel down
                self.scroll_y = min(
                    self.total_content_height - (HEIGHT - int(165 * 1.3)),
                    self.scroll_y + self.scroll_speed
                )

        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:  # Left mouse button dragged
                self.scroll_y = max(0, min(
                    self.total_content_height - (HEIGHT - int(165 * 1.3)),
                    self.scroll_y - event.rel[1]
                ))

        return None