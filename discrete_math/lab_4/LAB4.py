import re
from collections import Counter # словарь-счётчик для подсчёта частот элементов

with open("input_text.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()


def normalize(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z]+", " ", s) # всё что не латинская буква a..z заменяем на пробел
    s = re.sub(r"\s+", " ", s).strip() # два и более пробела собираем в один
    return s

text = normalize(raw_text)

N = len(text)
alphabet = sorted(set(text)) # отсортированное множество уникальных символов в тексте

char_counts = Counter(text)
char_freq = {ch: char_counts[ch] / N for ch in sorted(char_counts)} # вероятность встречи символа
 
bigrams = [text[i:i+2] for i in range(len(text)-1)] # список всех пар соседних символов
M = len(bigrams)  # число биграмм N-1
bigram_counts = Counter(bigrams) # подсчет сколько раз встречается каждая пара
bigram_freq = {bg: bigram_counts[bg] / M for bg in bigram_counts} # 

if __name__ == "__main__":
    print("=== NORMALIZED TEXT INFO ===")
    print(f"Length symbols: {N}")
    print(f"Alphabet size : {len(alphabet)}")
    print(f"Alphabet: {alphabet}")
    print()

    print("=== SYMBOL STATISTICS ===")
    print("symbol - count - probability")
    for ch in sorted(char_counts, key=lambda c: (-char_counts[c], c)):
        #char_counts[c] сколько раз встретился символ, мину нужен чтобы сортировка была в обратную сторону (по убыванию)
        # , c нужно если частота некоторых символов одинакова(будет сортировка по коду символа) 
        print(f"{repr(ch)},     {char_counts[ch]},     {char_counts[ch]/N:.8f}")
        #repr для того чтобы пробел был виден в таблице
    print()

    print("=== BIGRAM STATISTICS (top 50) ===")
    print("bigram - count - probability")
    for bg, cnt in bigram_counts.most_common(50):
        print(f"{repr(bg)},    {cnt},    {cnt/M:.8f}")