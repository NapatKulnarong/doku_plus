import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
SMOKE = (104, 109, 118)
RED = (191, 49, 49)
CUSTARD = (255, 240, 133)
MUSTARD = (245, 196, 94)
LEAF = (22, 196, 127)
MINT = (189, 232, 202)
TIFFANY = (100, 204, 197)
TEAL = (13, 124, 102)
LIGHT_BLUE = (96, 216, 232)
CLOUDS = (154, 203, 208)
OCEAN = (54, 116, 181)
NIGHT = (39, 84, 138)
WIZARD = (71, 78, 147)
WIDTH, HEIGHT = 540, 660
BOARD_SIZE = 540
CELL_SIZE = BOARD_SIZE // 9
TIMER_HEIGHT = HEIGHT - BOARD_SIZE

AVATARS = {
    "Bear": pygame.image.load("assets/avatars/beer.png"),
    "Black Dog": pygame.image.load("assets/avatars/black_dog.png"),
    "Chick": pygame.image.load("assets/avatars/chick.png"),
    "Gorilla": pygame.image.load("assets/avatars/gorilla.png"),
    "Meerkat": pygame.image.load("assets/avatars/meerkat.png"),
    "Penguin": pygame.image.load("assets/avatars/penguin.png"),
    "Rabbit": pygame.image.load("assets/avatars/rabbit.png"),
    "Seal": pygame.image.load("assets/avatars/seal.png"),
}

pygame.init()
