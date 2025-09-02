from const import *
from square import Square
from piece import *
from move import Move

class Board:

    def __init__(self):
        self.squares = [[0 for _ in range(COLS)] for _ in range(ROWS)] 

        self._create() 
        self._add_pieces('white')
        self._add_pieces('black')

    def calc_moves(self, piece, row, col):
        ''' 
        Calculate all possible valid moves for a given piece at a specific position.
        '''

        def pawn_moves():
            # pawn steps
            if piece.moved:
                steps = 1
            else:
                steps = 2

            # directional moves
            start = row + piece.direction
            end = row + piece.direction * (steps + 1)
            for move_row in range(start, end, piece.direction):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].is_empty():
                        #create initial and final move squares
                        initial = Square(row, col)
                        final = Square(move_row, col)
                        # create new move
                        move = Move(initial, final)
                        piece.add_move(move)
                    #piece blocked
                    else:
                        break
                # out of range
                else:
                    break

                # diagonal moves
                move_row = row + piece.direction
                move_cols = [col-1, col+1]
                for move_col in move_cols:
                    if Square.in_range(move_row, move_col):
                        if self.squares[move_row][move_col].has_rival_piece(piece.color):
                            # create initial and final move squares
                            initial = Square(row, col)
                            final = Square(move_row, move_col)
                            # create new move
                            move = Move(initial, final)
                            piece.add_move(move)

        def knight_moves(): #8 Possible Moves
            possible_moves = [
                 (row -2, col +1),
                 (row -1, col +2),
                 (row +1, col +2),
                 (row +2, col +1),
                 (row +2, col -1),
                 (row +1, col -2),
                 (row -1, col -2),
                 (row -2, col -1)
            ]
            
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_rival(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create new move
                        move = Move(initial, final)
                        # append valid move to piece
                        piece.add_move(move)
                        
        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                move_row = row + row_incr
                move_col = col + col_incr

                while True:
                    if Square.in_range(move_row, move_col):
                        #create squares of the new move
                        initial = Square(row, col)
                        final = Square(move_row, move_col)
                        move = Move(initial, final)

                        #if empty = continue looping
                        if self.squares[move_row][move_col].is_empty():
                            piece.add_move(move)

                        #has rival piece
                        if self.squares[move_row][move_col].has_rival_piece(piece.color):
                            piece.add_move(move)
                            break

                        # has own piece
                        if self.squares[move_row][move_col].has_team_piece(piece.color):
                            break
                    else:
                        break

                    move_row = move_row + row_incr
                    move_col = move_col + col_incr
        
        def king_moves():
            adjacents = [
                (row -1, col +0), #UP
                (row -1, col +1), #UP RIGHT
                (row +0, col +1), #RIGHT
                (row +1, col +1), #DOWN RIGHT
                (row +1, col +0), #DOWN
                (row +1, col -1), #DOWN LEFT
                (row +0, col -1), #LEFT
                (row -1, col -1)  #UP LEFT
            ]

            for adjacent in adjacents:
                move_row, move_col = adjacent

                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].is_empty_or_rival(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square(move_row, move_col)
                        # create new move
                        move = Move(initial, final)
                        # append valid move to piece
                        piece.add_move(move)
        
        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1, +1), #UP RIGHT
                (-1, -1), #UP LEFT
                (+1, +1), #DOWN RIGHT
                (+1, -1) #DOWN LEFT
            ])

        elif isinstance(piece, Rook):
            straightline_moves([
                (-1, 0), #UP
                (+1, 0), #DOWN
                (0, +1), #RIGHT
                (0, -1) #LEFT
            ])

        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, +1), #UP RIGHT
                (-1, -1), #UP LEFT
                (+1, +1), #DOWN RIGHT
                (+1, -1), #DOWN LEFT
                (-1, 0), #UP
                (+1, 0), #DOWN
                (0, +1), #RIGHT
                (0, -1) #LEFT
            ])

        elif isinstance(piece, King):
            king_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
    
    def _add_pieces(self, color):
        if color == 'white':
            row_pawn, row_other = (6, 7)
        else:
            row_pawn, row_other = (1, 0)

        # Pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
            #self.squares[5][0] = Square(5, 0, Pawn(color))

        # Knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))
        #self.squares[4][4] = Square(row_other, 6, Knight(color))

        # Bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
        #self.squares[5][4] = Square(5, 4, Bishop(color))

        # Rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # Queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        
        # King (fix column from 6 to 4)
        self.squares[row_other][4] = Square(row_other, 4, King(color))
