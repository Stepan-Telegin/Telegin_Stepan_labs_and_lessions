from decimal import Decimal
import math

midpoint = Decimal("0.097481728")

full_binary = ""
temp_val = midpoint

for _ in range(50):
    temp_val *= 2

    if temp_val >= 1:
        full_binary += "1"
        temp_val -= 1
    else:
        full_binary += "0"

for length in range(1, len(full_binary) + 1):
    prefix = full_binary[:length]

    integer_value = int(prefix, 2)
    power_of_two = Decimal(2) ** length
    decoded_val = Decimal(integer_value) / power_of_two

print(prefix)
