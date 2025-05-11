import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CARBON = (67, 66, 66)
SMOKE = (104, 109, 118)
GRAY = (200, 200, 200)
RED = (191, 49, 49)
EGGYOLK = (255, 145, 73)
SALMON = (254, 119, 67)
CUSTARD = (255, 240, 133)
MUSTARD = (245, 196, 94)
LEAF = (22, 196, 127)
MINT = (189, 232, 202)
TIFFANY = (100, 204, 197)
TEAL = (13, 124, 102)
LIGHT_BLUE = (96, 216, 232)
CLOUDS = (154, 203, 208)
WATER = (96, 181, 255)
OCEAN = (54, 116, 181)
NIGHT = (39, 84, 138)
WIZARD = (71, 78, 147)
GRAPE = (146, 136, 248)
TARO = (142, 125, 190)
WIDTH, HEIGHT = int(540 * 1.3), int(660 * 1.3)  # 702, 858
BOARD_SIZE = int(540 * 1.3)  # 702
CELL_SIZE = BOARD_SIZE // 9  # This will now be 78 (702/9)
TIMER_HEIGHT = HEIGHT - BOARD_SIZE  # 858 - 702 = 156

AVATARS = {
    "Bear": pygame.image.load("assets/avatars/bear.png"),
    "Black Dog": pygame.image.load("assets/avatars/black_dog.png"),
    "Chick": pygame.image.load("assets/avatars/chick.png"),
    "Gorilla": pygame.image.load("assets/avatars/gorilla.png"),
    "Meerkat": pygame.image.load("assets/avatars/meerkat.png"),
    "Penguin": pygame.image.load("assets/avatars/penguin.png"),
    "Rabbit": pygame.image.load("assets/avatars/rabbit.png"),
    "Seal": pygame.image.load("assets/avatars/seal.png"),
}

pygame.init()