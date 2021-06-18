import pygame
import sys
import random
from pygame import mouse
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME
import checkers_engine as ce


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SQUARE_SIZE = 70


def game_quit():
    pygame.quit()
    sys.exit()


def load_image(name):
    try:
        image = pygame.image.load(name)
    except pygame.error as message:
        print('cannot load an image')
        raise SystemExit(message)
    image = image.convert_alpha()
    return image, image.get_rect()


class Boundries:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def __contains__(self, coords: tuple) -> bool:
        x, y = coords
        return 0 <= x < self.width and 0 <= y < self.height


class Grid(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.rows = 8
        self.columns = 8
        self.square_size = SQUARE_SIZE
        self.grid = pygame.sprite.Group()
        self.pieces = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

    def make_grid(self):
        for column in range(self.columns):
            for row in range(self.rows):
                if (row + column) % 2 == 0:
                    color = WHITE
                else:
                    color = BLACK

                square = Square(
                    self.square_size,
                    (row*self.square_size, column*self.square_size),
                    color)
                self.grid.add(square)

    def get_pieces(self):
        return self.pieces

    def make_pieces(self):

        for row in range(1, self.rows+1):
            for column in range(1, self.columns+1):
                piece = None
                if column < 4:
                    if column % 2 == 0 and row % 2 == 1:
                        piece = Piece(
                            (row*SQUARE_SIZE, column*SQUARE_SIZE), GREEN)
                    if column % 2 == 1 and row % 2 == 0:
                        piece = Piece(
                            (row*SQUARE_SIZE, column*SQUARE_SIZE), GREEN)

                if column > 5:
                    if column % 2 == 0 and row % 2 == 1:
                        piece = Piece(
                            (row*SQUARE_SIZE, column*SQUARE_SIZE), BLUE)
                    if column % 2 == 1 and row % 2 == 0:
                        piece = Piece(
                            (row*SQUARE_SIZE, column*SQUARE_SIZE), BLUE)
                if piece is not None:
                    self.pieces.add(piece)

    def get_grid(self):
        return self.grid

    def get_clicked_piece_coords(self, mouse_sprite_location):
        mouse_sprite = mouse_sprite_location
        pieces = self.get_pieces()
        coords = None
        selected_piece = None

        for piece in pieces:
            if pygame.sprite.collide_rect(piece, mouse_sprite):
                mouse_pos = pygame.mouse.get_pos()
                coords = (mouse_pos[1]//SQUARE_SIZE,
                          mouse_pos[0]//SQUARE_SIZE)
                selected_piece = piece
                break

        if coords is not None and selected_piece is not None:
            return (selected_piece, coords)
        return None, None

    def drag_and_drop(self, selected_piece, piece_coords):
        mouse_pos = pygame.mouse.get_pos()
        selected_piece.move(mouse_pos)

    def make_sprites(self):

        self.make_grid()
        self.make_pieces()
        grid_sprites = self.get_grid()
        pieces_sprites = self.get_pieces()

        self.all_sprites.add(grid_sprites, pieces_sprites)

    def get_all_sprites(self):
        return self.all_sprites


class Square(pygame.sprite.Sprite):
    def __init__(self, size: int, coords: tuple, color: tuple) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.size = size
        self.color = color
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords

    def stick(self, piece):
        piece.move((self.rect.centerx+SQUARE_SIZE//2,
                   self.rect.centery+SQUARE_SIZE//2))


class Piece(pygame.sprite.Sprite):
    def __init__(self, coords: tuple, color: tuple) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.size = SQUARE_SIZE//2
        self.color = color
        self.x_coord, self.y_coord = coords
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x_coord-SQUARE_SIZE//2,
                            self.y_coord-SQUARE_SIZE//2)

    def move(self, coords):
        x_coord, y_coord = coords
        self.rect.center = (x_coord-SQUARE_SIZE//2,
                            y_coord-SQUARE_SIZE//2)


class Sprite_mouse_location(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self._board_size = 8
        self.rect = pygame.Rect(0, 0, 1, 1)

    def get_square_under_mouse(self):
        mouse_position = pygame.Vector2(pygame.mouse.get_pos())
        x_coord = int(mouse_position.x // SQUARE_SIZE)
        y_coord = int(mouse_position.y // SQUARE_SIZE)

        if 0 <= x_coord < self._board_size and 0 <= y_coord < self._board_size:
            return x_coord, y_coord

        return None

    def update(self):
        mouse_position = pygame.Vector2(pygame.mouse.get_pos())
        self.rect.x = mouse_position[0]
        self.rect.y = mouse_position[1]


# pygame stuff
pygame.init()
window_width = 1024
window_height = 768
surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('some checkers')
clock = GAME_TIME.Clock()

# grid stuff
grid = Grid()

# mouse stuff
mouse_sprite_location = Sprite_mouse_location()

selected_piece = None
piece_coords = None
grid.make_sprites()

while True:

    mouse_pos = pygame.mouse.get_pos()
    for event in GAME_EVENTS.get():
        if event.type == GAME_GLOBALS.QUIT:
            game_quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pieces = grid.get_pieces()
            for piece in pieces:
                if pygame.sprite.collide_rect(piece, mouse_sprite_location):
                    selected_piece_coords = (mouse_pos[1]//SQUARE_SIZE,
                                             mouse_pos[0]//SQUARE_SIZE)
                    selected_piece = piece
                    break
        if event.type == pygame.MOUSEBUTTONUP:
            squares = grid.get_grid()
            for square in squares:
                if pygame.sprite.collide_rect(square, mouse_sprite_location) and selected_piece is not None:
                    square.stick(selected_piece)

                    selected_piece = None
                    break

    if selected_piece is not None:
        selected_piece.move(
            (mouse_pos[0]+SQUARE_SIZE//2, mouse_pos[1]+SQUARE_SIZE//2))

    surface.fill((0, 0, 0))
    all_sprites = grid.get_all_sprites()
    all_sprites.update()
    mouse_sprite_location.update()
    all_sprites.draw(surface)

    clock.tick(30)
    pygame.display.update()
