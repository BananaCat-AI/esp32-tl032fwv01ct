from displayio import release_displays
release_displays()

import gc
import random
import displayio
import time

from display_setup import init_display
from ocean import create_ocean
from diver import create_diver, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE

print("=" * 40)
print("Scuba Diver Game")
print("=" * 40)
print(f"Free memory: {gc.mem_free()} bytes")

display = init_display()
W = display.width
H = display.height
print(f"Logical size: {W}x{H}")

ocean_tg = create_ocean(W, H)
diver_group = create_diver()
diver_tg = diver_group[0]

DIVER_W = SPRITE_WIDTH * SCALE
DIVER_H = SPRITE_HEIGHT * SCALE
MARGIN = 40

scene = displayio.Group()
scene.append(ocean_tg)
scene.append(diver_group)

display.root_group = scene
display.auto_refresh = True

gc.collect()
print()
print(f"Scene ready, mem={gc.mem_free()}")
print(f"[swim] Diver: {DIVER_W}x{DIVER_H}, display: {W}x{H}")
print("-" * 40)

x = float(-DIVER_W)
y = float(H // 2)
target_y = y
speed_x = 60.0

next_depth_change = 0.0
next_speed_change = 0.0

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

    frame += 1
    if frame % 200 == 0:
        print(f"[swim] f={frame} spd={speed_x:.0f} tgt_y={int(target_y)} pos=({int(x)},{int(y)}) mem={gc.mem_free()}")

    time.sleep(0.03)
