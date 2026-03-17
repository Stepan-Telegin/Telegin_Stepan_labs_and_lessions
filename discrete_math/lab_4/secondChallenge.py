import math
from LAB4 import text as lab4_text, char_counts

# ------------------------
# получение кодов
# ------------------------

codes = {}

def build_codes(node, code=""):

    if isinstance(node[1], str):
        codes[node[1]] = code
        return

    build_codes(node[1][0], code + "0")
    build_codes(node[1][1], code + "1")


# ------------------------
# построение дерева Хаффмана (обёрнуто в функцию)
# ------------------------

def build_huffman_codes(freq):
    global codes

    nodes = []

    for symbol in freq:
        nodes.append([freq[symbol], symbol])

    while len(nodes) > 1:

        # сортировка по частоте
        nodes = sorted(nodes, key=lambda x: x[0])

        left = nodes[0]
        right = nodes[1]

        nodes = nodes[2:]

        new_node = [left[0] + right[0], [left, right]]

        nodes.append(new_node)

    tree = nodes[0]

    codes = {}
    build_codes(tree)
    return dict(codes)


# ------------------------
# энтропия Шеннона
# ------------------------

def compute_entropy(freq):
    total = sum(freq.values())
    entropy = 0
    for symbol in freq:
        p = freq[symbol] / total
        entropy -= p * math.log2(p)
    return entropy


if __name__ == "__main__":
    # частоты букв из задания 1
    freq = dict(char_counts)

    # общее количество символов
    total = sum(freq.values())

    huffman_codes = build_huffman_codes(freq)

    print("Коды Хаффмана:")

    for c in huffman_codes:
        print(c, huffman_codes[c])


    # ------------------------
    # кодирование текста
    # ------------------------

    encoded = ""

    for ch in lab4_text:
        encoded += huffman_codes[ch]

    print("\nЗакодированный текст (первые 200 бит):")
    print(encoded[:200])

    huffman_length = len(encoded)

    print("\nДлина кода Хаффмана:", huffman_length)


    # ------------------------
    # равномерный код
    # ------------------------

    uniform_length = len(lab4_text) * 5

    print("Длина равномерного кода:", uniform_length)


    # ------------------------
    # энтропия Шеннона
    # ------------------------

    entropy = compute_entropy(freq)

    print("\nЭнтропия Шеннона:", entropy)

    print("Средняя длина кода Хаффмана:", huffman_length / len(lab4_text))

    with open("huffman_encoded.txt", "w", encoding="utf-8") as f:
        f.write(encoded)

    print(f"\nЗакодированный текст записан в файл: huffman_encoded.txt")