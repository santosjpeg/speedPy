import pygame, sys
from pygame.locals import *

from imports import *
from rendering.renderer import Renderer 
import pycardengine.pycard as pycard

class Speed:
    def __init__(self):
        table = pycard.Table()
        #CENTER LEFT AND CENTER RIGHT DESKS FOR FLIPPING CARDS BEFORE EACH ROUND; 6 CARDS EACH
        table.add_deck('center_deck_1',
                       (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2),
                       (0,-1),
                       False)
        
        table.create_cards_in_deck('center_deck_1', (1,13),(1,13),(1,13),(1,13))
        table['center_deck_1'].shuffle()

        table.add_deck('center_deck_2',
                       (WINDOW_WIDTH // (4/3), WINDOW_HEIGHT // 2),
                       (0,-1),
                       False)
        while len(table['center_deck_2']) < 6:
            table.deal_to_top('center_deck_1', 'center_deck_2')
        table['center_deck_2'].shuffle()

        #USER AND OPPONENT DECK; 20 CARDS EACH
        table.add_deck('user_deck',
                       (WINDOW_WIDTH // 8, WINDOW_HEIGHT // (4/3)),
                       (0,-1),
                       False)
        while len(table['user_deck']) < 20:
            table.deal_to_top('center_deck_1', 'user_deck')
        table['user_deck'].shuffle()

        table.add_deck('opponent_deck',
                       (WINDOW_WIDTH // (8/7), WINDOW_HEIGHT // 4),
                       (0,-1),
                       False)
        while len(table['opponent_deck']) < 20:
            table.deal_to_top('center_deck_1','opponent_deck')
        table['opponent_deck'].shuffle()

        #INITIALIZE USER + OPPONENT HAND
        table.add_deck('user_hand',
                       (WINDOW_WIDTH // 4, WINDOW_HEIGHT // (4/3)),
                       (75,0),
                       True)
        while len(table['user_hand']) < 5:
            table.deal_to_top('user_deck', 'user_hand')
        
        table.add_deck('opponent_hand',
                       (WINDOW_WIDTH // (8/6), WINDOW_HEIGHT // 4),
                       (-75,0),
                       True)
        while len(table['opponent_hand']) < 5:
            table.deal_to_top('opponent_deck','opponent_hand')

        # Flip over a card each from both center decks to begin game
        table.add_deck('center_flipped_1',
                       (WINDOW_WIDTH_HALF - 100,WINDOW_HEIGHT // 2),
                       (1,0),
                       True)
        table.deal_to_top('center_deck_1', 'center_flipped_1')

        table.add_deck('center_flipped_2',
                       (WINDOW_WIDTH_HALF + 100,WINDOW_HEIGHT // 2),
                       (1,0),
                       True)
        table.deal_to_top('center_deck_2', 'center_flipped_2')
        self.table = table

    
    def interact(self, mouse_x_y : tuple[int , int]) -> None:
        target = self.table.click_deck(mouse_x_y)
        if target:
            name , d , c = target 
            #PRIMARY MOVE LOGIC
            if name in {'user_hand', 'opponent_hand'} and self.is_legal_turn(c, 'center_flipped_1'):
                d.remove(c)
                d.append_top(c)
                self.table.deal_to_top(name, 'center_flipped_1')
            elif name in {'user_hand', 'opponent_hand'} and self.is_legal_turn(c, 'center_flipped_2'):
                d.remove(c)
                d.append_top(c)
                self.table.deal_to_top(name, 'center_flipped_2')
            
    
    
    def is_legal_turn(self, card : pycard.Card, dest_deck : pycard.Deck) -> bool:
        top_card = self.table[dest_deck].get_top_card().rank 
        return (card.rank in {top_card + 1, top_card - 1}) or ({card.rank, top_card} == {1,13})
    
    def draw(self, display_surface : pygame.Surface, off : float = 0) -> None:
        self.table.draw(display_surface)

    def update(self, dt: float) -> None:
        #Check for winner
        user_deck = self.table['user_deck']
        opponent_deck = self.table['opponent_deck']
        user_hand = self.table['user_hand']
        opponent_hand = self.table['opponent_hand']

        if len(user_deck) == 0 and len(user_hand) == 0:
            print("USER WON")
        elif len(opponent_deck) == 0 and len(opponent_hand) == 0:
            print("OPPONENT WON")

        if len(self.table['user_deck']) > 0 and len(self.table['user_hand']) < 5:
            self.table.deal_to_top('user_deck','user_hand')
        elif len(self.table['opponent_deck']) > 0 and len(self.table['opponent_hand']) < 5:
            self.table.deal_to_top('opponent_deck', 'opponent_hand')
        #Check if there are no more legal turns on either user or opponent hand 
        user_no_turns = True
        opponent_no_turns = True

        for c in user_hand:
            if self.is_legal_turn(c, 'center_flipped_1') or self.is_legal_turn(c,'center_flipped_2'):
                user_no_turns = False
                break

        for c in opponent_hand:
            if self.is_legal_turn(c, 'center_flipped_1') or self.is_legal_turn(c,'center_flipped_2'):
                opponent_no_turns = False
                break
        
        if user_no_turns and opponent_no_turns:
            self.table.deal_to_top('center_deck_1', 'center_flipped_1')
            self.table.deal_to_top('center_deck_2', 'center_flipped_2')
                    

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
        
        mxy = mx , my = pygame.mouse.get_pos()
        #EVENT HANDLER
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    handle_quit()
                    
                case pygame.MOUSEBUTTONDOWN:
                    match event.dict['button']:
                        case 1:
                            speed.interact(mxy)
                    
                
        speed.draw(display_surface, offset)
        speed.update(delta)

        #UPDATE
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


if __name__ == '__main__':
    main()