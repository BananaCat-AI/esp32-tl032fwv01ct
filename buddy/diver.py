import displayio
import time

DIVER_COLORS = {
    ".": None,         # transparent
    "W": 0x1B2838,     # wetsuit
    "S": 0xE8B88A,     # skin
    "M": 0xFFDD00,     # mask / goggles
    "T": 0x607080,     # air tank
    "F": 0x1A5C2A,     # flippers
    "B": 0x88DDEE,     # bubbles
    "H": 0x444444,     # hose / regulator
    "G": 0x3399FF,     # goggle lens
}

DIVER_ART = [
    "..................BB....",
    "...................B....",
    "..........TTTT..........",
    ".........TTTTWWWSS......",
    "..FFFFWWWWWWWWWWSGMS....",
    "...FFFWWWWWWWWWWSMMSH...",
    "..FFFFWWWWWWWWWWWSSS....",
    ".........WWWWWWWW.......",
    "..........WWWW..........",
]

SPRITE_WIDTH = max(len(row) for row in DIVER_ART)
SPRITE_HEIGHT = len(DIVER_ART)
SCALE = 4


def create_diver():
    """Create a scaled scuba diver sprite Group with transparent background.

    Returns a Group with scale=SCALE containing the TileGrid.
    Set group.x / group.y to position (coordinates are in screen pixels).
    Effective size on screen: SPRITE_WIDTH*SCALE x SPRITE_HEIGHT*SCALE.
    """
    screen_w = SPRITE_WIDTH * SCALE
    screen_h = SPRITE_HEIGHT * SCALE
    print(f"[diver] Building sprite {SPRITE_WIDTH}x{SPRITE_HEIGHT} @ {SCALE}x = {screen_w}x{screen_h} on screen...")
    t_start = time.monotonic()

    color_keys = [k for k in DIVER_COLORS if DIVER_COLORS[k] is not None]
    palette = displayio.Palette(len(color_keys) + 1)
    palette[0] = 0x000000
    palette.make_transparent(0)

    char_to_idx = {".": 0}
    for i, key in enumerate(color_keys):
        palette[i + 1] = DIVER_COLORS[key]
        char_to_idx[key] = i + 1

    bmp = displayio.Bitmap(SPRITE_WIDTH, SPRITE_HEIGHT, len(palette))

    for y, row in enumerate(DIVER_ART):
        for x, ch in enumerate(row):
            if ch != ".":
                bmp[x, y] = char_to_idx[ch]

    elapsed = time.monotonic() - t_start
    print(f"[diver] Done in {elapsed:.3f}s")

    tg = displayio.TileGrid(bmp, pixel_shader=palette)
    group = displayio.Group(scale=SCALE)
    group.append(tg)
    return group
