from displayio import release_displays
release_displays()

import gc
import random
import displayio
import bitmaptools
import time
import busio
import board
import dotclockframebuffer
from framebufferio import FramebufferDisplay

DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 820
NUM_BANDS = 7
GRADIENT_STEPS = 64
MIN_BRIGHTNESS = 0.15

BAND_COLORS = [
    0x0000FF,  # Blue
    0x00FFFF,  # Cyan
    0x00FF00,  # Green
    0xFFFF00,  # Yellow
    0xFF0000,  # Red
    0xFF00FF,  # Magenta
    0xFFFFFF,  # White
]
BAND_NAMES = ["Blue", "Cyan", "Green", "Yellow", "Red", "Magenta", "White"]

print("=" * 40)
print("TL032FWV01CT Rainbow Display v3")
print("=" * 40)
print(f"Display: {DISPLAY_WIDTH}x{DISPLAY_HEIGHT}")
print(f"Gradient: {GRADIENT_STEPS} steps, min brightness {MIN_BRIGHTNESS:.0%}")
print(f"Free memory: {gc.mem_free()} bytes")

init_sequence_tl032 = bytes((
    b'\x11\x80d'
    b'\xff\x05w\x01\x00\x00\x13'
    b'\xef\x01\x08'
    b'\xff\x05w\x01\x00\x00\x10'
    b'\xc0\x02\xe5\x02'
    b'\xc1\x02\x0c\n'
    b'\xc2\x02\x07\x0f'
    b'\xc3\x01\x02'
    b'\xcc\x01\x10'
    b'\xcd\x01\x08'
    b'\xb0\x10\x00\x08Q\r\xce\x06\x00\x08\x08\x1d\x02\xd0\x0fo6?'
    b'\xb1\x10\x00\x10O\x0c\x11\x05\x00\x07\x07\x1f\x05\xd3\x11n4?'
    b'\xff\x05w\x01\x00\x00\x11'
    b'\xb0\x01M'
    b'\xb1\x01\x1c'
    b'\xb2\x01\x87'
    b'\xb3\x01\x80'
    b'\xb5\x01G'
    b'\xb7\x01\x85'
    b'\xb8\x01!'
    b'\xb9\x01\x10'
    b'\xc1\x01x'
    b'\xc2\x01x'
    b'\xd0\x81\x88d'
    b'\xe0\x03\x80\x00\x02'
    b'\xe1\x0b\x04\xa0\x00\x00\x05\xa0\x00\x00\x00``'
    b'\xe2\r00``<\xa0\x00\x00=\xa0\x00\x00\x00'
    b'\xe3\x04\x00\x0033'
    b'\xe4\x02DD'
    b'\xe5\x10\x06>\xa0\xa0\x08@\xa0\xa0\nB\xa0\xa0\x0cD\xa0\xa0'
    b'\xe6\x04\x00\x0033'
    b'\xe7\x02DD'
    b'\xe8\x10\x07?\xa0\xa0\tA\xa0\xa0\x0bC\xa0\xa0\rE\xa0\xa0'
    b'\xeb\x07\x00\x01NN\xeeD\x00'
    b"\xed\x10\xff\xff\x04Vr\xff\xff\xff\xff\xff\xff'e@\xff\xff"
    b'\xef\x06\x10\r\x04\x08?\x1f'
    b'\xff\x05w\x01\x00\x00\x13'
    b'\xe8\x02\x00\x0e'
    b'\xff\x05w\x01\x00\x00\x00'
    b'\x11\x80x'
    b'\xff\x05w\x01\x00\x00\x13'
    b'\xe8\x82\x00\x0c\n'
    b'\xe8\x02\x00\x00'
    b'\xff\x05w\x01\x00\x00\x00'
    b'6\x01\x00'
    b':\x01f'
    b'\x11\x80x'
    b')\x80x'
))

print("[1/4] Sending init sequence over I2C...")
board.I2C().deinit()
i2c = busio.I2C(board.SCL, board.SDA, frequency=400_000)
tft_io_expander = dict(board.TFT_IO_EXPANDER)
#tft_io_expander['i2c_address'] = 0x38 # uncomment for rev B
dotclockframebuffer.ioexpander_send_init_sequence(i2c, init_sequence_tl032, **tft_io_expander)
i2c.deinit()
print("       OK")

print("[2/4] Creating framebuffer...")
fb = dotclockframebuffer.DotClockFramebuffer(
    **dict(board.TFT_PINS),
    frequency=16000000,
    width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT,
    hsync_pulse_width=3, hsync_back_porch=251, hsync_front_porch=150, hsync_idle_low=False,
    vsync_pulse_width=6, vsync_back_porch=90, vsync_front_porch=100, vsync_idle_low=False,
    pclk_active_high=False, pclk_idle_high=False, de_idle_high=False,
)
display = FramebufferDisplay(fb, auto_refresh=False)
print(f"       {display.width}x{display.height}, mem={gc.mem_free()} bytes")

print("[3/4] Drawing gradient rainbow...")
t_start = time.monotonic()

num_colors = NUM_BANDS * GRADIENT_STEPS
palette = displayio.Palette(num_colors)
for band in range(NUM_BANDS):
    r_base = (BAND_COLORS[band] >> 16) & 0xFF
    g_base = (BAND_COLORS[band] >> 8) & 0xFF
    b_base = BAND_COLORS[band] & 0xFF
    for step in range(GRADIENT_STEPS):
        factor = MIN_BRIGHTNESS + (1.0 - MIN_BRIGHTNESS) * step / (GRADIENT_STEPS - 1)
        r = int(r_base * factor)
        g = int(g_base * factor)
        b = int(b_base * factor)
        palette[band * GRADIENT_STEPS + step] = (r << 16) | (g << 8) | b

bitmap = displayio.Bitmap(DISPLAY_WIDTH, DISPLAY_HEIGHT, num_colors)
band_height = DISPLAY_HEIGHT // NUM_BANDS
col_width = DISPLAY_WIDTH / GRADIENT_STEPS

for band in range(NUM_BANDS):
    y0 = band * band_height
    y1 = DISPLAY_HEIGHT if band == NUM_BANDS - 1 else (band + 1) * band_height
    for step in range(GRADIENT_STEPS):
        x0 = int(step * col_width)
        x1 = DISPLAY_WIDTH if step == GRADIENT_STEPS - 1 else int((step + 1) * col_width)
        bitmaptools.fill_region(bitmap, x0, y0, x1, y1, band * GRADIENT_STEPS + step)

t_draw = time.monotonic() - t_start

tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
group = displayio.Group()
group.append(tile_grid)
display.root_group = group
display.auto_refresh = True

print(f"       Done in {t_draw:.3f}s ({NUM_BANDS * GRADIENT_STEPS} fill_region calls)")
for i, name in enumerate(BAND_NAMES):
    y0 = i * band_height
    y1 = DISPLAY_HEIGHT if i == NUM_BANDS - 1 else (i + 1) * band_height
    print(f"       {name}: rows {y0}-{y1}")

gc.collect()
print(f"       Free memory: {gc.mem_free()} bytes")

print("[4/4] Animation loop (shift every 2s)")
print("-" * 40)

frame = 0
while True:
    time.sleep(2)
    display.auto_refresh = False
    new_x = random.randint(-16, 16)
    new_y = random.randint(-16, 16)
    group.x = new_x
    group.y = new_y
    display.auto_refresh = True
    frame += 1
    if frame % 5 == 0:
        print(f"[frame {frame}] pos=({new_x},{new_y}) mem={gc.mem_free()}")
