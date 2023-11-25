import pygame
from game.constants import BLOCK_SIZE_SMALL
from game.colors import Color


BLOCK_TEXTURE = {
    Color.BLUE: pygame.image.load("assets/blocks/blue.png"),
    Color.GREEN: pygame.image.load("assets/blocks/green.png"),
    Color.LIGHT_BLUE: pygame.image.load("assets/blocks/light_blue.png"),
    Color.ORANGE: pygame.image.load("assets/blocks/orange.png"),
    Color.PURPLE: pygame.image.load("assets/blocks/purple.png"),
    Color.RED: pygame.image.load("assets/blocks/red.png"),
    Color.YELLOW: pygame.image.load("assets/blocks/yellow.png"),
}

BLOCK_TEXTURE_SMALL = { 
    color: pygame.transform.scale(texture, (BLOCK_SIZE_SMALL, BLOCK_SIZE_SMALL)) for color, texture in BLOCK_TEXTURE.items()
}