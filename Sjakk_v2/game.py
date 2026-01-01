import pygame as pg

from const import *
from board import *
from square import *
from dragger import *

class Game:
    def __init__(self):
        self.next_player = "white"
        self.board = Board() 
        self.dragger = Dragger()


    def show_bg(self, window):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (229, 228, 200)
                else: 
                    color = (60, 95, 135)

                rect = col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE

                pg.draw.rect(window, color, rect)

    def show_pieces(self, window):
        for row in range(ROWS):
            for col in range(COLS):
                # piece ?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    # ALLE BRIKKER UTENAT DRAGGER
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pg.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        window.blit(img, piece.texture_rect)

    
    def show_moves(self, window):
        if self.dragger.dragging:
            piece = self.dragger.piece

            #LØKKER GJENNOM LOVLIG TREEKK
            for move in piece.moves:
                color = '#C86464' if (move.final.row + move.final.col) % 2 == 0 else '#C84646'

                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)

                pygame.draw.rect(window, color, rect)
    def show_last_moves(self, window):
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # color
                color = (123, 187, 227) if (pos.row + pos.col) % 2 == 0 else (43, 119, 191)
                # rect
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(window, color, rect)





    # other methods 

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'