import board

# Search for the Expander & Touch Controller
i2c = board.I2C()
while i2c.try_lock():
    pass

address = i2c.scan()
for name in address:
    print(hex(name))
# Expander 0x38
# Touch Controller 0x3f


