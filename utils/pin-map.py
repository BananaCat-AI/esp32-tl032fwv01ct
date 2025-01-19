"""Pin Map Script"""
import microcontroller
import board

board_pins = []
for pin in dir(board):
    if isinstance(getattr(board, pin), microcontroller.Pin):
        pins = []
        for alias in dir(board):
            if getattr(board, alias) is getattr(board, pin):
                pins.append(f"board.{alias}")
        # Add the original GPIO name, in parentheses
        if pins:
            # Only include pins that are in the board.
            pins.append(f"({str(pin)})")
            board_pins.append(" ".join(pins))
# Sort pin names for readability
sorted_pins = sorted(board_pins)
print("Board Pins: ", sorted_pins, "\n")
