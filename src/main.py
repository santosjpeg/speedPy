import pygame, sys
from pygame.locals import *

from imports import *
from rendering.renderer import Renderer 
import pycardengine.pycard as pycard

class Speed:
    def __init__(self):
        #GAME SETUP
        #   1. INIT TABLE
        #   2. ADD 'test' DECK
        #   3. CREATE CARDS IN TEST DECK ()
        table = pycard.Table()
        table.add_deck('test',
                       (500,500),
                       (0,0),
                       False)
        
        table.create_cards_in_deck('test', (1,13),(1,13),(1,13),(1,13))

        
        
        table['test'].shuffle()
        self.table = table
    
    def draw(self, display_surface : pygame.Surface, off : float = 0) -> None:
        self.table.draw(display_surface)

    def update(self, dt: float) -> None:
        self.table.update(dt)
    
            


""" Deactivates PyGame and triggers exit() system call """
def handle_quit() -> None:
    pygame.quit()
    sys.exit()
    
def main() -> None:
    pygame.init()
    speed = Speed()

    resolution = (WINDOW_WIDTH, WINDOW_HEIGHT)
    display_surface = pygame.display.set_mode(resolution)
    pygame.display.set_caption('Speed: Card Game (52CardEngine)')
    FPS_CLOCK = pygame.time.Clock()

    font = pygame.font.Font('freesansbold.ttf', 32)
    
    delta : float 
    t : float = 0
    offset : float = 0

    #MAIN/GAME LOOP
    while True:
        delta = FPS_CLOCK.tick(FPS) / 1000
        delta = max(0.001, min(0.1,delta))
        t += delta

        display_surface.fill(POKER_GREEN)
        
        #EVENT HANDLER
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    handle_quit()
                    
                
        speed.draw(display_surface, offset)
        speed.update(delta)

        #UPDATE
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


if __name__ == '__main__':
    main()