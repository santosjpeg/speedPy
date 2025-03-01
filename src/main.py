import pygame, sys
import thorpy as tp
from pygame.locals import *

from imports import *
import pycardengine.pycard as pycard

class States:
    #Stores super class attributes of current state (running, done, quit) and which state is before or after current
    def __init__(self):
        self.done = False 
        self.next = None
        self.quit = False 
        self.previous = None
    
class Menu(States):
    # Menu always comes before Game
    def __init__(self):
        States.__init__(self)
        self.next = 'game'
    
    def cleanup(self):
        #TODO
        pass

    def startup(self):
        #TODO
        pass

    #Move to next state if mouse button click
    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.done = True
    
    #Constantly draw a blank poker table until user mouse click
    def update(self, screen, dt):
        self.draw(screen)
    
    def draw(self, screen):
        screen.fill(POKER_GREEN)

class Control:
    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False 
        #Initialize window and FPS clock
        self.screen = pygame.display.set_mode(self.size)
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Speed: Card Game (52CardEngine)')
        self.state_dict = {
            'menu': Menu(),
            'game': Speed(),
        }

    #Take in dicitonary of states, store name of start state
    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state

        #using class __dict__ to access object as member of dictionary
        self.state = self.state_dict[self.state_name]
    
    def flip_state(self):
        #
        self.state.done = False 
        previous, self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        self.state.previous = previous
    
    def update(self, dt):
        if self.state.quit:
            self.done = True 
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen,dt)
    
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            self.state.get_event(event)
        
    def main_game_loop(self):
        while not self.done:
            delta = self.clock.tick(FPS) / 1000
            delta = max(0.001, min(0.1,delta))
            self.event_loop() 
            self.update(delta)
            pygame.display.flip()

class Speed(States):
    def __init__(self):
        States.__init__(self)
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
        self.next = 'menu'

    def cleanup(self):
        print("debug: cleaning up game")

    def startup(self):
        print("debug: starting up game")
    
    def get_event(self, event):
        mxy = pygame.mouse.get_pos()
        #EVENT HANDLER
        if event.type == pygame.QUIT:
            handle_quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.interact(mxy)
    
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
        display_surface.fill(POKER_GREEN)
        self.table.draw(display_surface)

    def update(self, screen : pygame.Surface, dt: float) -> None:
        #Check for winner
        user_deck = self.table['user_deck']
        opponent_deck = self.table['opponent_deck']
        user_hand = self.table['user_hand']
        opponent_hand = self.table['opponent_hand']

        if len(user_deck) == 0 and len(user_hand) == 0:
            print("USER WON")
        elif len(opponent_deck) == 0 and len(opponent_hand) == 0:
            print("OPPONENT WON")

        #Deals card from deck if hand has less than 5 cards
        if len(self.table['user_deck']) > 0 and len(self.table['user_hand']) < 5:
            self.table.deal_to_top('user_deck','user_hand')
        if len(self.table['opponent_deck']) > 0 and len(self.table['opponent_hand']) < 5:
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
        
        #No legal turns => next round starts with a flipped card from both center decks
        if user_no_turns and opponent_no_turns and len(self.table['center_deck_1']) > 0 and len(self.table['center_deck_2']) > 0:
            self.table.deal_to_top('center_deck_1', 'center_flipped_1')
            self.table.deal_to_top('center_deck_2', 'center_flipped_2')
                    

        
        self.table.update(dt)
        self.draw(screen)
    
def handle_quit() -> None:
    pygame.display.quit()
    pygame.quit()
    sys.exit()
    
def main() -> None:
    pygame.init()
    resolution = (WINDOW_WIDTH, WINDOW_HEIGHT)

    settings = {
        'size': resolution,
        'fps': FPS,
        'caption': CAPTION,
    }
    state_dict = {
        'menu': Menu(),
        'game': Speed(),
    }

    app = Control(**settings)
    app.setup_states(state_dict, 'menu')
    app.main_game_loop()

if __name__ == '__main__':
    main()