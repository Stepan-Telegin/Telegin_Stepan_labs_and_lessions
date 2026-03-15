import math

# частоты букв (их нужно вставить из задания 1)
freq = {
    'a': 50,
    'b': 20,
    'c': 15,
    'd': 10,
    'e': 5
}

# общее количество символов
total = sum(freq.values())

# ------------------------
# построение дерева Хаффмана
# ------------------------

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


build_codes(tree)

print("Коды Хаффмана:")

for c in codes:
    print(c, codes[c])


# ------------------------
# кодирование текста
# ------------------------

text = "abcdeabcde"

encoded = ""

for ch in text:
    encoded += codes[ch]

print("\nЗакодированный текст:")
print(encoded)

huffman_length = len(encoded)

print("\nДлина кода Хаффмана:", huffman_length)


# ------------------------
# равномерный код
# ------------------------

uniform_length = len(text) * 5

print("Длина равномерного кода:", uniform_length)


# ------------------------
# энтропия Шеннона
# ------------------------

entropy = 0

for symbol in freq:

    p = freq[symbol] / total
    entropy -= p * math.log2(p)

print("\nЭнтропия Шеннона:", entropy)

print("Средняя длина кода Хаффмана:", huffman_length / len(text))