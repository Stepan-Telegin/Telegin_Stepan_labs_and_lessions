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


def search_with_automaton(filename, pattern):
    print(f"\n--- Запуск поиска Конечным Автоматом ---")
    if not pattern:
        print("Ошибка: Пустой поисковый запрос.")
        return

    tf: list[dict] = build_transition_table(pattern)
    m = len(pattern)

    found_indices = []
    current_state = 0

    try:
        with open(filename, "r", encoding="utf-8") as f:
            text: str = f.read()

        print(f"Длина текста: {len(text)} символов. Ищем: '{pattern}'")

        for i, char in enumerate(text):
            if char in tf[current_state]:
                current_state = tf[current_state][char]
            else:
                current_state = 0

            if current_state == m:
                start_index = i - m + 1
                found_indices.append(start_index)

    except UnicodeDecodeError:
        print(
            "Ошибка: Не удалось прочитать файл (проблема с кодировкой, ожидается UTF-8)."
        )
        return
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        return
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return

    if found_indices:
        print(f"Найдено вхождений: {len(found_indices)}")
        print(f"Позиции (индексы начала): {found_indices}")
    else:
        print("Образец в тексте не найден.")


# ==========================================
# 2. Алгоритм Кнута-Морриса-Пратта (КМП)
# ==========================================


def build_kmp_table(pattern):
    """
    Строит таблицу сдвигов d на основе префикс-функции.
    d[j] - длина совпадения префикса и суффикса для подстроки pattern[:j].
    d[0] = -1, d[1] = 0 и т.д.
    """
    m = len(pattern)
    # Таблица d размером m+1, инициализируем d[0] = -1
    d = [0] * (m + 1)
    d[0] = -1

    # Вспомогательный массив pi (классическая префикс-функция)
    pi = [0] * m
    k = 0
    for q in range(1, m):
        while k > 0 and pattern[k] != pattern[q]:
            k = pi[k - 1]
        if pattern[k] == pattern[q]:
            k += 1
        pi[q] = k

    # Заполняем таблицу d значениями из pi со сдвигом индекса
    # d[j] (на слайде) соответствует pi[j-1]
    for i in range(m):
        d[i + 1] = pi[i]

    return d


def search_with_kmp(filename, pattern):
    print(f"\n--- Запуск поиска Кнута-Морриса-Пратта ---")
    if not pattern:
        print("Ошибка: Пустой поисковый запрос.")
        return

    # Шаг 1: Построение таблицы сдвигов
    d = build_kmp_table(pattern)
    m = len(pattern)
    found_indices = []

    try:
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()

        n = len(text)
        print(f"Длина текста: {len(text)} символов. Ищем: '{pattern}'")

        if m > n:
            print("Образец длиннее текста.")
            return

        # Шаг 2: Поиск
        k = 0  # Смещение образца относительно текста (левый край)

        # Пока образец помещается в тексте
        while k <= n - m:
            j = 0  # Сколько символов совпало

            # Сравниваем символы
            while j < m and text[k + j] == pattern[j]:
                j += 1

            # Если j == m, значит нашли полное совпадение
            if j == m:
                found_indices.append(k)

            # Вычисляем сдвиг по формуле из конспекта: shift = j - d[j]
            # Это работает и при полном совпадении (j=m), и при частичном
            shift = j - d[j]
            k += shift

    except UnicodeDecodeError:
        print("Ошибка: Не удалось прочитать файл (проблема с кодировкой).")
        return
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        return
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return

    if found_indices:
        print(f"Найдено вхождений: {len(found_indices)}")
        print(f"Позиции (индексы начала): {found_indices}")
    else:
        print("Образец в тексте не найден.")


if __name__ == "__main__":
    target_pattern: str = input("Введите строку для поиска (образец): ")
    file_path: str = "C:/Users/user/Documents/GitHub/Telegin_Stepan_labs_and_lessions/ASD/labs_3_4_5/text.txt"

    search_with_automaton(file_path, target_pattern)

    search_with_kmp(file_path, target_pattern)
