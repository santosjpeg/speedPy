screen_size = screen_w, screen_h = (320*3, 180*3)
half_screen_size = half_screen_w, half_screen_h = screen_w // 2, screen_h // 2
window_size = window_w, window_h = (1920, 1080)
half_window_size = half_window_w, half_window_h = window_w // 2, window_h // 2
window_scale = window_scale_x, window_scale_y = window_w / screen_w, window_h / screen_h

font_size: int = 28
sys_font_name: str = 'ubuntumono'

colors: dict[str, tuple[int,int,int]] = {
    'poker_green': (53, 101, 77),
    'poker_dark_green': (43, 91, 87),
    'poker_red': (199, 44, 72),
    'poker_black': (28, 28, 30),
    'poker_white': (242, 242, 242),
    'poker_border': (211, 211, 211)
}
