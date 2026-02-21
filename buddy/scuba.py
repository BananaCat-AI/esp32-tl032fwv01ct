from displayio import release_displays
release_displays()

import gc
import random
import displayio
import time
import busio
import board
import adafruit_focaltouch
from adafruit_display_text import label
import terminalio

from display_setup import init_display
from ocean import create_ocean
from diver import create_diver, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE

FISH_NAMES = [
    "Clownfish", "Blue Tang", "Angelfish", "Pufferfish",
    "Barracuda", "Manta Ray", "Seahorse", "Swordfish",
    "Lionfish", "Parrotfish", "Triggerfish", "Moray Eel",
    "Hammerhead", "Starfish", "Jellyfish", "Octopus",
    "Marlin", "Tuna", "Grouper", "Butterflyfish",
]

print("=" * 40)
print("Scuba Diver Game")
print("=" * 40)
print(f"Free memory: {gc.mem_free()} bytes")

display = init_display()
W = display.width
H = display.height
print(f"Logical size: {W}x{H}")

print("[touch] Init FocalTech...")
i2c = busio.I2C(board.SCL, board.SDA, frequency=400_000)
touch = adafruit_focaltouch.Adafruit_FocalTouch(i2c, address=0x38)
print("[touch] Ready")

ocean_tg = create_ocean(W, H)
diver_group = create_diver()
diver_tg = diver_group[0]

DIVER_W = SPRITE_WIDTH * SCALE
DIVER_H = SPRITE_HEIGHT * SCALE
MARGIN = 40
HIT_PADDING = 20

fish_label = label.Label(
    terminalio.FONT,
    text="",
    color=0xFFFFFF,
    scale=3,
    anchor_point=(0.5, 1.0),
)
fish_label.hidden = True


def touch_to_logical(tx, ty):
    """Convert physical touch coords to logical display coords for rotation=90."""
    return (ty, H - 1 - tx)


scene = displayio.Group()
scene.append(ocean_tg)
scene.append(diver_group)
scene.append(fish_label)

display.root_group = scene
display.auto_refresh = True

gc.collect()
print()
print(f"Scene ready, mem={gc.mem_free()}")
print(f"[game] Touch the diver to name a fish!")
print("-" * 40)

x = float(-DIVER_W)
y = float(H // 2)
target_y = y
speed_x = 60.0

next_depth_change = 0.0
next_speed_change = 0.0
label_hide_time = 0.0
touch_cooldown = 0.0
score = 0

last_time = time.monotonic()
frame = 0

while True:
    now = time.monotonic()
    dt = now - last_time
    last_time = now

    if now >= next_depth_change:
        drift = random.randint(-30, 30)
        target_y = max(MARGIN, min(H - DIVER_H - MARGIN, y + drift))
        next_depth_change = now + random.uniform(3.0, 8.0)

    if now >= next_speed_change:
        speed_x = random.uniform(30.0, 100.0)
        next_speed_change = now + random.uniform(3.0, 7.0)

    x += speed_x * dt
    if x > W + DIVER_W:
        x = float(-DIVER_W)

    dy = target_y - y
    y += dy * min(dt * 0.5, 1.0)

    diver_group.x = int(x)
    diver_group.y = int(y)

    if label_hide_time > 0 and now >= label_hide_time:
        fish_label.hidden = True
        label_hide_time = 0.0

    if touch.touched and now >= touch_cooldown:
        for t in touch.touches:
            lx, ly = touch_to_logical(t["x"], t["y"])
            dx = int(x)
            dy_pos = int(y)
            hit = (dx - HIT_PADDING <= lx <= dx + DIVER_W + HIT_PADDING and
                   dy_pos - HIT_PADDING <= ly <= dy_pos + DIVER_H + HIT_PADDING)
            if hit:
                score += 1
                name = random.choice(FISH_NAMES)
                fish_label.text = name
                fish_label.x = max(10, min(W - 10, dx + DIVER_W // 2))
                fish_label.y = max(30, dy_pos - 5)
                fish_label.hidden = False
                label_hide_time = now + 2.0
                touch_cooldown = now + 0.5
                print(f"[game] #{score} {name}! touch=({lx},{ly})")
                break

    frame += 1
    if frame % 500 == 0:
        print(f"[swim] f={frame} score={score} pos=({int(x)},{int(y)}) mem={gc.mem_free()}")

    time.sleep(0.03)
