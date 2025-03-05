import tkinter as tk
from tkinter import *
import time

class CheckersBoardGUI:
    def __init__(self):
        # setting up the board and its attributes
        self.board = tk.Tk()
        self.board.title("Checkers")
        self.board.geometry("450x450")
        self.board.config(background="black")

        self.canvas = tk.Canvas(self.board, width=400, height=400)
        self.canvas.pack(padx=10, pady=10)

        # setting up piece values for future reference and use
        self.turn = "red"
        self.choice_active_dir1 = False
        self.choice_active_dir2 = False
        self.original_piece = None
        self.consumable_piece = None
        self.consumed_position = None
        self.ascended_movement = False
        self.ascended_consumption = False
        self.consumable_piece_found = False

        # setting up piece counters for each side to check for victory
        self.black_pieces = 0
        self.red_pieces = 0

        self.square_size = 50
        self.piece_size = 30
        
        
        # prepearing board initialization
        self.piece_repr = self.board_initialization()
        self.draw_board()

        self.board.mainloop()


        
    def board_initialization(self):
        # array of arrays representing the checkers board with its rows and columns and its pieces
        return [
            [None, Piece("black"), None, Piece("black"), None, Piece("black"), None, Piece("black")],
            [Piece("black"), None, Piece("black"), None, Piece("black"), None, Piece("black"), None],
            [None, Piece("black"), None, Piece("black"), None, Piece("black"), None, Piece("black")],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Piece("red"), None, Piece("red"), None, Piece("red"), None, Piece("red"), None],
            [None, Piece("red"), None, Piece("red"), None, Piece("red"), None, Piece("red")],
            [Piece("red"), None, Piece("red"), None, Piece("red"), None, Piece("red"), None]
        ]
    


    def draw_board(self):
        # deleting all previous enteties on the canvas to draw board
        self.canvas.delete("all")

        self.red_pieces = 0
        self.black_pieces = 0

        # for loop calculating and drawing the board and pieces on its
        for row in range(8):
            for col in range(8):
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size

                if (row + col) % 2 == 0:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="gray", outline="black")

                piece = self.piece_repr[row][col]

                # checking if drawn pieces are elligable for ascension to queen status
                if piece is not None:
                    if piece.color == "black":
                        self.black_pieces += 1
                        if piece.color == "black" and row == 7:
                            piece.has_ascended()
                    if piece.color == "red":
                        self.red_pieces += 1
                        if piece.color == "red" and row == 0:
                            piece.has_ascended()

                if piece is not None:
                    piece_color = piece.color
                    offset = (self.square_size - self.piece_size) // 2
                    piece_id = self.canvas.create_rectangle(
                        x1 + offset, y1 + offset, 
                        x1 + offset + self.piece_size,
                        y1 + offset + self.piece_size, 
                        fill=piece_color,
                        outline="white"
                    )
                    if piece.ascended == True: # if found piece is a queen piece, small white square within created to distinguish
                        self.piece_size = 10
                        offset = (self.square_size - self.piece_size) // 2
                        piece_id = self.canvas.create_rectangle(
                        x1 + offset, y1 + offset, 
                        x1 + offset + self.piece_size,
                        y1 + offset + self.piece_size, 
                        fill="white",
                        outline="black"
                        )
                        self.piece_size = 30


                    
                    self.canvas.tag_bind(piece_id, "<Button-1>", lambda event, r=row, c=col: self.piece_clicked(event, r, c))

        # if one side has no pieces left win screen created
        if self.red_pieces == 0:
            self.win_screen("The Black side has won!")
        if self.black_pieces == 0:
            self.win_screen("The Red side has won!")

        self.black_on_board = tk.Label(width=25,fg="black",bg="darkgray",text=f"remaining black pieces : {self.black_pieces}")
        self.red_on_board = tk.Label(width=25,fg="black",bg="maroon",text=f"remaining red pieces : {self.red_pieces}")
        self.black_on_board.pack(padx=5,pady=3)
        self.red_on_board.pack(padx=5,pady=3)






    def piece_clicked(self, event, row, col):
        piece = self.piece_repr[row][col]

        self.ascended_consumption = False
        self.ascended_movement = False

        
        if piece is not None:
            new_row = row + 1 if piece.color == "black" else row - 1

        self.black_on_board.destroy()
        self.red_on_board.destroy()

        def move_piece():
            if self.original_piece is not None and (self.choice_active_dir1 == True or self.choice_active_dir2 == True or self.choice_active_q == True) and piece.color in ["navy", "yellow"]:
                orig_row, orig_col, orig_color, is_ascended = self.original_piece

                # clear the original position
                self.piece_repr[orig_row][orig_col] = None
                new_piece = Piece(orig_color)

                # retaining original ascended status
                new_piece.ascended = is_ascended

                # move the piece to the new position
                self.piece_repr[row][col] = new_piece
                self.choice_active_dir1 = False
                self.choice_active_dir2 = False
                self.original_piece = None
                self.ascended_consumption = False
                self.ascended_movement = False

                self.turn = "red" if orig_color == "black" else "black"

                self.choices_cleared()
        
        move_piece()

        def forced_consumption():
            if self.original_piece and self.consumable_piece and self.consumed_position is not None:
                orig_row, orig_col, orig_color, is_ascended = self.original_piece
                eaten_row, eaten_col, eaten_color = self.consumable_piece
                cons_row, cons_col, cons_color = self.consumed_position
                self.draw_board()


                # clear original piece
                self.piece_repr[orig_row][orig_col] = None

                # move/create original piece in consumed jump position
                self.piece_repr[cons_row][cons_col] = Piece(orig_color)

                # retaining ascended status
                self.piece_repr[cons_row][cons_col].ascended = is_ascended

                # deleting eaten piece
                self.piece_repr[eaten_row][eaten_col] = None

                jump_check()

                self.turn = "red" if orig_color == "black" else "black"

                # clearing values for further moves
                self.choice_active_q = False
                self.choice_active_dir1 = False
                self.choice_active_dir2 = False
                self.original_piece = None
                self.consumable_piece = None
                self.consumed_position = None
                self.ascended_consumption = False
                self.ascended_movement = False
                # self.consumable_piece_found = False
                self.choices_cleared()
                
        self.choices_cleared()
        
        def jump_check():
            orig_row, orig_col, orig_color, is_ascended = self.original_piece
            cons_row, cons_col, cons_color = self.consumed_position

            # redifining new row to be used new "original" piece
            new_row = cons_row + 1 if orig_color == "black" else cons_row - 1

            # checking for possible consumable pieces after original move
            if 0 <= new_row < 8 and 0 <= cons_col + 1 < 8:

                # reusable module to check paramaters for multi-eating functionality
                def check_move(new_row, cons_col, row_op, col_op, col_op2, orig_color):
                    check_row = row_op(cons_row)
                    check_col = col_op(cons_col)
                    check_col2 = col_op2(cons_col)
                    if self.piece_repr[new_row][check_col] is not None:
                        # making sure jump/multi eat pieces are not protected
                        prot_check_row = row_op(check_row) 
                        prot_check_col = col_op(check_col)
                        if 0 <= prot_check_row < 8 and 0 <= prot_check_col < 8 and self.piece_repr[prot_check_row][prot_check_col] is None: # making sure potential jump positions not out of bounds
                            if (orig_color == "red" and self.piece_repr[new_row][check_col].color == "black") or (orig_color == "black" and self.piece_repr[new_row][check_col].color == "red"):
                                if 0 <= check_row < 8 and 0 <= check_col < 8 and check_col2:
                                    if self.piece_repr[check_row][check_col2] is None:
                                        self.consumable_piece = (new_row, check_col, self.piece_repr[new_row][check_col].color)
                                        self.consumed_position = (prot_check_row, prot_check_col, orig_color)
                                        self.original_piece = (cons_row, cons_col, orig_color, is_ascended)
                                        forced_consumption()
                
                
                # executing function to check north for jump positions if queen piece or black piece
                if orig_color == "black" or is_ascended == True:
                    check_move(new_row, cons_col, lambda x:x+1, lambda x:x+1, lambda x:x+2, orig_color) # checking NW for multi-comsumption

                    check_move(new_row, cons_col, lambda x:x+1, lambda x:x-1, lambda x:x-2, orig_color) # checking NE for multi-comsumption
                
                # executing function to check south for jump positions if queen piece or red piece
                if orig_color == "red" or is_ascended == True:
                    check_move(new_row, cons_col, lambda x:x-1, lambda x:x+1, lambda x:x+2, orig_color) # checking SW for multi-comsumption

                    check_move(new_row, cons_col, lambda x:x-1, lambda x:x-1, lambda x:x-2, orig_color) # checking SE for multi-comsumption

                self.choices_cleared()




        # checking for movement or consumption possibilities for ordinary pieces then sending values to forced consumption if found
        if piece is not None:
            if piece.color == "black" and self.turn == "black" and piece.ascended == False:
                if col + 1 < 8  and self.piece_repr[new_row][col + 1] is not None and self.piece_repr[new_row][col + 1].color == "red":
                    if col + 2 < 8 and new_row + 1 < 8 and self.piece_repr[new_row + 1][col + 2] is None:
                        self.consumable_piece = (new_row, col + 1, "red")
                        self.consumed_position = (new_row + 1, col + 2, piece.color)
                        self.original_piece = (row, col, piece.color, False)
                        self.consumable_piece_found = True
                        forced_consumption()
                if col - 1 >= 0 and self.piece_repr[new_row][col - 1] is not None and self.piece_repr[new_row][col - 1].color == "red":
                    if col - 2 < 8 and new_row + 1 < 8 and self.piece_repr[new_row + 1][col - 2] is None:
                        self.consumed_position = (new_row + 1, col - 2, piece.color)
                        self.consumable_piece = (new_row, col - 1, "red")
                        self.original_piece = (row, col, piece.color, False)
                        self.consumable_piece_found = True
                        forced_consumption()



                if col + 1 < 8 and self.choice_active_dir1 == False and self.piece_repr[new_row][col + 1] is None and self.consumable_piece_found == False:
                    self.piece_repr[new_row][col + 1] = Piece("navy")
                    self.original_piece = (row, col, piece.color, False)
                    self.choice_active_dir1 = True
                if col - 1 >= 0 and self.choice_active_dir2 == False and self.piece_repr[new_row][col - 1] is None and self.consumable_piece_found == False:
                    self.piece_repr[new_row][col - 1] = Piece("navy")
                    self.original_piece = (row, col, piece.color, False)
                    self.choice_active_dir2 = True   
                    



            if piece.color == "red" and self.turn == "red" and piece.ascended == False:
                if col + 1 < 8 and self.piece_repr[new_row][col + 1] is not None and self.piece_repr[new_row][col + 1].color == "black":
                    if new_row - 1 >= 0 and col + 2 < 8 and self.piece_repr[new_row - 1][col + 2] is None:
                        self.consumed_position = (new_row - 1, col + 2, piece.color)
                        self.consumable_piece = (new_row, col + 1, "black")
                        self.original_piece = (row, col, piece.color, False)
                        self.consumable_piece_found = True
                        forced_consumption()
                if col - 1 >= 0 and self.piece_repr[new_row][col - 1] is not None and self.piece_repr[new_row][col - 1].color == "black":
                    if new_row - 1 >= 0 and col - 2 < 8 and self.piece_repr[new_row - 1][col - 2] is None:
                        self.consumed_position = (new_row - 1, col - 2, piece.color)
                        self.consumable_piece = (new_row, col - 1, "black")
                        self.original_piece = (row, col, piece.color, False)
                        self.consumable_piece_found = True
                        forced_consumption()


                        
                if col + 1 < 8 and self.choice_active_dir1 == False and self.piece_repr[new_row][col + 1] is None and self.consumable_piece_found == False:
                    self.piece_repr[new_row][col + 1] = Piece("yellow")
                    self.original_piece = (row, col, piece.color, False)
                    self.choice_active_dir1 = True
                if col - 1 >= 0 and self.choice_active_dir2 == False and self.piece_repr[new_row][col - 1] is None and self.consumable_piece_found == False:
                    self.piece_repr[new_row][col - 1] = Piece("yellow")
                    self.original_piece = (row, col, piece.color, False)
                    self.choice_active_dir2 = True   
        


        def ascended_movement():
            if piece is not None:
                if piece.ascended:
                    self.original_piece = (row, col, piece.color, True)
                    if (piece.color == "red" and self.turn == "red") or (piece.color == "black" and self.turn == "black"):
                        self.choice_active_q = True
                        orig_row, orig_col, orig_color, is_ascended = self.original_piece
                        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # NE NW SE and SW
                        # itterating through board to see possible movement or eating positions
                        for dr, dc in directions:
                            r, c = row, col
                            while True:
                                r += dr
                                c += dc
                                if 0 <= r < 8 and 0 <= c < 8:
                                    if self.piece_repr[r][c] is None: # checking for potential movement positionsa and marking them
                                        highlight_color = "navy" if piece.color == "black" else "yellow"
                                        self.piece_repr[r][c] = Piece(highlight_color)
                                        self.original_piece = (row, col, piece.color, True)
                                        self.ascended_movement = True


                                    def directional_check(color,r_check,c_check,r_op,c_op):
                                        r_next = r_op(r)  # applying row operation
                                        c_next = c_op(c)  # applying column operation
                                        if self.piece_repr[r_next][c_next] is None:
                                            self.consumed_position = (r_next, c_next, orig_col)
                                            self.consumable_piece = (r, c, "black")
                                            self.original_piece = (orig_row, orig_col, orig_color, is_ascended)
                                            self.ascended_consumption = True
                                            self.choice_active_q = True
                                            forced_consumption()
                                            self.choices_cleared()


                                    if self.piece_repr[r][c] is not None and (self.piece_repr[r][c].color == "black" and orig_color == "red"):
                                            
                                        if (r - 1 >= 0 and c - 1 >= 0) and (r + 1 < 8 and c + 1 < 8):
                                            if self.piece_repr[r - 1][c - 1] is None:
                                                if orig_row > r and orig_col > c:
                                                    # checking NW
                                                    directional_check(piece.color, r, c, lambda x: x - 1, lambda x: x - 1)
                                                    break
                                            if self.piece_repr[r - 1][c + 1] is None:
                                                if orig_row > r and orig_col < c:
                                                    # checking NE
                                                    directional_check(piece.color, r, c, lambda x: x - 1, lambda x: x + 1)
                                                    break
                                            if self.piece_repr[r + 1][c + 1] is None:
                                                if orig_row < r and orig_col < c:
                                                    # checking SE
                                                    directional_check(piece.color, r, c, lambda x: x + 1, lambda x: x + 1)
                                                    break
                                            if self.piece_repr[r + 1][c - 1] is None:
                                                if orig_col > c and orig_row < r:
                                                    # checking SW
                                                    directional_check(piece.color, r, c, lambda x: x + 1, lambda x: x - 1)
                                                    break
                                            break # stopping if protected piece found

                                        if self.piece_repr[r][c] is not None:
                                            if self.piece_repr[r][c].color == orig_color:  # checking color
                                                break  # stop movement in direction if piece of same side found
                        


                                    if self.piece_repr[r][c] is not None and (self.piece_repr[r][c].color == "red" and orig_color == "black"):
                                            
                                        if (r - 1 >= 0 and c - 1 >= 0) and (r + 1 < 8 and c + 1 < 8):
                                            if self.piece_repr[r - 1][c - 1] is None:
                                                if orig_row > r and orig_col > c:
                                                    # checking NW
                                                    directional_check(piece.color, r, c, lambda x: x - 1, lambda x: x - 1)
                                                    break
                                            if self.piece_repr[r - 1][c + 1] is None:
                                                if orig_row > r and orig_col < c:
                                                    # checking NE
                                                    directional_check(piece.color, r, c, lambda x: x - 1, lambda x: x + 1)
                                                    break
                                            if self.piece_repr[r + 1][c + 1] is None:
                                                if orig_row < r and orig_col < c:
                                                    # checking SE
                                                    directional_check(piece.color, r, c, lambda x: x + 1, lambda x: x + 1)
                                                    break
                                            if self.piece_repr[r + 1][c - 1] is None:
                                                if orig_col > c and orig_row < r:
                                                    # checking SW
                                                    directional_check(piece.color, r, c, lambda x: x + 1, lambda x: x - 1)
                                                    break
                                            break # stopping if protected piece found

                                        if self.piece_repr[r][c] is not None:
                                            if self.piece_repr[r][c].color == orig_color:  # checking color
                                                break  # stop movement in direction if piece of same side found
                                else:
                                    break # stopping when out of bounds

        ascended_movement()
        self.consumable_piece_found = False
        self.draw_board()
    


    def choices_cleared(self):
        self.choice_active_q = False
        self.choice_active_dir1 = False
        self.choice_active_dir2 = False
        for row in range(8): # itterating to find any movement pieces
            for col in range(8):
                piece = self.piece_repr[row][col]
                if piece is not None and piece.color in ["yellow", "navy", "orange", "purple"]:
                    self.piece_repr[row][col] = None # clearing movement pieces if found
        

    
    def win_screen(self, message_shown):
        for widget in self.board.winfo_children():
            if widget != self.board:  # making sure root window itself isnt destroyed when game finished
                widget.destroy()
        # creating win screen and win screen label
        screen = tk.Label(self.board, text=message_shown, font=("Arial", 20), bg="black", fg="white") 
        screen.pack(padx=50,pady=50)





class Piece:
    def __init__(self, color):
        # creating piece and its status
        self.color = color
        self.ascended = False
        
    def has_ascended(self):
        # ascending piece
        self.ascended = True
        # print("unit ascended") debug print statement to make sure unit has ascended
            

board = CheckersBoardGUI()