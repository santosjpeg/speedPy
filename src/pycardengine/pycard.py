import pygame
import settings.settings as s
import random, math

popped_card_tracker: list['Card'] = []
"""list[Card]: Tracks history of popped Cards. Used by 'undo()' calls."""

class Base:
    # size = w, h = (64*2, 89*2)
    size = w, h = (72*2-8, 97*2-16)
    half_size = hw, hh = w // 2, h // 2
    qrt_size = qw, qh = w // 4, h // 4
    eth_size = ew, eh = w // 8, h // 8
    pip_size = pw, ph = (26, 22)
    pip_center = pcx, pcy = pw // 2, ph // 2
    pip_points: dict[int, list[tuple[int, int]]] = {
        1: [(-1, -1), (hw, hh)],
        2: [(hw, hh - qh - eh // 2), (-1, -1)],
        3: [(hw, hh - qh - eh // 2), (-1, -1), (hw, hh)],
        4: [(hw - eh, hh - qh - eh // 2), (hw + eh, hh - qh - eh // 2), (-1, -1)],
        5: [(hw - eh, hh - qh - eh // 2), (hw + eh, hh - qh - eh // 2), (-1, -1), (hw, hh)],
        6: [(hw - eh, hh - qh - eh // 2), (hw + eh, hh - qh - eh // 2), (-1, -1), (hw - eh, hh), (hw + eh, hh)],
        7: [(hw - eh, hh - qh - eh // 2), (hw + eh, hh - qh - eh // 2), (-1, -1), (hw - eh, hh), (hw + eh, hh), (hw, hh - eh - eh // 4)],
        8: [(hw - eh, hh - qh - eh // 2), (hw - eh, hh - eh), (hw + eh, hh - qh - eh // 2), (hw + eh, hh - eh), (-1, -1)],
        9: [(hw - eh, hh - qh - eh // 2), (hw - eh, hh - eh), (hw + eh, hh - qh - eh // 2), (hw + eh, hh - eh), (-1, -1), (hw, hh - qh + eh // 4)],
        10: [(hw - eh, hh - qh - eh // 2), (hw - eh, hh - eh), (hw + eh, hh - qh - eh // 2), (hw + eh, hh - eh), (hw, hh - qh + eh // 4), (-1, -1)],
        11: [(hw - eh, hh - qh - eh // 2), (-1, -1)],
        12: [(hw - eh, hh - qh - eh // 2), (-1, -1)],
        13: [(hw - eh, hh - qh - eh // 2), (-1, -1)]
    }
    pip_ranks: dict[int, str] = {
        1: 'A', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K'
    }
    r: int = 14
    circle_points: list[tuple[int, int]] = [
        (r, r),
        (w - r, r),
        (w - r, h - r),
        (r, h - r)
    ]
    def __init__(self):
        """
        Automatically initialized by Table and shared by all Card objects. This should not be
        manually initialized or called other than to fetch render-related variables.
        """
        self.face_image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.back_image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.bg_pip_image = pygame.Surface((128, 128))
        self.rect = self.face_image.get_rect(center=(0, 0))
        self.pips: dict[str, pygame.Surface] = {}
        self.init_base()

    def init_base(self) -> None:
        poly_points = []
        for p_i in range(len(self.circle_points)):
            x, y = self.circle_points[p_i]
            rad = self.r
            pygame.draw.circle(self.face_image, s.colors['poker_border'], (x, y), rad)
            match p_i:
                case 0:
                    poly_points.append((x - rad, y))
                    poly_points.append((x, y))
                    poly_points.append((x, y - rad))
                case 1:
                    poly_points.append((x, y - rad))
                    poly_points.append((x, y))
                    poly_points.append((x + rad, y))
                case 2:
                    poly_points.append((x + rad, y))
                    poly_points.append((x, y))
                    poly_points.append((x, y + rad))
                case 3:
                    poly_points.append((x, y + rad))
                    poly_points.append((x, y))
                    poly_points.append((x - rad, y))
        pygame.draw.polygon(self.face_image, s.colors['poker_border'], poly_points)
        inner_base = self.face_image.copy()
        for y in range(self.h):
            for x in range(self.w):
                if inner_base.get_at((x, y)).a != 0:
                    inner_base.set_at((x, y), s.colors['poker_white'])
        inner_base = pygame.transform.scale(inner_base, (self.w - 4, self.h - 4))
        rect = inner_base.get_rect(center=self.face_image.get_rect().center)
        self.face_image.blit(inner_base, rect)

        rect = pygame.Rect((self.circle_points[0][0] - 1, self.circle_points[0][1] - 1),
                    (self.w - self.r * 2 + 2, self.h - self.r * 2 + 2))

        self.back_image.blit(self.face_image, (0,0))

        color = (235, 0, 60)

        dec_r = math.floor(color[0] / rect.height)
        # dec_g = math.floor((255 - color[1]) / rect.height)
        dec_b = math.floor((255 - color[2]) / rect.height)
        for row in range(rect.height):
            rad, g, b = color
            color = (rad-dec_r, g, b + dec_b)
            pygame.draw.line(self.back_image, color, (rect.x, rect.y + row), (rect.x + rect.width, rect.y + row))

        in_rect = pygame.Rect((self.circle_points[0][0] - 1 + 8, self.circle_points[0][1] - 1 + 8),
                                     (self.w - self.r * 2 + 2 - 8 * 2, self.h - self.r * 2 + 2 - 8 * 2))
        pygame.draw.rect(self.back_image, s.colors['poker_white'], in_rect, 8)
        rect_3 = pygame.Rect(in_rect.x + 20, in_rect.y + 20, in_rect.width - 40, in_rect.height - 40)
        pygame.draw.polygon(self.back_image, s.colors['poker_white'],
                            [(rect_3.x + rect_3.width / 2, rect_3.y),
                             (rect_3.x + rect_3.width, rect_3.y + rect_3.height / 2),
                             (rect_3.x + rect_3.width / 2, rect_3.y + rect_3.height),
                             (rect_3.x, rect_3.y + rect_3.height / 2)], 5)

        in_color = (50, 0, 225)

        dec_r = math.floor((255 - in_color[0]) / rect.height)
        # dec_g = math.floor((255 - in_color[1]) / rect.height)
        dec_b = math.floor(in_color[2] / rect.height)
        for row in range(in_rect.height):
            rad, g, b = in_color
            in_color = (rad + dec_r, g, b - dec_b)

            for x in range(in_rect.width):
                if self.back_image.get_at((x + in_rect.x, row + in_rect.y)) == s.colors['poker_white']:
                    self.back_image.set_at((x + in_rect.x, row + in_rect.y), in_color)

    def init_pips(self,
                  diamond_color: tuple[int, int, int],
                  heart_color: tuple[int, int, int],
                  club_color: tuple[int, int, int],
                  spade_color: tuple[int, int, int]) -> None:
        """
        Create each pip and save it as a Surface. Also creates a large version of each pip for the Aces.
        :param diamond_color: renders diamond Card rank and suit with this color (default 'poker_red')
        :param heart_color: renders heart Card rank and suit with this color (default 'poker_red')
        :param club_color: renders club Card rank and suit with this color (default 'poker_red')
        :param spade_color: renders spade Card rank and suit with this color (default 'poker_red')
        :return: None
        """
        pw, ph = self.pip_size
        hpw, hph = pw // 2, ph // 2
        scale_factor = 2.5

        image = pygame.Surface((pw - 4, ph + 4 - 4), pygame.SRCALPHA)
        image.fill(diamond_color)
        image = pygame.transform.rotate(image, 45)
        rect = image.get_rect()
        image = pygame.transform.scale(image, (rect.w * 0.6, rect.h))
        self.pips['diamond'] = image.copy()

        image = pygame.Surface(((pw - 4) * scale_factor, (ph + 4 - 4) * scale_factor), pygame.SRCALPHA)
        image.fill(diamond_color)
        image = pygame.transform.rotate(image, 45)
        rect = image.get_rect()
        image = pygame.transform.scale(image, (rect.w * 0.6, rect.h))
        self.pips['diamond_large'] = image.copy()

        image = pygame.Surface(self.pip_size, pygame.SRCALPHA)
        pygame.draw.circle(image, heart_color, (hpw - hpw // 2 + 2, hph - 3), 3 * 2)
        pygame.draw.circle(image, heart_color, (hpw + hpw // 2 - 1, hph - 3), 3 * 2)
        pygame.draw.polygon(image, heart_color, [(hpw, ph - 1), (0 + 3, hph-1), (pw - 3, hph-1)])
        self.pips['heart'] = image.copy()

        image = pygame.Surface((self.pip_size[0] * scale_factor, self.pip_size[1] * scale_factor), pygame.SRCALPHA)
        pygame.draw.circle(image, heart_color, ((hpw - hpw // 2 + 1) * scale_factor,
                                                          (hph - 3) * scale_factor), 3 * 2 * scale_factor)
        pygame.draw.circle(image, heart_color, ((hpw + hpw // 2 - 1) * scale_factor,
                                                          (hph - 3) * scale_factor), 3 * 2 * scale_factor)
        pygame.draw.polygon(image, heart_color, [(hpw * scale_factor, (ph - 1) * scale_factor),
                                                           ((0 + 3) * scale_factor, (hph - 1) * scale_factor),
                                                           ((pw - 3) * scale_factor, (hph - 1) * scale_factor)])
        self.pips['heart_large'] = image.copy()

        image = pygame.Surface(self.pip_size, pygame.SRCALPHA)
        pygame.draw.circle(image, club_color, (hpw - hpw // 2 - 1, hph + 2), 5)
        pygame.draw.circle(image, club_color, (hpw + hpw // 2 + 1, hph + 2), 5)
        pygame.draw.circle(image, club_color, (hpw, hph - hph // 2 - 1), 5)
        pygame.draw.polygon(image, club_color, [(hpw, hph), (pw - hpw // 2-2, ph),
                                                             (0 + hpw // 2+2, ph)])
        self.pips['club'] = image.copy()

        image = pygame.Surface((self.pip_size[0] * scale_factor, self.pip_size[1] * scale_factor), pygame.SRCALPHA)
        pygame.draw.circle(image, club_color, ((hpw - hpw // 2 - 1) * scale_factor,
                                                            (hph + 2) * scale_factor), 5 * scale_factor)
        pygame.draw.circle(image, club_color, ((hpw + hpw // 2 + 1) * scale_factor,
                                                            (hph + 2) * scale_factor), 5 * scale_factor)
        pygame.draw.circle(image, club_color, (hpw * scale_factor,
                                                            (hph - hph // 2 - 1) * scale_factor), 5 * scale_factor)
        pygame.draw.polygon(image, club_color,
                            [(hpw * scale_factor, hph * scale_factor), ((pw - hpw // 2 - 2) * scale_factor,
                                                                        ph * scale_factor),
                             ((0 + hpw // 2 + 2) * scale_factor, ph * scale_factor)])
        self.pips['club_large'] = image.copy()

        image = pygame.Surface(self.pip_size, pygame.SRCALPHA)
        pygame.draw.circle(image, spade_color, (hpw - hpw // 2 + 1, hph + 1), 5)
        pygame.draw.circle(image, spade_color, (hpw + hpw // 2, hph + 1), 5)
        pygame.draw.polygon(image, spade_color, [(hpw, 0), (0+3, hph+1), (pw-3, hph+1)])
        pygame.draw.polygon(image, spade_color, [(hpw, hph), (pw - hpw // 2-2, ph),
                                                             (0 + hpw // 2+2, ph)])
        self.pips['spade'] = image.copy()

        image = pygame.Surface((self.pip_size[0] * scale_factor, self.pip_size[1] * scale_factor), pygame.SRCALPHA)
        pygame.draw.circle(image, spade_color, ((hpw - hpw // 2 + 1) * scale_factor,
                                                            (hph + 1) * scale_factor), 5 * scale_factor)
        pygame.draw.circle(image, spade_color, ((hpw + hpw // 2 - 1) * scale_factor,
                                                            (hph + 1) * scale_factor), 5 * scale_factor)
        pygame.draw.polygon(image, spade_color, [(hpw * scale_factor, 0), ((0+3) * scale_factor,
                                                                                       (hph + 1) * scale_factor),
                                                             ((pw-3) * scale_factor, (hph + 1) * scale_factor)])
        pygame.draw.polygon(image, spade_color,
                            [(hpw * scale_factor, hph * scale_factor),
                             ((pw - hpw // 2 - 2) * scale_factor, ph * scale_factor),
                             ((0 + hpw // 2 + 2) * scale_factor, ph * scale_factor)])
        self.pips['spade_large'] = image.copy()

    def init_bg(self) -> None:
        """
        Create a background image, saved as a Surface, in green and dark green using the pip iconography.
        :return: None
        """
        rect = self.bg_pip_image.get_rect()
        dia_bg = pygame.Surface((rect.w // 2, rect.h // 2))
        dia_bg.fill(s.colors['poker_dark_green'])
        bg_rect = dia_bg.get_rect()
        p_image = self.pips['diamond'].copy()
        p_rect = p_image.get_rect(center=bg_rect.center)
        for y in range(p_rect.h):
            for x in range(p_rect.w):
                if p_image.get_at((x, y)).a != 0:
                    p_image.set_at((x, y), s.colors['poker_green'])
        dia_bg.blit(p_image, p_rect)
        self.bg_pip_image.blit(dia_bg, (0, 0))

        hrt_bg = pygame.Surface((rect.w // 2, rect.h // 2))
        hrt_bg.fill(s.colors['poker_dark_green'])
        bg_rect = hrt_bg.get_rect()
        p_image = self.pips['heart'].copy()
        p_rect = p_image.get_rect(center=bg_rect.center)
        for y in range(p_rect.h):
            for x in range(p_rect.w):
                if p_image.get_at((x, y)).a != 0:
                    p_image.set_at((x, y), s.colors['poker_green'])
        hrt_bg.blit(p_image, p_rect)
        self.bg_pip_image.blit(hrt_bg, (rect.w // 2, rect.h // 2))

        clb_bg = pygame.Surface((rect.w // 2, rect.h // 2))
        clb_bg.fill(s.colors['poker_green'])
        bg_rect = clb_bg.get_rect()
        p_image = self.pips['club'].copy()
        p_rect = p_image.get_rect(center=bg_rect.center)
        for y in range(p_rect.h):
            for x in range(p_rect.w):
                if p_image.get_at((x, y)).a != 0:
                    p_image.set_at((x, y), s.colors['poker_dark_green'])
        clb_bg.blit(p_image, p_rect)
        self.bg_pip_image.blit(clb_bg, (rect.w // 2, 0))

        spd_bg = pygame.Surface((rect.w // 2, rect.h // 2))
        spd_bg.fill(s.colors['poker_green'])
        bg_rect = spd_bg.get_rect()
        p_image = self.pips['spade'].copy()
        p_rect = p_image.get_rect(center=bg_rect.center)
        for y in range(p_rect.h):
            for x in range(p_rect.w):
                if p_image.get_at((x, y)).a != 0:
                    p_image.set_at((x, y), s.colors['poker_dark_green'])
        spd_bg.blit(p_image, p_rect)
        self.bg_pip_image.blit(spd_bg, (0, rect.h // 2))

class Card:
    def __init__(self, rank: int, suit: str, color: tuple[int, int, int], base: Base, move_speed: int = 10):
        """
        Standard poker card with a Rank (1-13), Suit, and Color. All Card objects
        share the same Base.
        :param rank: ranges 1-13
        :param suit: 'diamond', 'heart', 'club', 'spade'
        :param color: renders rank and suit in this color
        :param base: shared Base by all Cards
        :param move_speed: how fast the card moves across the table (default 10)
        """
        self.rank = rank
        self.suit = suit
        self.color = color
        self.base = base
        self.move_speed = move_speed

        self.popped_from: Deck | None = None
        self.in_deck: Deck | None = None

        self.face_image = self.base.face_image.copy()
        self.back_image = self.base.back_image.copy()

        self.pos: pygame.math.Vector2 = pygame.math.Vector2()
        self.offset_pos: pygame.math.Vector2 = pygame.math.Vector2()
        self.target_pos: pygame.math.Vector2 = pygame.math.Vector2()

        self.rect: pygame.Rect = self.face_image.get_rect(center=self.pos)
        self.font: pygame.font.SysFont = pygame.font.SysFont(s.sys_font_name, s.font_size, bold=True)

        # squash the 10 due to it being two digits and often takes up the most pixels in any given font
        if rank == 10:
            self.font_image = pygame.Surface((28, 28), pygame.SRCALPHA)
            image_1 = self.font.render('1', False, color)
            rect_1 = image_1.get_rect()
            image_1 = pygame.transform.scale(image_1, (rect_1.w * 0.9, rect_1.h))
            image_0 = self.font.render('0', False, color)
            rect_0 = image_0.get_rect()
            image_0 = pygame.transform.scale(image_0, (rect_0.w * 0.9, rect_0.h))
            self.font_image.blit(image_1, (10,0))
            self.font_image.blit(image_0, (10, 0))
        else:
            self.font_image = self.font.render(self.base.pip_ranks[rank], False, color)

        self.face_image.blit(self.font_image, (self.base.circle_points[0][0] - 6, self.base.circle_points[0][1] - 6))
        rect = self.font_image.get_rect()
        pip_image = self.base.pips[suit]
        pip_rect = self.base.pips[suit].get_rect()
        pip_image = pygame.transform.scale(pip_image, (pip_rect.w * 0.85, pip_rect.h * 0.85))
        pip_rect = self.base.pips[suit].get_rect(center=rect.center)
        self.face_image.blit(pip_image, (pip_rect.centerx, pip_rect.centery + 22))

        for pipx, pipy in self.base.pip_points[rank]:
            if pipx < 0:
                card_mirror = pygame.transform.flip(self.face_image, True, True)
                self.face_image.blit(card_mirror, (0, self.base.h // 2),
                                     pygame.Rect((0, self.base.h // 2), (self.base.w, self.base.h // 2)))
                continue
            pip_image = self.base.pips[suit]
            p_rect = pip_image.get_rect(center=(pipx, pipy))
            if rank == 1:
                pip_image = self.base.pips[f'{suit}_large']
                p_rect = pip_image.get_rect(center=(pipx, pipy))
            self.face_image.blit(pip_image, p_rect)

    def update(self, dt: float) -> None:
        """
        Updates position and rect.center each frame. Will move toward target_pos if not already there.
        :param dt: delta time
        :return: None
        """
        if round(self.pos) != round(self.target_pos):
            dir_to = (self.target_pos - self.pos)
            self.pos += dir_to * self.move_speed * dt
        self.rect.center = math.floor(self.pos.x), math.floor(self.pos.y)

class Deck:
    def __init__(self, name: str, xy: tuple[int, int], stack_offset: tuple[int, int], base: Base, face_up: bool = False):
        """
        Contains and manages a list of Card objects.
        :param name: name of the deck
        :param xy: center (x, y) of the deck (where the bottom-most card will render)
        :param stack_offset: offset (x_off, y_off) between every Card in the deck (used for card stacks and fans)
        :param base: shared Base by all Cards
        :param face_up: renders card face if True, card back if False
        """
        self.name = name
        self.anchor_xy = xy
        self.xy = xy
        self.deck: list[Card] = []
        self.stack_offset = stack_offset
        self.base = base
        self.face_up = face_up

    def __getitem__(self, index) -> Card:
        """Get Card at index."""
        return self.deck[index]

    def __setitem__(self, index, item) -> None:
        """Set index with a Card."""
        self.deck[index] = item

    def __len__(self) -> int:
        """Length of list[Card]."""
        return len(self.deck)

    def get_top_card(self) -> Card:
        """
        Get the Card sitting on top of the deck.
        :return: last Card in list
        """
        return self.deck[len(self.deck) - 1]

    def get_bottom_card(self) -> Card:
        """
        Get the Card sitting at the bottom of the deck.
        :return: first Card in list
        """
        return self.deck[0]

    def append_top(self, c: Card) -> None:
        """
        Place Card on top of the deck.
        :param c: Card to place
        :return: None
        """
        c.in_deck = self
        self.deck.append(c)

    def append_bottom(self, c: Card) -> None:
        """
        Place Card at the bottom of the deck.
        :param c: Card to place
        :return: None
        """
        c.in_deck = self
        self.deck.insert(0, c)

    def pop(self) -> Card:
        """
        Pop Card off the top of the deck and reset the Card's offset_pos.
        :return: popped Card
        """
        c = self.deck.pop()
        c.popped_from = self
        c.offset_pos.x = 0
        c.offset_pos.y = 0
        popped_card_tracker.append(c)
        return c

    def remove(self, c: Card) -> None:
        """
        Remove a specific Card from the deck and reset the Card's offset_pos.
        :param c: Card to remove
        :return: None
        """
        c.offset_pos.x = 0
        c.offset_pos.y = 0
        self.deck.remove(c)

    def draw(self, display_surface: pygame.Surface) -> None:
        """
        Render all Cards in deck using the stack_offset to display_surface.
        :param display_surface: Surface to blit onto
        :return: None
        """
        x, y = self.xy
        off_x, off_y = self.stack_offset
        for c in self.deck:
            c.target_pos = pygame.math.Vector2(x, y) + c.offset_pos
            if self.face_up:
                display_surface.blit(c.face_image, c.rect)
            else:
                display_surface.blit(c.back_image, c.rect)
            x += off_x
            y += off_y

    def create(self, diamond_range: tuple[int, int],
               heart_range: tuple[int, int],
               club_range: tuple[int, int],
               spade_range: tuple[int, int],
               diamond_color: tuple[int, int, int],
               heart_color: tuple[int, int, int],
               club_color: tuple[int, int, int],
               spade_color: tuple[int, int, int]) -> None:
        """
        Fill the deck with initialized Card objects (unshuffled). Each range is INCLUSIVE, which means
        passing (1, 13) as a parameter will create Cards of rank 1-13 (Ace-King) and add them to the deck.
        :param diamond_range: (low, high) int range INCLUSIVE
        :param heart_range: (low, high) int range INCLUSIVE
        :param club_range: (low, high) int range INCLUSIVE
        :param spade_range: (low, high) int range INCLUSIVE
        :param diamond_color: renders diamond Card rank and suit with this color (default 'poker_red')
        :param heart_color: renders heart Card rank and suit with this color (default 'poker_red')
        :param club_color: renders club Card rank and suit with this color (default 'poker_black')
        :param spade_color: renders spade Card rank and suit with this color (default 'poker_black')
        :return:
        """
        low, high = diamond_range
        for rank_val in range(low, high + 1):
            self.deck.append(Card(rank_val, 'diamond', diamond_color, self.base))
        low, high = heart_range
        for rank_val in range(low, high + 1):
            self.deck.append(Card(rank_val, 'heart', heart_color, self.base))
        low, high = club_range
        for rank_val in range(low, high + 1):
            self.deck.append(Card(rank_val, 'club', club_color, self.base))
        low, high = spade_range
        for rank_val in range(low, high + 1):
            self.deck.append(Card(rank_val, 'spade', spade_color, self.base))

    def shuffle(self) -> None:
        """
        Shuffle the deck using random.shuffle.
        :return: None
        """
        random.shuffle(self.deck)

    def update(self, dt: float) -> None:
        """
        Calls update() on each Card in the deck.
        :param dt: delta time
        :return: None
        """
        for c in self.deck:
            c.update(dt)

    def click_card(self, xy: tuple[int, int]) -> Card | None:
        """
        Returns the Card object based on a collidepoint(x, y) call. The deck is searched
        in reverse order to prioritize the most exposed cards first.
        :param xy: (x, y) position for collidepoint(x, y) call
        :return: Card if any found, None if not
        """
        x, y = xy
        for c in reversed(self.deck):
            if c.rect.collidepoint(x, y):
                return c
        return None

class Table:
    def __init__(self):
        """
        Contains and manages a dictionary of Deck objects in the form of dict[str, Deck] (empty on initialization).
        Also initializes Base, which is shared by all Card objects in all Decks.
        """
        self.decks: dict[str, Deck] = {}
        self.base: Base = Base()
        self.first_deck: bool = True

    def __getitem__(self, name: str) -> Deck:
        """Get Deck by name."""
        return self.decks[name]

    def create_cards_in_deck(self, name: str,
                             diamond_range: tuple[int, int],
                             heart_range: tuple[int, int],
                             club_range: tuple[int, int],
                             spade_range: tuple[int, int],
                             diamond_color: tuple[int, int, int] = s.colors['poker_red'],
                             heart_color: tuple[int, int, int] = s.colors['poker_red'],
                             club_color: tuple[int, int, int] = s.colors['poker_black'],
                             spade_color: tuple[int, int, int] = s.colors['poker_black']) -> None:
        """
        Fill a Deck, by name, with initialized Card objects (unshuffled). Each range is INCLUSIVE, which means
        passing (1, 13) as a parameter will create Cards of rank 1-13 (Ace-King) and add them to the deck. If this
        is the first Deck being created, initialize Base with passed colors.
        :param name: name of the deck to fill with new cards
        :param diamond_range: (low, high) int range INCLUSIVE
        :param heart_range: (low, high) int range INCLUSIVE
        :param club_range: (low, high) int range INCLUSIVE
        :param spade_range: (low, high) int range INCLUSIVE
        :param diamond_color: renders diamond Card rank and suit with this color (default 'poker_red')
        :param heart_color: renders heart Card rank and suit with this color (default 'poker_red')
        :param club_color: renders club Card rank and suit with this color (default 'poker_black')
        :param spade_color: renders spade Card rank and suit with this color (default 'poker_black')
        :return:
        """
        if self.first_deck:
            self.first_deck = False
            self.base.init_pips(diamond_color, heart_color, club_color, spade_color)
            self.base.init_bg()
        self[name].create(diamond_range, heart_range, club_range, spade_range,
                          diamond_color, heart_color, club_color, spade_color)

    def add_deck(self, name: str, xy: tuple[int, int], stack_offset: tuple[int, int], face_up: bool = False) -> None:
        """
        Add a Deck to the Table (will initialize a Deck object and add it to the deck dictionary).
        :param name: name of the deck
        :param xy: center (x, y) of the deck (where the bottom-most card will render)
        :param stack_offset: offset (x_off, y_off) between every Card in the deck (used for card stacks and fans)
        :param face_up: renders card face if True, card back if False
        :return: None
        """
        self.decks[name] = Deck(name, xy, stack_offset, self.base, face_up)

    def shuffle_deck(self, name: str) -> None:
        """
        Calls shuffle() on a Deck by name (shuffle() uses random.shuffle).
        :return: None
        """
        self.decks[name].shuffle()

    def remove_deck(self, name: str) -> None:
        """
        Calls 'del' on a Deck by name to remove it from the deck dictionary.
        :param name:
        :return: None
        """
        del self.decks[name]

    def deal_to_bottom(self, from_deck: str, to_deck: str) -> None:
        """
        Pops Card off from_deck and appends it to the bottom of to_deck.
        :param from_deck: name of Deck to pop from
        :param to_deck: name of Deck to append to the bottom of
        :return: None
        """
        self.decks[to_deck].append_bottom(self.decks[from_deck].pop())

    def deal_to_top(self, from_deck: str, to_deck: str) -> None:
        """
        Pops Card off from_deck and appends it to the top of to_deck.
        :param from_deck: name of Deck to pop from
        :param to_deck: name of Deck to append to the top of
        :return: None
        """
        self.decks[to_deck].append_top(self.decks[from_deck].pop())

    def draw(self, display_surface: pygame.Surface) -> None:
        """
        Calls draw() on all Decks in the deck dictionary.
        :param display_surface:
        :return: None
        """
        for d in self.decks.values():
            d.draw(display_surface)

    def update(self, dt: float) -> None:
        """
        Calls update() on all Decks in the deck dictionary.
        :param dt: delta time
        :return: None
        """
        for d in self.decks.values():
            d.update(dt)

    def click_deck(self, xy: tuple[int, int]) -> tuple[str, Deck, Card] | None:
        """
        Returns the name of the Deck, the Deck object, and the Card object at (x, y) position using
        collidepoint(x, y). Each deck is searched in reverse order to prioritize the most exposed cards first.
        :param xy: (x, y) position for collidepoint(x, y) calls
        :return: (deck_name: str, deck_object: Deck, card_object: Card) if found, None if not
        """
        for name, d in self.decks.items():
            c = d.click_card(xy)
            if c:
                return name, d, c
        return None
