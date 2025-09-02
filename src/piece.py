import os
import pygame

class Piece:

    def __init__(self, name, color, value, size=80):
        self.name = name
        self.color = color
        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign
        self.moves = []
        self.moved = False

        self.set_texture(size)
        self.texture_rect = None

    def set_texture(self, size=80):
        self.texture = os.path.join(
            'assets', 'images', f'imgs-{size}px', f'{self.color}_{self.name}.png'
        )

        self.image = pygame.image.load(self.texture)
        self.image = pygame.transform.scale(self.image, (size, size))

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []

class Pawn(Piece):

    def __init__(self, color):
        self.direction = -1 if color == 'white' else 1
        super().__init__('pawn', color, 1.0)

class Knight(Piece):

    def __init__(self, color):
        super().__init__('knight', color, 3.0)

class Bishop(Piece):

    def __init__(self, color):
        super().__init__('bishop', color, 3.001)

class Rook(Piece):

    def __init__(self, color):
        super().__init__('rook', color, 5.0)

class Queen(Piece):

    def __init__(self, color):
        super().__init__('queen', color, 9.0)

class King(Piece):

    def __init__(self, color):
        super().__init__('king', color, 10000.0)