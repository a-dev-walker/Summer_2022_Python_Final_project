from cmath import rect
from tkinter.tix import COLUMN
from turtle import back, color
import pygame
import os
import numpy as np

# Initialize pygame
pygame.init()


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
BLACK_COLOR = (255,255,255)
RED_COLOR = (255,0,0)
MY_FONT = pygame.font.SysFont("monospace", 100)
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
def draw_window(play_chip_group, phantom_piece):
    WIN.fill(WHITE)
    
    play_chip_group.draw(WIN)


    # for chip in playchips:
    #     print(chip.rect.x, chip.rect.y)
    #     print(chip.image)
    #     WIN.blit(chip.image,(chip.rect.x,chip.rect.y))

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
def placing_a_piece(backend_board,row,column, player_turn):
    backend_board[row][column] = player_turn + 1


# Get front end information on how far to move piece 
# NOte I swapped the order of the tuples for starting loc and ending loc because the play grid is flipped from the backend grid
def how_far_to_drop_piece(board,row,column):
    starting_loc = [ 9 + (column) * PIECE_SIZE[0], -128]
    ending_loc = [17 + row * PIECE_SIZE[1],9 + (column) * PIECE_SIZE[0]]

    return starting_loc,ending_loc


# def updating_chip_locations(playchips):
#     for chip in playchips:
#         chip.update()


def updating_phantom_chip(backend_board,phantom_chip,column,player_turn):
    if column_validity_check(backend_board,column):
        open_row = BOARD_ROW_COUNT - next_open_row(backend_board,column) -1

        starting_location , ending_location = how_far_to_drop_piece(backend_board,open_row,column)

        phantom_chip.rect.top = ending_location[0]
        phantom_chip.rect.left = ending_location[1]

        if player_turn == 0:
            phantom_chip.image = pygame.transform.scale(pygame.image.load(RED_PIECE_LOCATION),PIECE_SCALE)
        else:
            phantom_chip.image = pygame.transform.scale(pygame.image.load(BLACK_PIECE_LOCATION),PIECE_SCALE)
    else:
        phantom_chip.rect.top = -500





# Class object to make chips for the board
# Assistance for this section was obtained at: http://floppsie.comp.glam.ac.uk/Glamorgan/gaius/games/8.html
class Chip(pygame.sprite.Sprite):
    def __init__(self, image_file,starting_location,ending_location,name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(image_file),PIECE_SCALE)
        self.rect = self.image.get_rect()
        self.rect.x = starting_location[0]
        self.rect.y = starting_location[1]
        self.ending_location = ending_location
        self.name = name




    def update(self):
        # print(f" current location y: {self.rect.y}")
        # print(f" current location x: {self.rect.x}")
        # print(f" final location y: {self.ending_location[0]}")
        if self.rect.y < self.ending_location[0]:
            self.rect.y += 4





#Main Game loop 
def main():

    #main function variables
    clock = pygame.time.Clock()
    run = True
    player_turn = 0
    overall_turn_count = 0
    play_chips_group = pygame.sprite.Group()
    end_game = False
    end_game_tick_count = 0

    base_chip_name_val = "chip_from_turn_"
    

    backend_board = create_backend_board(BOARD_ROW_COUNT, BOARD_COLUMN_COUNT)

    #initializing the phantom piece
    phantom_chip = Chip(RED_PIECE_LOCATION, (-128,-128),[-128,-128],"phantom_chip")

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
                        #print("valid col")
                        next_row = next_open_row(backend_board,mouse_col)

                        placing_a_piece(backend_board,next_row,mouse_col,player_turn)

                        front_end_next_row = BOARD_ROW_COUNT - next_row - 1

                        print(next_row)
                        starting_loc, ending_loc = how_far_to_drop_piece(backend_board,front_end_next_row,mouse_col)


                        #Create the name of the next piece to be created and add to playchips
                        next_chip_name = base_chip_name_val + str(overall_turn_count)
                        print(next_chip_name)
                        #playchips.append(Chip(RED_PIECE_LOCATION,starting_loc,ending_loc,next_chip_name))
                        play_chips_group.add(Chip(RED_PIECE_LOCATION,starting_loc,ending_loc,next_chip_name))


                        # Updating player turns and overall turns
                        player_turn += 1
                        player_turn = player_turn % 2
                        overall_turn_count += 1

                        if winning_move(backend_board, 1):
                            label = MY_FONT.render("Player 1 wins!!", 1, RED_COLOR)
                            end_game = True


                else: #player 2
                    if column_validity_check(backend_board,mouse_col):
                        #print("valid col")
                        next_row = next_open_row(backend_board,mouse_col)

                        placing_a_piece(backend_board,next_row,mouse_col,player_turn)

                        front_end_next_row = BOARD_ROW_COUNT - next_row - 1

                        print(next_row)
                        starting_loc, ending_loc = how_far_to_drop_piece(backend_board,front_end_next_row,mouse_col)

                        #Create the name of the next piece to be created and add to playchips
                        next_chip_name = base_chip_name_val + str(overall_turn_count)
                        print(next_chip_name)
                        #playchips.append(Chip(RED_PIECE_LOCATION,starting_loc,ending_loc,next_chip_name))
                        play_chips_group.add(Chip(BLACK_PIECE_LOCATION,starting_loc,ending_loc,next_chip_name))

                        # Updating player turns and overall turns
                        player_turn += 1
                        player_turn = player_turn % 2
                        overall_turn_count += 1


                        if winning_move(backend_board, 2):
                            label = MY_FONT.render("Player 2 wins!!", 1, BLACK_COLOR)
                            end_game = True
                    
       

        #print(checking_mouse_column(mouse_pos))
        #updating_chip_locations(playchips)
        play_chips_group.update()
        draw_window(play_chips_group, phantom_chip)

        print(backend_board)


        if end_game:
            if end_game_tick_count > 3000:
                run = False
            else:
                WIN.blit(label,(40,10))
                end_game_tick_count += 1
        




    #end of the main game loop; will end game
    pygame.quit()



if __name__ == "__main__":
    main()
 