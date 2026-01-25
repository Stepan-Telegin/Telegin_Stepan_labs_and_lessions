import itertools


def solve_task_1():
    source_word = "ЧЕРЕСПОЛОСИЦА"
    k = 6

    raw_variations = itertools.permutations(source_word, k)

    unique_words = set(raw_variations)

    count = len(unique_words)

    print(f"Исходное слово: {source_word}")
    print(f"Длина выборки: {k}")
    print(f"Количество различных слов: {count}")


# Запуск
if __name__ == "__main__":
    solve_task_1()
