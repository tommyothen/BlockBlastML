import random
import sys
from typing import List, Optional, Tuple

import pygame

from game.constants import *
from game.block import *
from game.grid import *
from game.shapes import *
from game.textures import *
from game.fonts import *
from game.colors import *

class Game:
    def __init__(self):
        """Initialize the game, the screen, and the game clock."""
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Block Blast! ML")
        self.clock = pygame.time.Clock()
        self.grid = Grid()
        self.score = 0
        self.next_pieces: List[Optional[Block]] = [None] * NEXT_PIECES_COUNT

    def run(self):
        """Run the main game loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.grid.handle_event(event, self.next_pieces)

            self.manage_next_pieces()

            # Check for any lines cleared
            self.score += self.grid.clear_lines()

            # Check for game over
            if self.check_game_over():
                print("Game Over!")
                running = False

            self.draw()

            pygame.display.update()
            self.clock.tick(60)  # Cap the framerate to 60 FPS
        pygame.quit()
        sys.exit()
                    
    def check_game_over(self) -> bool:
        """Check if any of the next pieces can be placed on the grid."""
        return self.grid.can_place_pieces(self.next_pieces)

    def draw(self):
        """Draw the game onto the screen."""
        self.screen.fill((65, 83, 146))
        self.grid.draw(self.screen)
        self.draw_score()
        self.draw_next_pieces()

        pygame.display.update()

    def draw_score(self):
        """Draw the current score on the screen."""
        score_text = FONT.render(f"{self.score}", True, SCORE_COLOR)
        score_text_rect = score_text.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] * 0.2))
        self.screen.blit(score_text, score_text_rect)

    def manage_next_pieces(self):
        """Manage the next pieces, spawning new ones if necessary."""
        # Only spawn new pieces if all pieces are None
        if all(piece is None for piece in self.next_pieces):
            for i in range(NEXT_PIECES_COUNT):
                self.next_pieces[i] = Block.create_random()

    def draw_next_pieces(self):
        """Draw the next pieces on the screen."""
        spacing = SCREEN_SIZE[0] * 0.1

        # Create a container for the next pieces
        # First, find the total width and height of the container
        total_width = 0
        total_height = 0
        for piece in self.next_pieces:
            if piece is not None:
                total_width += len(piece.shape[0]) * BLOCK_SIZE_SMALL
                total_height = max(total_height, len(piece.shape) * BLOCK_SIZE_SMALL)

        # Add the spacing between the pieces
        total_width += spacing * (NEXT_PIECES_COUNT - 1)

        # Then, create the container
        container = pygame.Surface((total_width, total_height), pygame.SRCALPHA)

        # Make the container's rect
        container_rect = container.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] * 0.85))

        # Draw the next pieces onto the container
        x = 0
        for piece in self.next_pieces:
            if piece is not None:
                piece.draw(x + len(piece.shape[0]) * BLOCK_SIZE_SMALL // 2, total_height // 2, small=True, given_screen=container)
                x += len(piece.shape[0]) * BLOCK_SIZE_SMALL + spacing

        # Draw the container onto the screen
        self.screen.blit(container, container_rect)


