from typing import Tuple

import pygame

from game.constants import BLOCK_SIZE
from game.textures import BLOCK_TEXTURE


class GridBlock:
    def __init__(self, color: str, pos: Tuple[int, int]):
        """Initialize a new grid block with a given color."""
        self.color = color
        self.pos = pos

    def draw(self, x: int, y: int, screen: pygame.Surface):
        """Draw the block at given coordinates."""
        screen.blit(BLOCK_TEXTURE[self.color], (4 + x - BLOCK_SIZE // 2, 4 + y - BLOCK_SIZE // 2))