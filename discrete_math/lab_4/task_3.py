import math
import heapq


MAX_DICT_SIZE = 4096


def bits_for_uniform_code(alphabet_size: int) -> int:
    if alphabet_size <= 1:
        return 1
    return math.ceil(math.log2(alphabet_size))


def build_huffman_codes(frequencies: dict) -> dict:
    # Узлы: ('leaf', symbol) или ('node', left, right)
    heap = []
    counter = 0
    for symbol, freq in frequencies.items():
        heapq.heappush(heap, (freq, counter, ("leaf", symbol)))
        counter += 1

    if len(heap) == 1:
        # при одном символе обычно дают 1 бит
        only_symbol = heap[0][2][1]
        return {only_symbol: "0"}

    while len(heap) > 1:
        f1, _, n1 = heapq.heappop(heap)
        f2, _, n2 = heapq.heappop(heap)
        heapq.heappush(heap, (f1 + f2, counter, ("node", n1, n2)))
        counter += 1

    root = heap[0][2]
    codes = {}

    def dfs(node, prefix):
        kind = node[0]
        if kind == "leaf":
            symbol = node[1]
            codes[symbol] = prefix or "0"
            return
        dfs(node[1], prefix + "0")
        dfs(node[2], prefix + "1")

    dfs(root, "")
    return codes


def lzw_encode(text: str, char_to_index: dict, max_dict_size: int):
    dict_size = len(char_to_index)

    dict_prefix = [-1] * dict_size
    dict_char = [""] * dict_size
    for ch, idx in char_to_index.items():
        dict_char[idx] = ch

    transition = {}

    if not text:
        return [], dict_size, dict_prefix, dict_char

    output_codes = []
    current_index = char_to_index[text[0]]

    for ch in text[1:]:
        key = (current_index, ch)
        if key in transition:
            current_index = transition[key]
        else:
            output_codes.append(current_index)

            if dict_size < max_dict_size:
                transition[key] = dict_size
                dict_prefix.append(current_index)
                dict_char.append(ch)
                dict_size += 1

            current_index = char_to_index[ch]

    output_codes.append(current_index)
    return output_codes, dict_size, dict_prefix, dict_char


def main():
    input_path = "lab_4/input_text.txt"
    output_path = "lab_4/encoded_text.txt"

    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    print("Исходные данные:")
    print(f"Файл: {input_path}")
    print(f"Длина текста (в символах): {len(text)}")

    alphabet = sorted(set(text))
    alphabet_size = len(alphabet)
    print(f"Мощность алфавита: {alphabet_size}")

    print("\nАлфавит и нумерация первых гнезд словаря (один символ = одно гнездо):")
    char_to_index = {ch: i for i, ch in enumerate(alphabet)}
    for ch in alphabet:
        print(f"  {repr(ch)} -> {char_to_index[ch]}")

    frequencies = {}
    for ch in text:
        frequencies[ch] = frequencies.get(ch, 0) + 1

    total_symbols = len(text)
    information_per_symbol = 0.0
    for ch, freq in frequencies.items():
        p = freq / total_symbols
        information_per_symbol -= p * math.log2(p)
    shannon_information = information_per_symbol * total_symbols

    print("\nКоличество информации:")
    print(
        f"Количество информации на символ (H): {information_per_symbol:.6f} бит/символ"
    )
    print(f"Оценка количества информации I = N*H: {shannon_information:.2f} бит")

    # 1) Равномерный код
    uniform_bits_per_symbol = bits_for_uniform_code(alphabet_size)
    uniform_total_bits = len(text) * uniform_bits_per_symbol

    print("\nРавномерный код:")
    print(f"Длина кода символа: {uniform_bits_per_symbol} бит")
    print(f"Итого: {uniform_total_bits} бит")
    print(
        f"Средняя длина (равномерный): {uniform_total_bits / len(text):.6f} бит/символ"
    )
    print(
        f"Избыточность относительно N*H: {uniform_total_bits - shannon_information:.2f} бит"
    )

    # 2) Хаффман
    huffman_codes = build_huffman_codes(frequencies)
    huffman_total_bits = sum(
        frequencies[ch] * len(huffman_codes[ch]) for ch in frequencies
    )

    print("\n=== Код Хаффмана ===")
    print("Таблица (символ, частота, код):")
    for ch in sorted(frequencies, key=lambda x: (-frequencies[x], x)):
        print(f"  {repr(ch):>6}  freq={frequencies[ch]:>5}  code={huffman_codes[ch]}")
    print(f"Итого: {huffman_total_bits} бит")
    print(f"Средняя длина (Хаффман): {huffman_total_bits / len(text):.6f} бит/символ")
    print(
        f"Избыточность относительно N*H: {huffman_total_bits - shannon_information:.2f} бит"
    )

    # 3) LZW
    lzw_codes, final_dict_size, dict_prefix, dict_char = lzw_encode(
        text, char_to_index, MAX_DICT_SIZE
    )
    lzw_code_width = math.ceil(math.log2(MAX_DICT_SIZE))
    lzw_total_bits = len(lzw_codes) * lzw_code_width

    print("\n=== LZW ===")
    print(f"Максимальный размер словаря: {MAX_DICT_SIZE} гнезд")
    print(f"Разрядность индекса (фиксированная): {lzw_code_width} бит")
    print(f"Количество выданных индексов: {len(lzw_codes)}")
    print(f"Фактический размер словаря после кодирования: {final_dict_size}")
    print(f"Итого: {lzw_total_bits} бит")
    print(f"Средняя длина (LZW): {lzw_total_bits / len(text):.6f} бит/символ")
    print(
        f"Избыточность относительно N*H: {lzw_total_bits - shannon_information:.2f} бит"
    )

    print("\nПервые индексы LZW (для контроля):")
    print(lzw_codes[:30])

    def decode_entry(entry_index: int) -> str:
        symbols = []
        while entry_index != -1:
            symbols.append(dict_char[entry_index])
            entry_index = dict_prefix[entry_index]
        symbols.reverse()
        return "".join(symbols)

    print("\nПервые 10 добавленных гнёзд словаря (после одиночных символов):")
    first_added = alphabet_size
    last = min(final_dict_size, first_added + 10)
    for idx in range(first_added, last):
        print(
            f"  гнездо {idx}: {repr(decode_entry(idx))} (prefix={dict_prefix[idx]}, char={repr(dict_char[idx])})"
        )

    with open(output_path, "w", encoding="utf-8") as f:
        for code in lzw_codes:
            f.write(f"{code:0{lzw_code_width}b}")

    print(f"\nДвоичный поток LZW записан в файл: {output_path}")
    print(f"Первые {min(120, lzw_total_bits)} бит (для контроля):")
    with open(output_path, "r", encoding="utf-8") as f:
        print(f.read(120))

    # Сравнение
    print("\n=== Сравнение (число бит) ===")
    print(f"Равномерный код : {uniform_total_bits}")
    print(f"Хаффман         : {huffman_total_bits}")
    print(f"LZW             : {lzw_total_bits}")

    print("\n=== Отношение к равномерному коду ===")
    print(f"Хаффман / равномерный: {huffman_total_bits / uniform_total_bits:.4f}")
    print(f"LZW     / равномерный: {lzw_total_bits / uniform_total_bits:.4f}")


if __name__ == "__main__":
    main()
