# Scuba Diver Game

A small interactive game for the TL032FWV01CT display (320x820).  
A scuba diver swims around the screen. Touch the diver to get a random fish name.

## Architecture

The game uses `displayio.Group` as a scene graph with layered elements:

```
Display (320x820)
└── Group (root)
    ├── TileGrid: Ocean background (full screen, blue gradient)
    ├── TileGrid: Scuba diver sprite (~48x48, transparent background)
    └── Label: Fish name text (appears on touch, disappears after delay)
```

All graphics are drawn programmatically — no image files needed on the board.

---

## Milestones

Each milestone is a self-contained session that produces a working result on the display.

### Milestone 1 — Ocean background
**Goal**: Full-screen ocean scene rendered on the display.  
**Estimated time**: ~15 min  
**Deliverable**: `buddy/scuba.py` shows a blue ocean gradient with serial output confirming render time.

- [ ] Create `buddy/scuba.py` with display init (reuse from rainbow-display)
- [ ] Draw ocean background: dark blue at top, lighter blue/teal at bottom
- [ ] Deploy and verify on display via `tio`

### Milestone 2 — Scuba diver sprite
**Goal**: A recognizable diver character appears on the ocean.  
**Estimated time**: ~20 min  
**Deliverable**: Static diver sprite composited on top of the ocean background.

- [ ] Design diver sprite as a small palette-based bitmap (~48x48)
- [ ] Use `Palette.make_transparent()` so background pixels don't cover the ocean
- [ ] Add diver `TileGrid` to the scene group, position it mid-screen
- [ ] Deploy and verify diver is visible on the ocean

### Milestone 3 — Swimming animation
**Goal**: The diver moves smoothly across the screen.  
**Estimated time**: ~15 min  
**Deliverable**: Diver swims in a looping path, serial output shows frame rate.

- [ ] Implement a swim path (sine wave horizontal + slow vertical drift)
- [ ] Add game loop with frame timing (~15-20 FPS target)
- [ ] Print frame rate to serial every few seconds
- [ ] Deploy and verify smooth movement

### Milestone 4 — Touch detection
**Goal**: Touching the diver triggers a response.  
**Estimated time**: ~15 min  
**Deliverable**: Touch the diver and see a message in `tio`. Touch elsewhere = nothing.

- [ ] Install `adafruit_display_text` on the board
- [ ] Init FocalTech touch controller alongside display
- [ ] On each frame, check for touch events
- [ ] If touch coordinates overlap diver bounding box, print "HIT" + coordinates to serial
- [ ] Deploy and verify hit detection accuracy

### Milestone 5 — Fish names on screen
**Goal**: Complete game — touch the diver, see a fish name on the display.  
**Estimated time**: ~15 min  
**Deliverable**: Full interactive game loop.

- [ ] Add list of ~20 fish names
- [ ] On diver hit: pick a random fish name
- [ ] Render fish name as a `Label` near the touch point
- [ ] Auto-hide the label after ~2 seconds
- [ ] Deploy and play!

### Milestone 6 — Polish (optional)
**Goal**: Visual and gameplay improvements.  
**Estimated time**: ~20 min  

- [ ] Add bubble particles rising from the diver
- [ ] Add a score counter (how many fish named)
- [ ] Add a splash or ripple effect on miss
- [ ] Vary diver speed or path over time
- [ ] Add seaweed or coral to the ocean floor

---

## Dependencies

| Library | Status | Purpose |
|---------|--------|---------|
| `adafruit_focaltouch` | Installed | Touch input at `0x38` |
| `adafruit_bus_device` | Installed | I2C dependency |
| `adafruit_display_text` | Install at Milestone 4 | Fish name labels |

## Hardware Reference

- Display: 320x820, RGB666, 16 MHz pixel clock
- Touch: FocalTech FT6x36 at I2C `0x38`, coordinates x: 0-320, y: 0-820
- IO Expander: `0x3f` (Rev A default)
- Memory: ~7 MB PSRAM free after framebuffer

## Key Techniques

- `bitmaptools.fill_region()` for fast rectangular fills (~0.08s full screen)
- `displayio.Palette.make_transparent(index)` for sprite transparency
- `adafruit_display_text.label.Label` for text rendering
- Moving `TileGrid.x` / `TileGrid.y` is instant (no redraw cost)

## File

```
buddy/scuba.py   — Main game script (deploy as code.py to run)
```
