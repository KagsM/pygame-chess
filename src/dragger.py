import pygame
from const import *

class Dragger:

    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.initial_row = 0
        self.initial_col = 0

    #blit method

    def update_blit(self, surface):
        #texture
        self.piece.set_texture(size=128)
        texture = self.piece.texture

        #image
        img = pygame.image.load(texture)

        #rect
        img_center = (self.mouse_x, self.mouse_y)
        self.piece.texture_rect = img.get_rect(center=img_center)

        #update blit
        surface.blit(img, self.piece.texture_rect)

    #other methods

    def update_mouse(self, pos):
        self.mouse_x, self.mouse_y = pos #(X, Y)

    def save_initial(self, pos):
        self.initial_row = pos[1] // SQSIZE
        self.initial_col = pos[0] // SQSIZE

    def drag_piece(self, piece):
        self.piece = piece
        self. dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False
