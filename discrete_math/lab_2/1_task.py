import itertools


def solve_task_1():
    source_word = "ЧЕРЕСПОЛОСИЦА"
    k = 6

    raw_variations = itertools.permutations(source_word, k)

    unique_words = set(raw_variations)

    unique_words_list=list(unique_words)
    for i in range(0,10):
        print(unique_words_list[i])

    count = len(unique_words)

    print(f"Исходное слово: {source_word}")
    print(f"Длина выборки: {k}")
    print(f"Количество различных слов: {count}")

if __name__ == "__main__":
    solve_task_1()
