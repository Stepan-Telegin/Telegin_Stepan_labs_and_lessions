# ============================================================
# Циклический код БЧХ (31, 16)
# Порождающий многочлен: 1000111110101111
# n = 31, m = 16, r = n - m = 15
# ============================================================

# --- Параметры варианта ---
n = 31                      # общее число элементов кодового слова
m = 16                      # число информационных элементов
r = n - m                   # число проверочных (избыточных) элементов = 15

# Порождающий многочлен в бинарном виде (старший бит слева)
generator_poly_str = "1000111110101111"
# Преобразуем в список коэффициентов (старший бит = старшая степень)
generator_poly = [int(b) for b in generator_poly_str]

print("=" * 70)
print("ЦИКЛИЧЕСКИЙ КОД БЧХ (31, 16)")
print("=" * 70)
print(f"n = {n} (общее число элементов)")
print(f"m = {m} (число информационных элементов)")
print(f"r = {r} (число проверочных элементов)")
print(f"Порождающий многочлен P(x): {generator_poly_str}")
print(f"Степень порождающего многочлена: {len(generator_poly) - 1}")
print()


# --- Функция деления многочленов по модулю 2 (XOR) ---
def poly_mod(dividend, divisor):
    """
    Деление многочлена dividend на divisor по модулю 2.
    Возвращает остаток длиной (len(divisor) - 1).
    Многочлены представлены списками бит, старший бит слева.
    """
    # Копируем, чтобы не испортить исходный
    working = list(dividend)
    divisor_len = len(divisor)

    for i in range(len(working) - divisor_len + 1):
        if working[i] == 1:
            for j in range(divisor_len):
                working[i + j] ^= divisor[j]

    # Остаток — последние (divisor_len - 1) бит
    remainder = working[-(divisor_len - 1):]
    return remainder


def poly_multiply_mod2(a, b):
    """
    Умножение двух многочленов по модулю 2.
    a и b — списки коэффициентов (старший бит слева).
    """
    deg_a = len(a) - 1
    deg_b = len(b) - 1
    result_len = deg_a + deg_b + 1
    result = [0] * result_len

    for i in range(len(a)):
        if a[i] == 1:
            for j in range(len(b)):
                result[i + j] ^= b[j]

    return result


# --- Функция кодирования (систематический код) ---
def encode_systematic(info_bits, generator_poly, n, r):
    """
    Кодирование систематическим способом:
    1) Q(x) * x^r — сдвигаем информационные биты на r позиций
    2) R(x) = (Q(x) * x^r) mod P(x) — находим остаток
    3) F(x) = Q(x) * x^r + R(x) — кодовое слово
    """
    # Шаг 1: Q(x) * x^r = info_bits + r нулей справа
    shifted = list(info_bits) + [0] * r

    # Шаг 2: находим остаток
    remainder = poly_mod(shifted, generator_poly)

    # Шаг 3: складываем (XOR) — но поскольку младшие r бит shifted нулевые,
    # просто заменяем их остатком
    codeword = list(info_bits) + remainder

    # Обрезаем/дополняем до длины n
    assert len(codeword) == n, f"Длина кодового слова {len(codeword)} != {n}"
    return codeword


# ============================================================
# ПУНКТ 1: Порождающая матрица систематического кода
# ============================================================
print("=" * 70)
print("ПУНКТ 1: Порождающая матрица систематического кода")
print("=" * 70)
print()

# Строим порождающую матрицу размером m x n
# Каждая строка — кодовое слово для единичного информационного вектора
generator_matrix = []
for i in range(m):
    # Информационный вектор: единица в позиции i, остальные нули
    info_bits = [0] * m
    info_bits[i] = 1
    codeword = encode_systematic(info_bits, generator_poly, n, r)
    generator_matrix.append(codeword)

print(f"Порождающая матрица G ({m} x {n}):")
print(f"{'Строка':>8}  {'Информ. часть':>{m}}  {'Провер. часть':>{r}}")
print("-" * (8 + 2 + m + 2 + r))
for i, row in enumerate(generator_matrix):
    info_part = ''.join(str(b) for b in row[:m])
    check_part = ''.join(str(b) for b in row[m:])
    print(f"{i + 1:>8}  {info_part}  {check_part}")
print()

