import pygame as pg

from const import *
from square import Square
from Piece import *
from move import *
from square import *
import copy




class Board():
    def __init__ (self):
        self.squares = [[0,0,0,0,0,0,0,0] for col in range(COLS)] 
        self.last_move = None
        self.create()
        self.leggeTil("white")
        self.leggeTil("black")



    def move(self, piece, move):
        initial = move.initial 
        final = move.final 

        # console board move update
        self.squares[initial.row][initial.col].piece = None 
        self.squares[final.row][final.col].piece = piece


        # pawn promotion 
        if piece.name == "pawn":
            self.check_promotion(piece, final)

        # king casteling 
        if piece.name == "king":
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])


        #move
        piece.moved = True

        #clear valid moves 
        piece.clear_moves()

        # set last move 
        self.last_move = move


    def valid_move(self, piece, move):
        return move in piece.moves


    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2


    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_rival_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True 

        return False




    def calc_moves(self, piece, row, col, bool=True):
        "kalkulerer mulige lvlige trekk for en spesifikk brikke"


        def pawn_moves():
            if piece.moved:
                steps = 1
            else:
                steps = 2 

            #vertikal trekk
            start = row + piece.dir
            end = row + (piece.dir * (1+steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        #create initial and final moves squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)



                        #create new move 
                        move = Move(initial, final)

                        #check if checks 
                        if bool:
                            if not self.in_check(piece, move):

                                piece.add_move(move)
                        else:
                             piece.add_move(move)

                        

                    # blokert 
                    else:
                        break
                # not in range
                else:
                    break


            #diagonal trekk
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1] 
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)

                        move = Move(initial, final)

                        
                        #check if checks 
                        if bool:
                            if not self.in_check(piece, move):

                                piece.add_move(move)
                        else:
                             piece.add_move(move)


        def knight_moves():
            # maks 8 mulige trekk
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1)

            ]

            for possible_move in possible_moves:
                possible_moves_row, possible_moves_col = possible_move

                if Square.in_range(possible_moves_row,possible_moves_col):
                    if self.squares[possible_moves_row][possible_moves_col].isempty_or_rival(piece.color):
                        # a squares of the move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_moves_row][possible_moves_col].piece
                        final = Square(possible_moves_row,possible_moves_col, final_piece)


                        # create move
                        move = Move(initial, final)

                    
                        
                        #check if checks 
                        if bool:
                            if not self.in_check(piece, move):

                                piece.add_move(move)
                            else: 
                                break
                        else:
                             piece.add_move(move)
                      

        def straightlines_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr
           
                while True: 
                    if Square.in_range(possible_move_row,possible_move_col):
                     
                        #create squares of possible new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)

                        #create possible new move
                        move = Move(initial, final)

                        #empty , empty = continue looping 
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            #append new move                        
                            
                            #check if checks 
                            if bool:
                                if not self.in_check(piece, move):

                                    piece.add_move(move)
                            else:
                                piece.add_move(move)



                        #has rival piece, add move og så 'break' 
                        elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                            #append new move 
                            
                            #check if checks 
                            if bool:
                                if not self.in_check(piece, move):

                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            break

                        # team piece , altså den skal 'break' 
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break


                    else:
                        break
                    # incrementing incrs
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [
                (row-1, col+0), # up
                (row-1, col+1), # up-right
                (row+0, col+1), # right
                (row+1, col+1), # down-right
                (row+1, col+0), # down
                (row+1, col-1), # down-left
                (row+0, col-1), # left
                (row-1, col-1), # up-left
            ]
            # normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        # a squares of the move
                        initial = Square(row, col)
                        final = Square(possible_move_row,possible_move_col)

                        # create move
                        move = Move(initial, final)

                        #append new move
                        
                        #check if checks 
                        if bool:
                            if not self.in_check(piece, move):

                                piece.add_move(move)
                            else:
                                break
                        else:
                             piece.add_move(move)

            # castling moves
            if not piece.moved:
                # queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            # castling is not possible because there are pieces in between ?
                            if self.squares[row][c].has_piece():
                                break

                            if c == 3:
                            
                                # adds left rook to king
                                piece.left_rook = left_rook

                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)
                                

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)


                                #check if checks 
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        # append rook
                                        left_rook.add_move(moveR)

                                        # append konge
                                        piece.add_move(moveK)
                                else:
                                    left_rook.add_move(moveR)
                                    piece.add_move(moveK)





                # king cstle
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            # castling is not possible because there are pieces in between ?
                            if self.squares[row][c].has_piece():
                                break

                            if c == 6:
                                print("lei")
                                # adds right rook to king
                                piece.right_rook = right_rook

                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)

                                  #check if checks 
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        # append rook
                                        right_rook.add_move(moveR)

                                        # append konge
                                        piece.add_move(moveK)
                                else:
                                    right_rook.add_move(moveR)
                                    piece.add_move(moveK)

      

        
        if piece.name == 'pawn':
            pawn_moves()


        elif piece.name == 'knight':
            knight_moves()


        elif piece.name == 'bishop':
            straightlines_moves([
                (-1,1), # up ritgh
                (-1,-1), # up left
                (1,1), # down right
                (1,-1), # down left
            ])


        elif piece.name == 'rook':
            straightlines_moves([
                (-1,0), #up
                (0,1), #right
                (1,0), #down 
                (0,-1), #left

            ])


        elif piece.name == 'queen':
            straightlines_moves([
                (-1,1), # up ritgh
                (-1,-1), # up left
                (1,1), # down right
                (1,-1), # down left

                (-1,0), #up
                (0,1), #right
                (1,0), #down 
                (0,-1), #left



            ])

        elif piece.name == 'king':
            king_moves()


    def create(self):

        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)


    def leggeTil(self, color):
        if color == "white":
            row_pawn, row_other = (6,7)
        else: 
            row_pawn, row_other = (1,0)

        #bønder
        for col in range(COLS):
            self.squares[row_pawn] [col] = Square(row_pawn, col, Pawn(color))

        #knights
        self.squares[row_other] [1] = Square(row_other, 1, Knight(color))
        self.squares[row_other] [6] = Square(row_other, 6, Knight(color))

        #bishop
        self.squares[row_other] [2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other] [5] = Square(row_other, 5, Bishop(color))



        #rook
        self.squares[row_other] [0] = Square(row_other, 0, Rook(color))
        self.squares[row_other] [7] = Square(row_other, 7, Rook(color))

        #queen
        self.squares[row_other] [3] = Square(row_other, 3, Queen(color))


        #kong
        self.squares[row_other] [4] = Square(row_other, 4, King(color))


