from cmath import rect
from tkinter.tix import COLUMN
from turtle import back, color
import pygame
import os
import numpy as np

#Static variables
WIDTH, HEIGHT = 900,900
WHITE = 255,255,255
FPS = 60
LEFT = 1 #used for mouse button
RED_PIECE_LOCATION = os.path.join("Assets","red_piece_png_transparent.png")
BLACK_PIECE_LOCATION = os.path.join("Assets","black_piece_png_transparent.png")
PIECE_SCALE = 120,120
BOARD_ROW_COUNT = 6
BOARD_COLUMN_COUNT = 7
PIECE_SIZE = [128,128]
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Intro to Python Connect Four")


#Images
BOARD_IMAGE = pygame.image.load(
    os.path.join('Assets','board_png_transparent_test.png'))
BOARD = pygame.transform.scale(BOARD_IMAGE, (900,850))

RED_PIECE_IMAGE = pygame.image.load(RED_PIECE_LOCATION)
RED_PIECE = pygame.transform.scale(RED_PIECE_IMAGE, PIECE_SCALE)

BLACK_PIECE_IMAGE = pygame.image.load(BLACK_PIECE_LOCATION)
BLACK_PIECE = pygame.transform.scale(BLACK_PIECE_IMAGE, PIECE_SCALE)


def create_backend_board(rows, columns):
    backend_board = np.zeros((rows, columns))
    return backend_board


#Blit method to make transparent objects (obtained online: https://nerdparadise.com/programming/pygameblitopacity)
def blit_alpha(target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)


#Drawing the play window 
def draw_window(playchips, phantom_piece):
    WIN.fill(WHITE)
    
    
    for chip in playchips:
        WIN.blit(playchips[chip].image,playchips[chip].rect.x,playchips[chip].rect.y)

    blit_alpha(WIN,phantom_piece.image,(phantom_piece.rect.x,phantom_piece.rect.y),100)

    #blit_alpha(WIN,pieces[0].image,(pieces[0].rect.x,pieces[0].rect.y),128)
    # WIN.blit(BLACK_PIECE,(135+128,145+128))
    # blit_alpha(WIN,RED_PIECE,(9+128,17+128),56)


    WIN.blit(BOARD, (0,0))
    pygame.display.update()



# Function checking which column the mouse is currently hovering over
# Returns the count of the column, 1-7, and returns 0 if off the screen
def checking_mouse_column(mouse_position):
    mouse_x_loc = mouse_position[0]

    for column in range(1,BOARD_COLUMN_COUNT+1):
        if mouse_x_loc < 128*column:
            return column

    return BOARD_COLUMN_COUNT
    


