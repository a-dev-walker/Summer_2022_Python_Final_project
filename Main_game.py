from turtle import color
import pygame
import os

#Static variables
WIDTH, HEIGHT = 900,900
WHITE = 255,255,255
FPS = 60
RED_PIECE_LOCATION = os.path.join("Assets","red_piece_png_transparent.png")
BLACK_PIECE_LOCATION = os.path.join("Assets","black_piece_png_transparent.png")
PIECE_SCALE = 120,120
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
def draw_window(pieces):
    WIN.fill(WHITE)
    WIN.blit(BLACK_PIECE,(135+128,145+128))

    blit_alpha(WIN,RED_PIECE,(9+128,17+128),56)
    

    blit_alpha(WIN,pieces[0].image,(pieces[0].rect.x,pieces[0].rect.y),128)

    WIN.blit(BOARD, (0,0))
    pygame.display.update()


def checking_mouse_column(mouse_position):
    mouse_x_loc = mouse_position[0]

    for column in range(1,7):
        if mouse_x_loc < 128*column:
            return column

    return 0
    






#Class object to make chips for the board
class Chip(pygame.sprite.Sprite):
    def __init__(self, image_file,location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(image_file),PIECE_SCALE)
        self.rect = self.image.get_rect(topleft=(location[0],location[1]))





#Main Game loop 
def main():

    #main function variables
    clock = pygame.time.Clock()
    run = True
    player_turn = 0
    playchips = []

    new_red = Chip(RED_PIECE_LOCATION,(9,300))
    playchips.append(new_red)

    #Checking what event state the game is currently in
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        mouse_pos = pygame.mouse.get_pos()

        #new_red = Chip(RED_PIECE_LOCATION,(9,17))
        #new_red.rect.x
        new_red.rect.y += 1
        #playchips.append(new_red)


        draw_window(playchips)






    #end of the main game loop; will end game
    pygame.quit()



if __name__ == "__main__":
    main()
 