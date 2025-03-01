import pygame 
import thorpy as tp 

pygame.init()

screen = pygame.display.set_mode((1920,1080))
tp.init(screen, tp.theme_human)

my_button = tp.Button("Hello World.\nThis button uses the default theme")
my_button.center_on(screen)

def before_gui():
    screen.fill((250,)*3)

tp.call_before_gui(before_gui)

player = my_button.get_updater().launch()
pygame.quit()