# The math needed to check if a given player has won
# This math was taken from the following url: "https://www.askpython.com/python/examples/connect-four-game"
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(BOARD_COLUMN_COUNT-3):
        for r in range(BOARD_ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
 
    # Check vertical locations for win
    for c in range(BOARD_COLUMN_COUNT):
        for r in range(BOARD_ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
 
    # Check positively sloped diaganals
    for c in range(BOARD_COLUMN_COUNT-3):
        for r in range(BOARD_ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
 
    # Check negatively sloped diaganals
    for c in range(BOARD_COLUMN_COUNT-3):
        for r in range(3, BOARD_ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True



# Check if a given column is full or not
def column_validity_check(backend_board,column):
    if backend_board[BOARD_ROW_COUNT-1][column] == 0:
        return True
    else:
        return False

# Returns which row is the next that's open in the given column
def next_open_row(backend_board,column):
    for row in range(BOARD_ROW_COUNT):
        if backend_board[row][column] == 0:
            return row

# Filling in backend board with pieces
def placing_a_piece(backend_board,row,column, player_piece):
    backend_board[row][column] == player_piece


# Get front end information on how far to move piece 
# NOte I swapped the order of the tuples for starting loc and ending loc because the play grid is flipped from the backend grid
def how_far_to_drop_piece(board,row,column):
    starting_loc = [ -128, 9 + (column-1) * PIECE_SIZE[0]]
    ending_loc = [17 + row * PIECE_SIZE[1],9 + (column-1) * PIECE_SIZE[0]]

    return starting_loc,ending_loc


def updating_chip_locations(playchips):
    for chip in playchips:
        chip.update()


def updating_phantom_chip(backend_board,phantom_chip,column,player_turn):
    if column_validity_check(backend_board,column):
        open_row = BOARD_ROW_COUNT - next_open_row(backend_board,column) -1

        starting_location , ending_location = how_far_to_drop_piece(backend_board,open_row,column+1)

        phantom_chip.rect.top = ending_location[0]
        phantom_chip.rect.left = ending_location[1]

        if player_turn == 0:
            phantom_chip.image = pygame.transform.scale(pygame.image.load(RED_PIECE_LOCATION),PIECE_SCALE)
        else:
            phantom_chip.image = pygame.transform.scale(pygame.image.load(BLACK_PIECE_LOCATION),PIECE_SCALE)


def updating_turn_counts(player_turn,overall_turn_count):
    player_turn += 1
    player_turn = player_turn % 2
    overall_turn_count += 1



# Class object to make chips for the board
# Assistance for this section was obtained at: http://floppsie.comp.glam.ac.uk/Glamorgan/gaius/games/8.html
class Chip(pygame.sprite.Sprite):
    def __init__(self, image_file,initial_location,final_location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(image_file),PIECE_SCALE)
        self.rect = self.image.get_rect(topleft=(initial_location[0],initial_location[1]))
        self.final_location = final_location

    def update(self):
        if self.rect.top < self.final_location[1]:
            self.rect.top += 1





#Main Game loop 
def main():

    #main function variables
    clock = pygame.time.Clock()
    run = True
    player_turn = 1
    overall_turn_count = 0
    playchips = []

    base_chip_name_val = "chip_from_turn_"

    base_chip_name_template = "{} = \"{}\""
    

    backend_board = create_backend_board(BOARD_ROW_COUNT, BOARD_COLUMN_COUNT)

    phantom_chip = Chip(RED_PIECE_LOCATION, (-128,-128),[-128,-128])

    # new_red = Chip(RED_PIECE_LOCATION,(9,-128),[9,400])
    # playchips.append(new_red)

    #Checking what event state the game is currently in
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            mouse_col = checking_mouse_column(mouse_pos) - 1

            updating_phantom_chip(backend_board,phantom_chip,mouse_col,player_turn)
            if event.type == pygame.QUIT:
                run = False
            #Handling if a player is pressing the eft mouse button down
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                if player_turn == 0:
                    
                    if column_validity_check(backend_board,mouse_col):
                        next_row = next_open_row(backend_board,mouse_col)
                        starting_loc, ending_loc = how_far_to_drop_piece(backend_board,next_row,mouse_col)

                        placing_a_piece({backend_board},{next_row},{player_turn})


                        #Create the name of the next piece to be created
                        next_chip_name = base_chip_name_val + str(overall_turn_count)

                        #Create the string of the function for creating said new chip
                        next_chip_function_string = f"Chip(RED_PIECE_LOCATION,{starting_loc},{ending_loc}"
                        #Format an exec statement to make the next chip 
                        new_chip_statement = base_chip_name_template.format(next_chip_name,next_chip_function_string)
                        exec(new_chip_statement)

                        #Add the next chip to the playchips array
                        playchips.append(next_chip_name)

                        updating_turn_counts(player_turn,overall_turn_count)

                    

                    








        
       

        #print(checking_mouse_column(mouse_pos))
        updating_chip_locations(playchips)
        draw_window(playchips, phantom_chip)



        # Update player turn - need to do when swapping characters
        






    #end of the main game loop; will end game
    pygame.quit()



if __name__ == "__main__":
    main()
 