# Проверка: каждая строка порождающей матрицы должна делиться на P(x) без остатка
print("Проверка: все строки делятся на P(x) без остатка...")
all_ok = True
for i, row in enumerate(generator_matrix):
    rem = poly_mod(row, generator_poly)
    if any(b != 0 for b in rem):
        print(f"  ОШИБКА в строке {i + 1}: остаток = {''.join(str(b) for b in rem)}")
        all_ok = False
if all_ok:
    print("  ОК — все строки делятся без остатка.")
print()

# --- Генерация ВСЕХ кодовых слов ---
print("Генерация всех кодовых слов (2^m = 2^16 = 65536 слов)...")

all_codewords = []
for info_int in range(2 ** m):
    # Преобразуем целое число в список бит длиной m
    info_bits = []
    for bit_pos in range(m - 1, -1, -1):
        info_bits.append((info_int >> bit_pos) & 1)
    codeword = encode_systematic(info_bits, generator_poly, n, r)
    all_codewords.append(codeword)

print(f"Всего сгенерировано кодовых слов: {len(all_codewords)}")
print()

# Фрагмент множества кодовых слов
print("Фрагмент множества кодовых слов (первые 20 и последние 5):")
print(f"{'№':>6}  {'Инф. вектор':>{m}}  {'Кодовое слово':>{n}}  {'Вес'}")
print("-" * (6 + 2 + m + 2 + n + 2 + 4))
for idx in list(range(20)) + ['...'] + list(range(len(all_codewords) - 5, len(all_codewords))):
    if idx == '...':
        print("   ...")
        continue
    cw = all_codewords[idx]
    weight = sum(cw)
    info_str = ''.join(str(b) for b in cw[:m])
    cw_str = ''.join(str(b) for b in cw)
    print(f"{idx:>6}  {info_str}  {cw_str}  {weight:>3}")
print()

# --- Вычисление минимального кодового расстояния ---
# Для линейного кода dmin = минимальный вес Хэмминга ненулевого кодового слова
print("Вычисление минимального кодового расстояния dmin...")
print("(Для линейного кода dmin = минимальный вес ненулевого кодового слова)")

min_weight = n + 1  # начальное значение больше максимально возможного
min_weight_codeword = None
min_weight_index = -1

for idx in range(1, len(all_codewords)):  # пропускаем нулевое слово
    weight = sum(all_codewords[idx])
    if weight < min_weight:
        min_weight = weight
        min_weight_codeword = all_codewords[idx]
        min_weight_index = idx

print(f"Минимальное кодовое расстояние dmin = {min_weight}")
print(f"Кодовое слово с минимальным весом (индекс {min_weight_index}):")
print(f"  {''.join(str(b) for b in min_weight_codeword)}")
print()

# Фрагмент таблицы кодовых расстояний (расстояния Хэмминга между несколькими парами)
print("Фрагмент таблицы кодовых расстояний (первые 10 кодовых слов):")
fragment_size = 10
print(f"{'':>6}", end="")
for j in range(fragment_size):
    print(f"{j:>4}", end="")
print()
for i in range(fragment_size):
    print(f"{i:>6}", end="")
    for j in range(fragment_size):
        # Расстояние Хэмминга
        dist = sum(a ^ b for a, b in zip(all_codewords[i], all_codewords[j]))
        print(f"{dist:>4}", end="")
    print()
print()

# Распределение весов
print("Распределение весов кодовых слов:")
weight_distribution = {}
for cw in all_codewords:
    w = sum(cw)
    weight_distribution[w] = weight_distribution.get(w, 0) + 1
for w in sorted(weight_distribution.keys()):
    print(f"  Вес {w:>2}: {weight_distribution[w]} слов")
print()

# ============================================================
# ПУНКТ 2: Характеристики кода
# ============================================================
print("=" * 70)
print("ПУНКТ 2: Характеристики кода")
print("=" * 70)
print()

dmin = min_weight

# Кратность гарантированно обнаруживаемых ошибок: q_обн = dmin - 1
q_detect = dmin - 1

# Кратность гарантированно исправляемых ошибок:
# q_исп = (dmin - 1) / 2 при нечётном dmin
# q_исп = dmin / 2 - 1 при чётном dmin
if dmin % 2 == 1:
    q_correct = (dmin - 1) // 2
else:
    q_correct = dmin // 2 - 1

