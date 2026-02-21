import displayio
import bitmaptools
import time


def create_ocean(width, height):
    """Create an ocean background TileGrid with a smooth blue gradient."""
    print("[ocean] Drawing background...")
    t_start = time.monotonic()

    num_bands = min(height, 160)
    palette = displayio.Palette(num_bands)

    for i in range(num_bands):
        t = i / (num_bands - 1)
        r = int(2 * (1 - t) + 30 * t)
        g = int(10 * (1 - t) + 140 * t)
        b = int(60 * (1 - t) + 180 * t)
        palette[i] = (r << 16) | (g << 8) | b

    bmp = displayio.Bitmap(width, height, num_bands)
    band_height = height / num_bands

    for i in range(num_bands):
        y0 = int(i * band_height)
        y1 = height if i == num_bands - 1 else int((i + 1) * band_height)
        bitmaptools.fill_region(bmp, 0, y0, width, y1, i)

    elapsed = time.monotonic() - t_start
    print(f"[ocean] Done in {elapsed:.3f}s ({num_bands} bands)")

    return displayio.TileGrid(bmp, pixel_shader=palette)
