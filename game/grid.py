import math
from typing import List, Optional

import pygame
from pygame.event import Event
from game.block import Block

from game.grid_block import GridBlock
from game.colors import BACKGROUND_COLOR, GRID_LINE_COLOR
from game.constants import BLOCK_SIZE, GRID_LINE_WIDTH, GRID_SIZE, SCREEN_SIZE


class Grid:
    def __init__(self):
        """Initialize a new empty grid."""
        self.grid: List[List[Optional[GridBlock]]] = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.grid_width = BLOCK_SIZE * GRID_SIZE
        self.grid_height = self.grid_width
        self.grid_x = (SCREEN_SIZE[0] - self.grid_width) // 2
        self.grid_y = (SCREEN_SIZE[1] - self.grid_height) // 2

    def clear_lines(self):
        """Check if any lines have been cleared."""
        row_index_to_clear = []
        col_index_to_clear = []

        # Check for rows to clear
        for i in range(GRID_SIZE):
            row = self.grid[i]
            if all(block is not None for block in row):
                row_index_to_clear.append(i)

        # Check for columns to clear
        for j in range(GRID_SIZE):
            col = [self.grid[i][j] for i in range(GRID_SIZE)]
            if all(block is not None for block in col):
                col_index_to_clear.append(j)

        # Clear the rows first since they are easier to clear
        for i in row_index_to_clear:
            self.grid[i] = [None for _ in range(GRID_SIZE)]

        # Clear the columns
        for j in col_index_to_clear:
            for i in range(GRID_SIZE):
                self.grid[i][j] = None

        # return the score
        return len(row_index_to_clear) * 100 + len(col_index_to_clear) * 100
    
    def place_piece(self, piece: Block, x: int, y: int) -> bool:
        """Place the given piece on the grid at the given coordinates."""
        if not self.can_place_piece(piece, x, y):
            print("Cannot place piece here, space occupied.")
            return False

        # Place the piece on the grid
        for i in range(len(piece.shape)):
            for j in range(len(piece.shape[i])):
                if piece.shape[i][j] == 1:
                    self.grid[y + i][x + j] = GridBlock(piece.color, (x + j, y + i))

        return True

    def can_place_piece(self, piece: Block, x: int, y: int) -> bool:
        """Check if the given piece can be placed at the given coordinates."""
        # Check if the piece is out of bounds
        for i in range(len(piece.shape)):
            for j in range(len(piece.shape[i])):
                if piece.shape[i][j] == 1:
                    if y + i >= GRID_SIZE or x + j >= GRID_SIZE or self.grid[y + i][x + j] is not None:
                        return False
        return True
    
    def can_place_pieces(self, pieces: List[Block]) -> bool:
        """Check if any of the next pieces can be placed on the grid."""
        for piece in pieces:
            if piece is None:
                continue
            for y in range(GRID_SIZE):
                for x in range(GRID_SIZE):
                    if self.can_place_piece(piece, x, y):
                        return False
        return True
    
    def handle_event(self, event: Event, pieces: List[Block]):
        if event.type != pygame.KEYDOWN:
            return
            
        if event.key == pygame.K_1:
            pieceIdx = 0
        elif event.key == pygame.K_2:
            pieceIdx = 1
        elif event.key == pygame.K_3:
            pieceIdx = 2
        else:
            return
        
        piece = pieces[pieceIdx]
        if piece is None:
            return
        
        mouse_pos = pygame.mouse.get_pos()
        grid_pos = self.coords_to_grid_pos(*mouse_pos)
        if grid_pos is None:
            return
        
        if self.place_piece(piece, *grid_pos):
            pieces[pieceIdx] = None
        
    def coords_to_grid_pos(self, x, y):
        if x < self.grid_x or self.grid_x + self.grid_width < x:
            return
        if y < self.grid_y or self.grid_y + self.grid_height < y:
            return
        
        grid_pos_x = int((x - self.grid_x) / BLOCK_SIZE)
        grid_pos_y = int((y - self.grid_y) / BLOCK_SIZE)
        return (grid_pos_x, grid_pos_y)


    def draw(self, surface):
        """Draw the grid onto the given surface."""
        pygame.draw.rect(surface, BACKGROUND_COLOR, (self.grid_x, self.grid_y, self.grid_width, self.grid_height))

        # Draw the grid lines
        for i in range(GRID_SIZE + 1):
            pygame.draw.line(surface, GRID_LINE_COLOR,
                             (self.grid_x, self.grid_y + i * BLOCK_SIZE),
                             (self.grid_x + self.grid_width, self.grid_y + i * BLOCK_SIZE), GRID_LINE_WIDTH)
            pygame.draw.line(surface, GRID_LINE_COLOR,
                             (self.grid_x + i * BLOCK_SIZE, self.grid_y),
                             (self.grid_x + i * BLOCK_SIZE, self.grid_y + self.grid_height), GRID_LINE_WIDTH)

        # Draw the blocks
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                grid_block = self.grid[i][j]
                if grid_block is not None:
                    grid_block.draw(self.grid_x + (j + 0.5) * BLOCK_SIZE, self.grid_y + (i + 0.5) * BLOCK_SIZE, surface)

    