print(f"Минимальное кодовое расстояние dmin = {dmin}")
print()
print(f"В режиме ОБНАРУЖЕНИЯ ошибок:")
print(f"  Кратность гарантированно обнаруживаемых ошибок: q_обн = dmin - 1 = {q_detect}")
print()
print(f"В режиме ИСПРАВЛЕНИЯ ошибок:")
print(f"  Кратность гарантированно исправляемых ошибок: q_исп = (dmin - 1) / 2 = {q_correct}")
print()
print(f"Согласно таблице БЧХ из лекции: n=31, m=16, s=3, dmin=7")
print(f"Наш результат: dmin = {dmin}, q_исп = {q_correct}, q_обн = {q_detect}")
print()

# ============================================================
# ПУНКТ 3: Примеры, иллюстрирующие свойства кода
# ============================================================
print("=" * 70)
print("ПУНКТ 3: Примеры, иллюстрирующие свойства кода")
print("=" * 70)
print()

# --- Пример 3.1: Делимость кодового слова на порождающий многочлен ---
print("--- Пример 3.1: Делимость кодового слова на P(x) ---")
example_info = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1]
example_codeword = encode_systematic(example_info, generator_poly, n, r)
example_remainder = poly_mod(example_codeword, generator_poly)
print(f"Информационное слово:  {''.join(str(b) for b in example_info)}")
print(f"Кодовое слово:         {''.join(str(b) for b in example_codeword)}")
print(f"Остаток от деления на P(x): {''.join(str(b) for b in example_remainder)}")
print(f"Синдром = 0 => ошибок нет. Кодовое слово разрешённое.")
print()

# --- Пример 3.2: Обнаружение ошибки ---
print("--- Пример 3.2: Обнаружение ошибки (вносим 1 ошибку) ---")
received_word = list(example_codeword)
error_position = 5
received_word[error_position] ^= 1  # вносим ошибку в позицию 5
error_vector = [0] * n
error_vector[error_position] = 1
syndrome = poly_mod(received_word, generator_poly)
print(f"Отправленное кодовое слово: {''.join(str(b) for b in example_codeword)}")
print(f"Вектор ошибки:              {''.join(str(b) for b in error_vector)}")
print(f"Принятое слово:             {''.join(str(b) for b in received_word)}")
print(f"Синдром: {''.join(str(b) for b in syndrome)}")
print(f"Синдром ≠ 0 => ошибка обнаружена!")
print()

# --- Пример 3.3: Обнаружение 3-кратной ошибки ---
print(f"--- Пример 3.3: Обнаружение {q_correct}-кратной ошибки (= макс. исправляемой) ---")
received_word_3 = list(example_codeword)
error_positions_3 = [2, 10, 25]
error_vector_3 = [0] * n
for pos in error_positions_3:
    received_word_3[pos] ^= 1
    error_vector_3[pos] = 1
syndrome_3 = poly_mod(received_word_3, generator_poly)
print(f"Отправленное кодовое слово: {''.join(str(b) for b in example_codeword)}")
print(f"Позиции ошибок: {error_positions_3}")
print(f"Вектор ошибки:              {''.join(str(b) for b in error_vector_3)}")
print(f"Принятое слово:             {''.join(str(b) for b in received_word_3)}")
print(f"Синдром: {''.join(str(b) for b in syndrome_3)}")
print(f"Синдром ≠ 0 => ошибка обнаружена!")
print()

# --- Пример 3.4: Обнаружение 6-кратной ошибки (= dmin-1) ---
print(f"--- Пример 3.4: Обнаружение {q_detect}-кратной ошибки (= dmin - 1, макс. гарантированно обнаруживаемая) ---")
received_word_6 = list(example_codeword)
error_positions_6 = [0, 3, 7, 15, 22, 29]
error_vector_6 = [0] * n
for pos in error_positions_6:
    received_word_6[pos] ^= 1
    error_vector_6[pos] = 1
syndrome_6 = poly_mod(received_word_6, generator_poly)
print(f"Отправленное кодовое слово: {''.join(str(b) for b in example_codeword)}")
print(f"Позиции ошибок: {error_positions_6}")
print(f"Вектор ошибки:              {''.join(str(b) for b in error_vector_6)}")
print(f"Принятое слово:             {''.join(str(b) for b in received_word_6)}")
print(f"Синдром: {''.join(str(b) for b in syndrome_6)}")
if any(b != 0 for b in syndrome_6):
    print(f"Синдром ≠ 0 => ошибка обнаружена!")
else:
    print(f"Синдром = 0 => ошибка НЕ обнаружена (необнаруживаемая ошибка)!")
print()

