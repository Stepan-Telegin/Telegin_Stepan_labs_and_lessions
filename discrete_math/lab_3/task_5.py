from decimal import Decimal, getcontext
import math

getcontext().prec = 50


def get_symbol_ranges(probabilities):
    ranges = {}
    current_low = Decimal("0.0")

    sorted_keys = ["a", "b", "c", "d", "e", "f"]

    for char in sorted_keys:
        prob = Decimal(str(probabilities[char]))
        high = current_low + prob
        ranges[char] = (current_low, high)
        print(f"Symbol: {char}, Prob: {prob}, Range: [{current_low}, {high})")
        current_low = high
    print("-----------------------------------\n")
    return ranges


def arithmetic_encode(input_string, ranges):
    low = Decimal("0.0")
    high = Decimal("1.0")

    print(f"Start: [{low}, {high})")

    for char in input_string:
        current_range = high - low

        char_low, char_high = ranges[char]

        new_high = low + current_range * char_high
        new_low = low + current_range * char_low

        low = new_low
        high = new_high

        print(f"Symbol '{char}': New Interval [{low:.10f}..., {high:.10f}...)")

    return low, high


def find_shortest_binary_in_range(low, high):
    midpoint = (low + high) / 2

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

        if low <= decoded_val < high:
            return prefix

    return full_binary


def solve_task():
    alphabet_probs = {"a": 0.05, "b": 0.10, "c": 0.05, "d": 0.55, "e": 0.15, "f": 0.10}
    target_string = "eacdbf"

    ranges = get_symbol_ranges(alphabet_probs)

    final_low, final_high = arithmetic_encode(target_string, ranges)
    print(f"\nFinal Interval: \nLow : {final_low}\nHigh: {final_high}")

    binary_code = find_shortest_binary_in_range(final_low, final_high)
    print(f"\nResult Binary Code: {binary_code}")
    print(f"Length of code: {len(binary_code)} bits")

    num_symbols = len(alphabet_probs)
    bits_per_symbol = math.ceil(math.log2(num_symbols))
    original_size_bits = len(target_string) * bits_per_symbol
    compressed_size_bits = len(binary_code)

    print("\n--- Statistics ---")
    print(
        f"Uniform coding size ({len(target_string)} chars * {bits_per_symbol} bits): {original_size_bits} bits"
    )
    print(f"Arithmetic coding size: {compressed_size_bits} bits")

    compression_ratio = compressed_size_bits / original_size_bits

    compression_coefficient = original_size_bits / compressed_size_bits

    print(
        f"Compression Ratio (Степень сжатия): {compression_ratio:.4f} (or {compression_ratio*100:.2f}%)"
    )
    print(
        f"Compression Coefficient (Коэффициент сжатия): {compression_coefficient:.4f}"
    )


if __name__ == "__main__":
    solve_task()
