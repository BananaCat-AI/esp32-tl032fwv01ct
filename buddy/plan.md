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
**Status**: In progress  
**Deliverable**: Diver character visible on the ocean background.

- [x] Create `diver.py` — `create_diver()` returns a scaled Group
- [x] 19x19 pixel art with 9-color palette (wetsuit, skin, mask, tank, flippers, bubbles)
- [x] Transparent background via `Palette.make_transparent()`
- [x] 4x scale → 76x76 pixels on screen
- [ ] Verify diver is visible and recognizable on display

### Milestone 3 — Swimming animation
**Goal**: The diver moves smoothly across the screen.  
**Estimated time**: ~15 min  

- [ ] Implement swim path (sine wave horizontal + slow vertical drift)
- [ ] Game loop with frame timing (~15-20 FPS target)
- [ ] Print frame rate to serial periodically

### Milestone 4 — Touch detection
**Goal**: Touching the diver triggers a response.  
**Estimated time**: ~15 min  

- [ ] Install `adafruit_display_text` on the board
- [ ] Init FocalTech touch controller alongside display
- [ ] Check touch events each frame
- [ ] Hit detection: touch inside diver bounding box → print "HIT" to serial
- [ ] Note: touch coordinates may need rotation mapping (physical vs logical)

### Milestone 5 — Fish names on screen
**Goal**: Complete game — touch the diver, see a fish name.  
**Estimated time**: ~15 min  

- [ ] Add list of ~20 fish names
- [ ] On hit: pick random name, render as `Label` near touch point
- [ ] Auto-hide label after ~2 seconds

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
| `adafruit_display_text` | Install at Milestone 4 | Fish name labels |

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