# --- Пример 3.5: Циклическое свойство кода ---
print("--- Пример 3.5: Проверка циклического свойства кода ---")
print("Если кодовое слово принадлежит коду, то его циклический сдвиг тоже.")
test_cw = all_codewords[42]  # берём произвольное ненулевое кодовое слово
print(f"Исходное кодовое слово (индекс 42):  {''.join(str(b) for b in test_cw)}")
# Циклический сдвиг: последний элемент перемещается на первое место
shifted_cw = [test_cw[-1]] + test_cw[:-1]
shifted_remainder = poly_mod(shifted_cw, generator_poly)
print(f"Циклический сдвиг на 1:              {''.join(str(b) for b in shifted_cw)}")
print(f"Остаток от деления сдвинутого на P(x): {''.join(str(b) for b in shifted_remainder)}")
# Проверим, есть ли сдвинутое слово среди кодовых
shifted_is_codeword = shifted_cw in all_codewords
print(f"Сдвинутое слово является кодовым: {shifted_is_codeword}")
print()

# ============================================================
# ПУНКТ 4: Вектор ошибки, которую код обнаруживает, но не может исправить
# ============================================================
print("=" * 70)
print("ПУНКТ 4: Вектор ошибки, которую код может обнаружить, но не исправить")
print("=" * 70)
print()

# Код может исправить до q_correct = 3 ошибок.
# Код может обнаружить до q_detect = 6 ошибок.
# Ошибка кратности 4 (> q_correct, но <= q_detect) — обнаруживается, но не исправляется.

print(f"Код гарантированно исправляет до {q_correct} ошибок.")
print(f"Код гарантированно обнаруживает до {q_detect} ошибок.")
print(f"Ошибка кратности {q_correct + 1} обнаруживается, но НЕ может быть гарантированно исправлена.")
print()

example_info_4 = [1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1]
original_codeword = encode_systematic(example_info_4, generator_poly, n, r)

# Вносим 4 ошибки
error_positions_4 = [1, 8, 17, 28]
error_vector_4 = [0] * n
received_word_4 = list(original_codeword)
for pos in error_positions_4:
    received_word_4[pos] ^= 1
    error_vector_4[pos] = 1

syndrome_4 = poly_mod(received_word_4, generator_poly)

print(f"Информационное слово:       {''.join(str(b) for b in example_info_4)}")
print(f"Исходное кодовое слово:     {''.join(str(b) for b in original_codeword)}")
print(f"Вектор ошибки (кратность {q_correct + 1}): {''.join(str(b) for b in error_vector_4)}")
print(f"Позиции ошибок: {error_positions_4}")
print(f"Принятое слово:             {''.join(str(b) for b in received_word_4)}")
print(f"Синдром: {''.join(str(b) for b in syndrome_4)}")
print()

if any(b != 0 for b in syndrome_4):
    print("Синдром ≠ 0 => ошибка ОБНАРУЖЕНА.")
else:
    print("Синдром = 0 => ошибка НЕ обнаружена.")

# Проверяем, является ли принятое слово каким-то другим кодовым словом
is_another_codeword = received_word_4 in all_codewords
print(f"Принятое слово является другим кодовым словом: {is_another_codeword}")
print(f"Значит, код НЕ может исправить эту ошибку, т.к. кратность {q_correct + 1} > {q_correct} (макс. исправляемая).")
print(f"Но код её ОБНАРУЖИВАЕТ, т.к. синдром ≠ 0.")
print()

# ============================================================
# ПУНКТ 5: Сводка результатов для отчёта
# ============================================================
print("=" * 70)
print("ПУНКТ 5: СВОДКА РЕЗУЛЬТАТОВ ДЛЯ ОТЧЁТА")
print("=" * 70)
print()
print(f"1. Порождающая матрица: {m} x {n} (выведена выше)")
print(f"2. Минимальное кодовое расстояние: dmin = {dmin}")
print(f"3. Кратность гарантированно исправляемых ошибок: {q_correct}")
print(f"4. Кратность гарантированно обнаруживаемых ошибок: {q_detect}")
print(f"5. Фрагмент таблицы кодовых расстояний: выведен выше (10x10)")
print(f"6. Фрагмент множества кодовых слов: выведен выше")
print(f"7. Примеры (п.3): делимость, обнаружение, циклическое свойство")
print(f"8. Пример (п.4): 4-кратная ошибка — обнаруживается, не исправляется")
