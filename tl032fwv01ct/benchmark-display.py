from displayio import release_displays
release_displays()

import gc
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
print("TL032FWV01CT Display Benchmark")
print("=" * 40)
print(f"Display: {DISPLAY_WIDTH}x{DISPLAY_HEIGHT}")
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

print("[1/5] Init I2C...")
board.I2C().deinit()
i2c = busio.I2C(board.SCL, board.SDA, frequency=400_000)
tft_io_expander = dict(board.TFT_IO_EXPANDER)
#tft_io_expander['i2c_address'] = 0x38 # uncomment for rev B
dotclockframebuffer.ioexpander_send_init_sequence(i2c, init_sequence_tl032, **tft_io_expander)
i2c.deinit()
print("       OK")

print("[2/5] Creating framebuffer...")
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

band_height = DISPLAY_HEIGHT // NUM_BANDS
group = displayio.Group()
display.root_group = group

# ==========================================================
# BENCHMARK A: Solid bands — Palette(7) + 7 fill_region
# ==========================================================
print()
print("[3/5] BENCHMARK A: Solid color bands")
print(f"       Palette(7) + 7 fill_region calls")

palette_a = displayio.Palette(NUM_BANDS)
for i, c in enumerate(BAND_COLORS):
    palette_a[i] = c

bitmap_a = displayio.Bitmap(DISPLAY_WIDTH, DISPLAY_HEIGHT, NUM_BANDS)

gc.collect()
mem_before_a = gc.mem_free()
t_start = time.monotonic()

for band in range(NUM_BANDS):
    y0 = band * band_height
    y1 = DISPLAY_HEIGHT if band == NUM_BANDS - 1 else (band + 1) * band_height
    bitmaptools.fill_region(bitmap_a, 0, y0, DISPLAY_WIDTH, y1, band)

t_a = time.monotonic() - t_start
gc.collect()
mem_after_a = gc.mem_free()

tg_a = displayio.TileGrid(bitmap_a, pixel_shader=palette_a)
group.append(tg_a)
display.auto_refresh = True

print(f"  -->  {t_a:.4f}s")
print(f"       Memory used: {mem_before_a - mem_after_a} bytes")
print(f"       Showing for 3s...")
time.sleep(3)
display.auto_refresh = False
group.pop()

# ==========================================================
# BENCHMARK B: Gradient bands — Palette(448) + 448 fill_region
# ==========================================================
print()
print("[4/5] BENCHMARK B: Gradient bands")
print(f"       Palette({NUM_BANDS * GRADIENT_STEPS}) + {NUM_BANDS * GRADIENT_STEPS} fill_region calls")

num_grad_colors = NUM_BANDS * GRADIENT_STEPS
palette_b = displayio.Palette(num_grad_colors)
for band in range(NUM_BANDS):
    r_base = (BAND_COLORS[band] >> 16) & 0xFF
    g_base = (BAND_COLORS[band] >> 8) & 0xFF
    b_base = BAND_COLORS[band] & 0xFF
    for step in range(GRADIENT_STEPS):
        factor = (step + 1) / GRADIENT_STEPS
        r = int(r_base * factor)
        g = int(g_base * factor)
        b = int(b_base * factor)
        palette_b[band * GRADIENT_STEPS + step] = (r << 16) | (g << 8) | b

bitmap_b = displayio.Bitmap(DISPLAY_WIDTH, DISPLAY_HEIGHT, num_grad_colors)
col_width = DISPLAY_WIDTH / GRADIENT_STEPS

gc.collect()
mem_before_b = gc.mem_free()
t_start = time.monotonic()

for band in range(NUM_BANDS):
    y0 = band * band_height
    y1 = DISPLAY_HEIGHT if band == NUM_BANDS - 1 else (band + 1) * band_height
    for step in range(GRADIENT_STEPS):
        x0 = int(step * col_width)
        x1 = DISPLAY_WIDTH if step == GRADIENT_STEPS - 1 else int((step + 1) * col_width)
        bitmaptools.fill_region(bitmap_b, x0, y0, x1, y1, band * GRADIENT_STEPS + step)

t_b = time.monotonic() - t_start
gc.collect()
mem_after_b = gc.mem_free()

tg_b = displayio.TileGrid(bitmap_b, pixel_shader=palette_b)
group.append(tg_b)
display.auto_refresh = True

print(f"  -->  {t_b:.4f}s")
print(f"       Memory used: {mem_before_b - mem_after_b} bytes")
print(f"       Showing for 3s...")
time.sleep(3)
display.auto_refresh = False
group.pop()

# ==========================================================
# BENCHMARK C: Pixel-by-pixel — 262,400 Python writes
# ==========================================================
print()
print("[5/5] BENCHMARK C: Pixel-by-pixel (original)")
print(f"       {DISPLAY_WIDTH * DISPLAY_HEIGHT:,} individual bitmap[x,y] writes")

bitmap_c = displayio.Bitmap(DISPLAY_WIDTH, DISPLAY_HEIGHT, 65535)

gc.collect()
mem_before_c = gc.mem_free()
t_start = time.monotonic()

for x in range(DISPLAY_WIDTH):
    intensity = x * 255 // (DISPLAY_WIDTH - 1)
    b = intensity >> 3
    g = (intensity >> 2) << 5
    r = (intensity >> 3) << 11
    for band in range(NUM_BANDS):
        y0 = band * band_height
        y1 = DISPLAY_HEIGHT if band == NUM_BANDS - 1 else (band + 1) * band_height
        if band == 0:
            color = b
        elif band == 1:
            color = b | g
        elif band == 2:
            color = g
        elif band == 3:
            color = g | r
        elif band == 4:
            color = r
        elif band == 5:
            color = r | b
        else:
            color = r | g | b
        for y in range(y0, y1):
            bitmap_c[x, y] = color

t_c = time.monotonic() - t_start
gc.collect()
mem_after_c = gc.mem_free()

tg_c = displayio.TileGrid(
    bitmap_c,
    pixel_shader=displayio.ColorConverter(input_colorspace=displayio.Colorspace.RGB565),
)
group.append(tg_c)
display.auto_refresh = True

print(f"  -->  {t_c:.1f}s")
print(f"       Memory used: {mem_before_c - mem_after_c} bytes")

# ==========================================================
# Results
# ==========================================================
print()
print("=" * 40)
print("RESULTS")
print("=" * 40)
print(f"  A) Solid fill_region:    {t_a:.4f}s  ({NUM_BANDS} calls)")
print(f"  B) Gradient fill_region: {t_b:.4f}s  ({NUM_BANDS * GRADIENT_STEPS} calls)")
print(f"  C) Pixel-by-pixel:       {t_c:.1f}s  ({DISPLAY_WIDTH * DISPLAY_HEIGHT:,} writes)")
if t_a > 0:
    print(f"  Speedup A vs C: {t_c / t_a:.0f}x")
if t_b > 0:
    print(f"  Speedup B vs C: {t_c / t_b:.0f}x")
print("=" * 40)
gc.collect()
print(f"Free memory: {gc.mem_free()} bytes")
print()
print("Benchmark complete. Display shows pixel-by-pixel result.")
print("Reset board to run again.")

while True:
    time.sleep(60)
