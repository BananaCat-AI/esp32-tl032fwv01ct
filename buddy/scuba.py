from displayio import release_displays
release_displays()

import gc
import displayio
import time

from display_setup import init_display
from ocean import create_ocean
from diver import create_diver

print("=" * 40)
print("Scuba Diver Game")
print("=" * 40)
print(f"Free memory: {gc.mem_free()} bytes")

display = init_display()
W = display.width
H = display.height
print(f"Logical size: {W}x{H}")

ocean_tg = create_ocean(W, H)
diver_tg = create_diver()

diver_tg.x = W // 2 - 10
diver_tg.y = H // 2 - 10

scene = displayio.Group()
scene.append(ocean_tg)
scene.append(diver_tg)

display.root_group = scene
display.auto_refresh = True

gc.collect()
print()
print(f"Scene ready, mem={gc.mem_free()}")
print("Milestone 2 — diver on ocean")
print("-" * 40)

while True:
    time.sleep(60)
