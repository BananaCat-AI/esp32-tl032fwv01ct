"""Pin Map Script"""
import microcontroller
import board

"""
The pin names available in the CircuitPython `board` module are NOT the same as the names of the pins
on the microcontroller itself! The `board` pin names are `aliases` to the microcontroller pin names.
If you look at the datasheet for your microcontroller, you'll likely find a pinout with a series of pin names!
In this script we are accessing the `microcontroller.pin` module to get the microcontroller pin name.
The mapping results in: `board.<pin alias> (<microcontroller pin name>)` where the <pin alias> is the same as 
the one printed on the board.
"""
board_pins = []
for pin in dir(microcontroller.pin):
    if isinstance(getattr(microcontroller.pin, pin), microcontroller.Pin):
        pins = []
        for alias in dir(board):
            if getattr(board, alias) is getattr(microcontroller.pin, pin):
                pins.append(f"board.{alias}")
        # Add the original GPIO name, in parentheses
        if pins:
            # Only include pins that are in the board.
            pins.append(f"({str(pin)})")
            board_pins.append(" ".join(pins))
# Sort pin names for readability
sorted_pins = sorted(board_pins)
print("Board Pins: ", sorted_pins, "\n")
