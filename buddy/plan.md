# Scuba Diver Game

A small interactive game for the TL032FWV01CT display (320x820, rotated to 820x320 landscape).  
A scuba diver swims around the screen. Touch the diver to get a random fish name.

## Architecture

The game uses `displayio.Group` as a scene graph with layered elements:

```
Display (820x320 logical, 320x820 physical @ rotation=90)
└── Group (scene)
    ├── TileGrid: Ocean background (820x320, 160-band blue gradient)
    ├── Group(scale=4): Scuba diver sprite (19x19 art → 76x76 on screen)
    └── Label: Fish name text (appears on touch, disappears after delay)
```

All graphics are drawn programmatically — no image files needed on the board.

## File Structure

```
buddy/
  scuba.py           — Main entry point (game loop, scene composition)
  display_setup.py   — Display init (init sequence, framebuffer, rotation)
  ocean.py           — Ocean background gradient rendering
  diver.py           — Diver pixel art sprite with palette transparency
  plan.md            — This file
```

When deploying, all `.py` files are copied to the CIRCUITPY root.  
`scuba.py` becomes `code.py` (CircuitPython entry point).

---

## Milestones

Each milestone is a self-contained session that produces a working result on the display.

### Milestone 1 — Ocean background
**Status**: Complete  
**Deliverable**: Full-screen ocean gradient in landscape orientation.

- [x] Create `display_setup.py` — display init returns `FramebufferDisplay`
- [x] Create `ocean.py` — `create_ocean(w, h)` returns a TileGrid
- [x] 160-band smooth gradient, dark navy top → aqua bottom
- [x] Landscape orientation via `rotation=90` (820x320 logical)
- [x] Renders in ~0.075s

### Milestone 2 — Scuba diver sprite
**Status**: Complete  
**Deliverable**: Diver character visible on the ocean background.

- [x] Create `diver.py` — `create_diver()` returns a scaled Group
- [x] 24x9 horizontal pixel art with 9-color palette (wetsuit, skin, mask, tank, flippers, bubbles)
- [x] Transparent background via `Palette.make_transparent()`
- [x] 4x scale → 96x36 pixels on screen
- [x] Redesigned as horizontal swimmer (head right, flippers left, tank on back)
- [x] Verified visible and recognizable on display

### Milestone 3 — Swimming animation
**Status**: Complete  
**Deliverable**: Diver swims naturally across the screen with random variation.

- [x] Game loop with delta-time frame timing (~32 FPS achieved)
- [x] Always swims left-to-right, wraps around when off-screen
- [x] Random depth drift: ±30px from current position every 3-8 seconds, smooth interpolation
- [x] Variable horizontal speed: 30-100 px/s, changes every 3-7 seconds
- [x] Serial output: frame count, speed, target depth, position, memory
- [x] Note: CircuitPython f-strings don't support ternary expressions or line continuation

### Milestone 4 — Touch detection
**Status**: Complete  
**Deliverable**: Touch the diver = "HIT" in serial, miss = "miss".

- [x] Installed `adafruit_display_text`, `adafruit_bitmap_font`, `adafruit_ticks` on board
- [x] Init FocalTech at `0x38` alongside display (shared I2C bus)
- [x] Touch coordinate rotation: physical (320x820) → logical (820x320) via `(ty, H-1-tx)`
- [x] Hit detection with 20px padding around diver bounding box
- [x] Note: touch fires multiple times while held — needs debounce in Milestone 5

### Milestone 5 — Fish names on screen
**Status**: Complete  
**Deliverable**: Full interactive game — touch the diver, fish name appears on display.

- [x] 20 fish names (Clownfish, Manta Ray, Hammerhead, Octopus, etc.)
- [x] On hit: random fish name rendered as `Label` (white, 3x scale) above diver
- [x] Label auto-hides after 2 seconds
- [x] 0.5s touch debounce prevents duplicate triggers from held finger
- [x] Score counter tracked in serial output
- [x] Uses `terminalio.FONT` (built-in, no extra font files needed)

### Milestone 6 — Polish (optional)
**Goal**: Visual and gameplay improvements.  
**Estimated time**: ~20 min  

- [ ] Bubble particles rising from diver
- [ ] Score counter (fish named so far)
- [ ] Splash/ripple on miss
- [ ] Vary diver speed over time
- [ ] Seaweed or coral at ocean floor

---

## Dependencies

| Library | Status | Purpose |
|---------|--------|---------|
| `adafruit_focaltouch` | Installed | Touch input at `0x38` |
| `adafruit_bus_device` | Installed | I2C dependency |
| `adafruit_display_text` | Installed | Fish name labels |
| `adafruit_bitmap_font` | Installed | Dependency for display_text |
| `adafruit_ticks` | Installed | Dependency for display_text |

## Hardware Reference

- Physical display: 320x820, RGB666, 16 MHz pixel clock
- Logical display: 820x320 (rotation=90)
- Touch: FocalTech FT6x36 at I2C `0x38`, physical coords x: 0-320, y: 0-820
- IO Expander: `0x3f` (Rev A default)
- Memory: ~7.4 MB PSRAM free after framebuffer + scene

## Performance Notes

- Ocean gradient (160 bands): 0.075s via `bitmaptools.fill_region`
- Diver sprite (19x19 pixels): 0.014s pixel-by-pixel (small enough to be fast)
- `displayio.Group(scale=N)` scales without redraw cost
- Moving `TileGrid.x` / `TileGrid.y` or `Group.x` / `Group.y` is instant
