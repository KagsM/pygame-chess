import pygame
import sys

from const import *
from game import Game
from move import Move
from square import Square

class Main:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.game = Game()
        self.clock = pygame.time.Clock()

    def mainloop(self):

        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board

        while True:
            game.show_background(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                #click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouse_y // SQSIZE
                    clicked_col = dragger.mouse_x // SQSIZE

                    #Check if clicked square has a piece
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece?
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            # show methods
                            game.show_background(screen)

                            game.show_moves(screen)
                            game.show_pieces(screen)
                
                #mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_background(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                #release
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouse_y // SQSIZE
                        released_col = dragger.mouse_x // SQSIZE

                        #create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        #valid move
                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)

                            #sounds
                            game.play_sound(captured)

                        #show methods
                        game.show_background(screen)
                        game.show_pieces(screen)
                        # next turn
                        game.next_turn()

                    dragger.undrag_piece()

                    # key press
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        game.change_theme()

                #quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            

            pygame.display.update()
            #self.clock.tick(240) Uncomment and clock an FPS of 30,60,120 or default if choppy.

main = Main()
main.mainloop()
