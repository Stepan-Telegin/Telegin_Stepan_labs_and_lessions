### 3.	Реализовать алгоритм поиска по образцу с помощью конечного автомата


def build_transition_table(pattern):
    m = len(pattern)
    alphabet = set(pattern)
    transition_table = []

    for state in range(m + 1):
        state_transitions = {}

        for char in alphabet:
            current_string = pattern[:state] + char

            k = min(m, state + 1)

            while k > 0:
                if pattern[:k] == current_string[-k:]:
                    break
                k -= 1

            state_transitions[char] = k

        transition_table.append(state_transitions)

    return transition_table


def search_with_automaton(text, pattern):
    print(f"\nЗапуск поиска Конечным Автоматом")

    tf: list[dict] = build_transition_table(pattern)
    m = len(pattern)
    found_indices = []
    current_state = 0

    for i, char in enumerate(text):
        if char in tf[current_state]:
            current_state = tf[current_state][char]
        else:
            current_state = 0

        if current_state == m:
            start_index = i - m + 1
            found_indices.append(start_index)

    if found_indices:
        print(f"Найдено вхождений: {len(found_indices)}")
        print(f"Позиции (индексы начала): {found_indices}")
    else:
        print("Образец в тексте не найден.")


### 4.	Реализовать алгоритм Кнута-Морриса-Пратта для поиска по образцу


def compute_prefix_function(pattern):
    m = len(pattern)
    shifts = [0] * m
    k = 0

    for q in range(1, m):
        while k > 0 and pattern[k] != pattern[q]:
            k = shifts[k - 1]

        if pattern[k] == pattern[q]:
            k += 1

        shifts[q] = k

    return shifts


def search_kmp(text, pattern):
    print(f"\nЗапуск поиска алгоритмом Кнута-Морриса-Пратта (КМП)")

    m = len(pattern)
    n = len(text)

    shifts = compute_prefix_function(pattern)

    q = 0
    found_indices = []

    for i in range(n):
        while q > 0 and pattern[q] != text[i]:
            q = shifts[q - 1]

        if pattern[q] == text[i]:
            q += 1

        if q == m:
            start_index = i - m + 1
            found_indices.append(start_index)
            q = shifts[q - 1]

    if found_indices:
        print(f"Найдено вхождений: {len(found_indices)}")
        print(f"Позиции (индексы начала): {found_indices}")
    else:
        print("Образец в тексте не найден.")


### 5.	Реализовать алгоритм Бойера-Мура для поиска по образцу


def build_bad_char_table(pattern):
    m = len(pattern)
    table = {}

    for i in range(m - 1):
        char = pattern[i]
        table[char] = m - 1 - i

    return table


def search_boyer_moore(text, pattern):
    print(f"\nЗапуск поиска алгоритмом Бойера-Мура")

    m = len(pattern)
    n = len(text)

    if m > n:
        print("Образец длиннее текста. Поиск невозможен.")
        return

    shift_table = build_bad_char_table(pattern)

    found_indices = []
    k = 0

    while k <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[k + j]:
            j -= 1

        if j < 0:
            found_indices.append(k)

        last_char_text = text[k + m - 1]

        shift = shift_table.get(last_char_text, m)

        k += shift

    if found_indices:
        print(f"Найдено вхождений: {len(found_indices)}")
        print(f"Позиции (индексы начала): {found_indices}")
    else:
        print("Образец в тексте не найден.")


### 6.	Реализовать алгоритм Рабина для поиска по образцу


def get_rk_hash(string_slice, m):
    # h = s[0]*n^0 + s[1]*n^1 + ... + s[M-1]*n^(M-1)
    h = 0
    w = 1
    n_const = 256

    for i in range(m):
        h += w * ord(string_slice[i])
        w *= n_const

    return h


def update_rk_hash(h, char_out, char_in, m):
    # Формула: (h - out) / n + in * n^(m-1)
    n_const = 256

    nm = n_const ** (m - 1)

    h = (h - ord(char_out)) // n_const
    h += ord(char_in) * nm

    return h


def search_rabin_karp(text, pattern):
    print(f"\nЗапуск поиска алгоритмом Рабина-Карпа")

    n = len(text)
    m = len(pattern)

    if m > n:
        print("Образец длиннее текста. Поиск невозможен.")
        return

    hq = get_rk_hash(pattern, m)
    hs = get_rk_hash(text[0:m], m)

    found_indices = []

    for k in range(n - m + 1):

        if hs == hq:
            if text[k : k + m] == pattern:
                found_indices.append(k)

        if k < n - m:
            hs = update_rk_hash(hs, text[k], text[k + m], m)

    if found_indices:
        print(f"Найдено вхождений: {len(found_indices)}")
        print(f"Позиции (индексы начала): {found_indices}")
    else:
        print("Образец в тексте не найден.")


if __name__ == "__main__":
    target_pattern: str = input("Введите строку для поиска (образец): ")
    if not target_pattern:
        raise ValueError("Ошибка: Пустой поисковый запрос.")

    file_path: str = "labs_3_4_5/text.txt"

    if not target_pattern:
        print("Введена пустая строка. Поиск невозможен.")
    else:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                full_text: str = f.read()

            if not full_text:
                print("Файл пуст.")
            else:
                print(
                    f"Длина текста: {len(full_text)} символов. Ищем: '{target_pattern}'"
                )

                search_with_automaton(full_text, target_pattern)

                search_kmp(full_text, target_pattern)

                search_boyer_moore(full_text, target_pattern)

                search_rabin_karp(full_text, target_pattern)

        except FileNotFoundError:
            print(f"Ошибка: Файл '{file_path}' не найден. Проверьте путь.")
        except UnicodeDecodeError:
            print("Ошибка: Проблема с кодировкой файла (ожидается UTF-8).")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
