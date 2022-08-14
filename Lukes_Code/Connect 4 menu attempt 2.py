import pygame
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((600,400))

def options():
    pass

def start_the_game():
    
    pass

menu = pygame_menu.Menu('Welcome to Connect 4', 500, 400, theme=pygame_menu.themes.THEME_SOLARIZED)

menu.add.text_input ("Player 1:", default = 'Player 1')
menu.add.text_input ("Player 2:", default = 'Player 2')
menu.add.button('Play', start_the_game)
menu.add.button('Options', options)
menu.add.button('Quit', pygame_menu.events.EXIT)


menu.mainloop(surface)