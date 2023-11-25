import random
from typing import List

import pygame

from game.colors import Color
from game.constants import BLOCK_SIZE, BLOCK_SIZE_SMALL, DEBUG
from game.textures import BLOCK_TEXTURE, BLOCK_TEXTURE_SMALL
from game.shapes import BASE_BLOCKS


class Block:
    def __init__(self, shape: List[List[int]], color: Color):
        """Initialize a new block with a given shape and color."""
        self.shape = shape
        self.color = color

        # Randomly rotate the block
        for _ in range(random.randint(0, 3)):
            self.rotate()
    
    def create_random():
        """Spawn a new block with a random shape and color."""
        shape = random.choice(BASE_BLOCKS)
        color = random.choice(list(BLOCK_TEXTURE.keys()))
        return Block(shape, color)

    def rotate(self):
        """Rotate the block 90 degrees clockwise."""
        self.shape = [list(reversed(col)) for col in zip(*self.shape)]

    def draw(self, x: int, y: int, small=False, given_screen=None):
        """Draw the block on the center of the given coordinates."""
        block_size = BLOCK_SIZE_SMALL if small else BLOCK_SIZE
        block_texture = BLOCK_TEXTURE_SMALL[self.color] if small else BLOCK_TEXTURE[self.color]

        # Make a container for the blocks
        block_surface = pygame.Surface((len(self.shape[0]) * block_size, len(self.shape) * block_size), pygame.SRCALPHA)

        # Add a red background for debugging
        if (DEBUG):
            block_surface.fill((255, 0, 0, 100))

        # Draw the blocks onto the container
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j] == 1:
                    block_surface.blit(block_texture, (j * block_size, i * block_size))

        # Draw the container onto the screen
        which_screen = self.screen if given_screen is None else given_screen

        block_surface_rect = block_surface.get_rect(center=(x, y))
        which_screen.blit(block_surface, block_surface_rect)