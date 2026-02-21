import time
import board
import busio

print("=" * 40)
print("Touch Controller Test")
print("=" * 40)

i2c = busio.I2C(board.SCL, board.SDA, frequency=400_000)

while not i2c.try_lock():
    pass
addresses = i2c.scan()
i2c.unlock()
print(f"I2C devices found: {[hex(a) for a in addresses]}")

ctp = None
driver_name = None

# Try FocalTech (FT6x06/FT6x36) — common at 0x38
try:
    import adafruit_focaltouch
    print("Trying FocalTech at 0x38...", end=" ")
    ctp = adafruit_focaltouch.Adafruit_FocalTouch(i2c, address=0x38)
    driver_name = "FocalTech"
    print("OK!")
except Exception as e:
    print(f"failed ({e})")

# Try CST8XX — common at 0x15
if ctp is None:
    try:
        import adafruit_cst8xx
        for addr in [0x15, 0x38, 0x3f]:
            if addr not in addresses:
                continue
            try:
                print(f"Trying CST8XX at {hex(addr)}...", end=" ")
                ctp = adafruit_cst8xx.Adafruit_CST8XX(i2c, address=addr)
                driver_name = "CST8XX"
                print("OK!")
                break
            except Exception as e:
                print(f"failed ({e})")
    except ImportError:
        print("adafruit_cst8xx not installed, skipping")

if ctp is None:
    print("ERROR: No touch controller found.")
    print("Halting.")
    while True:
        time.sleep(60)

print()
print(f"Driver: {driver_name}")
print("Touch the display! Events will print below.")
print("-" * 40)

while True:
    if ctp.touched:
        for i, touch in enumerate(ctp.touches):
            x = touch["x"]
            y = touch["y"]
            print(f"  id={i}  x={x:4d}  y={y:4d}")
    time.sleep(0.05)
