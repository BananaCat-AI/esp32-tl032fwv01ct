import board

# Search for the Expander & Touch Controller
i2c = board.I2C()
while i2c.try_lock():
    pass

address = i2c.scan()
for name in address:
    print(hex(name))
# Touch Controller 0x38 (FocalTech FT6x36, use adafruit_focaltouch)
# IO Expander 0x3f (display init, Rev A default address)


