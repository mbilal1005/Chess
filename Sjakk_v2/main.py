import pygame as pg
import sys

from const import *
from game import Game
from square import *
from move import Move



class Main:


    def __init__(self):
        pg.init()

        self.window = pg.display.set_mode([WIDTH, HEIGHT])

        self.game = Game()


    def mainloop(self):
        window = self.window 
        game = self.game
        dragger = self.game.dragger
        board = self.game.board


        while True:
            game.show_bg(window)
            game.show_last_moves(window)
            game.show_moves(window)
            game.show_pieces(window)

            if dragger.dragging:
                dragger.update_blit(window)

        
            for event in pg.event.get():


                #CLICK
                if event.type == pg.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece 
                        # check if valid piece (color)
                        if piece.color == game.next_player:

                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            
                            #show methods
                            game.show_bg(window)

                            game.show_last_moves(window)

                            game.show_moves(window)

                            game.show_pieces(window)


                    

                    #MOTION
                elif event.type == pg.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        
                        game.show_bg(window)
                        game.show_last_moves(window)
                        game.show_moves(window)
                        game.show_pieces(window)

                        dragger.update_blit(window)



                    #click realese
                elif event.type == pg.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        #create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # Valid move?
                        if board.valid_move(dragger.piece, move):
                            board.move(dragger.piece, move)

                            # show methods 

                            game.show_bg(window)
                            game.show_last_moves(window)

                            game.show_pieces(window)
                            
                            # next turn 

                            game.next_turn()





                    
                    
                     
                    
                    
                    
                    dragger.undrag_piece()



                

                    #avslutt
                elif event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()





            pg.display.update()



main = Main()
main.mainloop()








