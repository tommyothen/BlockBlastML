import pygame
import random
import sys
from typing import List, Tuple, Optional

# Dev Constants
DEBUG = True

# Constants
SCREEN_SIZE = (720, 1280)
GRID_SIZE = 8
GRID_LINE_WIDTH = 3
BLOCK_SIZE = (SCREEN_SIZE[0] // (GRID_SIZE + 2)) - 1  # Slightly smaller to fit next pieces
NEXT_PIECES_COUNT = 3

# Colors
GRID_LINE_COLOR = (30, 37, 72)
BACKGROUND_COLOR = (39, 42, 83)
SCORE_COLOR = (255, 255, 255)

# Initialize Pygame
pygame.init()
FONT = pygame.font.Font("./Assets/Lato-Black.ttf", 90)
UI_FONT = pygame.font.Font("./Assets/Lato-Black.ttf", 30)

# Load block textures
BLOCK_TEXTURE = {
    "Blue": pygame.image.load("Assets/Blocks/Blue.png"),
    "Green": pygame.image.load("Assets/Blocks/Green.png"),
    "LightBlue": pygame.image.load("Assets/Blocks/LightBlue.png"),
    "Orange": pygame.image.load("Assets/Blocks/Orange.png"),
    "Purple": pygame.image.load("Assets/Blocks/Purple.png"),
    "Red": pygame.image.load("Assets/Blocks/Red.png"),
    "Yellow": pygame.image.load("Assets/Blocks/Yellow.png"),
}

BLOCK_SIZE_SMALL = (BLOCK_SIZE // 1.75)
BLOCK_TEXTURE_SMALL = {
    "Blue": pygame.transform.scale(BLOCK_TEXTURE["Blue"], (BLOCK_SIZE_SMALL, BLOCK_SIZE_SMALL)),
    "Green": pygame.transform.scale(BLOCK_TEXTURE["Green"], (BLOCK_SIZE_SMALL, BLOCK_SIZE_SMALL)),
    "LightBlue": pygame.transform.scale(BLOCK_TEXTURE["LightBlue"], (BLOCK_SIZE_SMALL, BLOCK_SIZE_SMALL)),
    "Orange": pygame.transform.scale(BLOCK_TEXTURE["Orange"], (BLOCK_SIZE_SMALL, BLOCK_SIZE_SMALL)),
    "Purple": pygame.transform.scale(BLOCK_TEXTURE["Purple"], (BLOCK_SIZE_SMALL, BLOCK_SIZE_SMALL)),
    "Red": pygame.transform.scale(BLOCK_TEXTURE["Red"], (BLOCK_SIZE_SMALL, BLOCK_SIZE_SMALL)),
    "Yellow": pygame.transform.scale(BLOCK_TEXTURE["Yellow"], (BLOCK_SIZE_SMALL, BLOCK_SIZE_SMALL)),
}

# Base block shapes
BASE_BLOCKS = [
    [[1, 1]],  # 2x1 block
    [[1, 1, 1]],  # 3x1 block
    [[1, 1, 1, 1]],  # 4x1 block
    [[1, 1, 1, 1, 1]],  # 5x1 block
    [[1, 1], [1, 1]],  # 2x2 block
    [[1, 1, 1, 1], [1, 1, 1, 1]],  # 4x2 block
    [[1, 1, 1], [1, 1, 1], [1, 1, 1]],  # 3x3 block
    [[1, 1, 1], [1, 0, 0], [1, 0, 0]],  # 3x3 - 2x2 block
    [[1, 1], [1, 0]],  # 2x2 - 2x1 block
    [[1, 1, 1], [1, 0, 0]],  # Tetris L block
    [[1, 1, 1], [0, 0, 1]],  # Tetris J block
    [[1, 1, 1], [0, 1, 0]],  # Tetris T block
    [[1, 1], [0, 1], [0, 1]],  # Tetris S block
    [[1, 1], [1, 0], [1, 0]],  # Tetris Z block
    [[1, 0], [0, 1]], # Diagonal 2x2 block
    [[1, 0, 0], [0, 1, 0], [0, 0, 1]], # Diagonal 3x3 block
]


class TextBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255, 255, 255)
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = (255, 0, 0) if self.active else (255, 255, 255)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Block:
    def __init__(self, shape: List[List[int]], color: str):
        """Initialize a new block with a given shape and color."""
        self.shape = shape
        self.color = color

        # Randomly rotate the block
        for _ in range(random.randint(0, 3)):
            self.rotate()

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

class GridBlock:
    def __init__(self, color: str, pos: Tuple[int, int]):
        """Initialize a new grid block with a given color."""
        self.color = color
        self.pos = pos

    def draw(self, x: int, y: int, screen: pygame.Surface):
        """Draw the block at given coordinates."""
        screen.blit(BLOCK_TEXTURE[self.color], (4 + x - BLOCK_SIZE // 2, 4 + y - BLOCK_SIZE // 2))

class Grid:
    def __init__(self):
        """Initialize a new empty grid."""
        self.grid: List[List[Optional[GridBlock]]] = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def draw(self, surface):
        """Draw the grid onto the given surface."""
        grid_width = BLOCK_SIZE * GRID_SIZE
        grid_height = grid_width
        grid_x = (SCREEN_SIZE[0] - grid_width) // 2
        grid_y = (SCREEN_SIZE[1] - grid_height) // 2

        pygame.draw.rect(surface, BACKGROUND_COLOR, (grid_x, grid_y, grid_width, grid_height))

        # Draw the grid lines
        for i in range(GRID_SIZE + 1):
            pygame.draw.line(surface, GRID_LINE_COLOR,
                             (grid_x, grid_y + i * BLOCK_SIZE),
                             (grid_x + grid_width, grid_y + i * BLOCK_SIZE), GRID_LINE_WIDTH)
            pygame.draw.line(surface, GRID_LINE_COLOR,
                             (grid_x + i * BLOCK_SIZE, grid_y),
                             (grid_x + i * BLOCK_SIZE, grid_y + grid_height), GRID_LINE_WIDTH)

        # Draw the blocks
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] is not None:
                    self.grid[i][j].draw(grid_x + (j + 0.5) * BLOCK_SIZE, grid_y + (i + 0.5) * BLOCK_SIZE, surface)


class Game:
    def __init__(self):
        """Initialize the game, the screen, and the game clock."""
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Block Blast! ML")
        self.clock = pygame.time.Clock()
        self.grid = Grid()
        self.score = 0
        self.next_pieces: List[Optional[Block]] = [None] * NEXT_PIECES_COUNT

        self.input_boxes = [TextBox(100, 100, 140, 32),
                            TextBox(100, 150, 140, 32),
                            TextBox(100, 200, 140, 32)]

    def spawn_piece(self) -> Block:
        """Spawn a new block with a random shape and color."""
        shape = random.choice(BASE_BLOCKS)
        color = random.choice(list(BLOCK_TEXTURE.keys()))
        return Block(shape, color)

    def check_game_over(self) -> bool:
        """Check if any of the next pieces can be placed on the grid."""
        for piece in self.next_pieces:
            if piece is None:
                continue
            for y in range(GRID_SIZE):
                for x in range(GRID_SIZE):
                    if self.can_place_piece(piece, x, y):
                        return False
        return True

    def run(self):
        """Run the main game loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                for box in self.input_boxes:
                    box.handle_event(event)

            if all(box.text for box in self.input_boxes):  # Check if all boxes have text
                try:
                    idx = int(self.input_boxes[0].text)
                    x = int(self.input_boxes[1].text)
                    y = int(self.input_boxes[2].text)
                    self.place_piece(idx-1, x-1, y-1)  # Place the piece
                    for box in self.input_boxes:  # Clear the text boxes
                        box.text = ''
                        box.txt_surface = box.font.render(box.text, True, box.color)
                except ValueError:
                    pass  # Handle invalid input


            self.manage_next_pieces()

            # Check for any lines cleared
            self.clear_lines()

            # Check for game over
            if self.check_game_over():
                print("Game Over!")
                running = False

            self.draw()

            pygame.display.update()
            self.clock.tick(60)  # Cap the framerate to 60 FPS
        pygame.quit()
        sys.exit()

    def clear_lines(self):
        """Check if any lines have been cleared."""
        row_index_to_clear = []
        col_index_to_clear = []

        # Check for rows to clear
        for i in range(GRID_SIZE):
            row = self.grid.grid[i]
            if all(block is not None for block in row):
                row_index_to_clear.append(i)

        # Check for columns to clear
        for j in range(GRID_SIZE):
            col = [self.grid.grid[i][j] for i in range(GRID_SIZE)]
            if all(block is not None for block in col):
                col_index_to_clear.append(j)

        # Clear the rows first since they are easier to clear
        for i in row_index_to_clear:
            self.grid.grid[i] = [None for _ in range(GRID_SIZE)]

        # Clear the columns
        for j in col_index_to_clear:
            for i in range(GRID_SIZE):
                self.grid.grid[i][j] = None

        # Add the score
        self.score += len(row_index_to_clear) * 100 + len(col_index_to_clear) * 100

    def draw(self):
        """Draw the game onto the screen."""
        self.screen.fill((65, 83, 146))
        self.grid.draw(self.screen)
        self.draw_score()
        self.draw_next_pieces()

        for box in self.input_boxes:
            box.draw(self.screen)

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
                self.next_pieces[i] = self.spawn_piece()

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

    def place_piece(self, pieceIdx: int, x: int, y: int):
        """Place the given piece on the grid at the given coordinates."""
        piece = self.next_pieces[pieceIdx]
        if piece is None:
            return

        if not self.can_place_piece(piece, x, y):
            print("Cannot place piece here, space occupied.")
            return

        # Place the piece on the grid
        for i in range(len(piece.shape)):
            for j in range(len(piece.shape[i])):
                if piece.shape[i][j] == 1:
                    self.grid.grid[y + i][x + j] = GridBlock(piece.color, (x + j, y + i))

        # Remove the piece from the next pieces
        self.next_pieces[pieceIdx] = None

    def can_place_piece(self, piece: Block, x: int, y: int) -> bool:
        """Check if the given piece can be placed at the given coordinates."""
        # Check if the piece is out of bounds
        for i in range(len(piece.shape)):
            for j in range(len(piece.shape[i])):
                if piece.shape[i][j] == 1:
                    if y + i >= GRID_SIZE or x + j >= GRID_SIZE or self.grid.grid[y + i][x + j] is not None:
                        return False
        return True

if __name__ == "__main__":
    game = Game()
    game.run()
