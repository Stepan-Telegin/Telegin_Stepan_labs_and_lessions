# Порождающий многочлен: 1000111110101111
# n = 31, m = 16, r = n - m = 15

n = 31  # общее число элементов кодового слова
m = 16  # число информационных элементов
r = n - m  # число проверочных элементов = 15

# Порождающий многочлен в бинарном виде (старший бит слева)
generator_poly_str = "1000111110101111"
# Преобразуем в список коэффициентов (старший бит = старшая степень)
generator_poly = [int(b) for b in generator_poly_str]

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
    remainder = working[-(divisor_len - 1) :]
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

    return codeword


# ПУНКТ 1: Порождающая матрица систематического кода
print("=" * 70)
print("ПУНКТ 1: Порождающая матрица систематического кода")
print("=" * 70)
print()

# Строим порождающую матрицу размером m x n
# Каждая строка — кодовое слово для единичного информационного вектора
generator_matrix = []
for i in range(m):
    # единица в позиции i, остальные нули
    info_bits = [0] * m
    info_bits[i] = 1
    codeword = encode_systematic(info_bits, generator_poly, n, r)
    generator_matrix.append(codeword)

print(f"Порождающая матрица G ({m} x {n}):")
print(f"{'Строка':>8}  {'Информ. часть':>{m}}  {'Провер. часть':>{r}}")
for i, row in enumerate(generator_matrix):
    info_part = "".join(str(b) for b in row[:m])
    check_part = "".join(str(b) for b in row[m:])
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
for info_int in range(2**m):
    # Преобразуем целое число в список бит длиной m
    info_bits = [int(b) for b in format(info_int, f"0{m}b")]
    codeword = encode_systematic(info_bits, generator_poly, n, r)
    all_codewords.append(codeword)

print(f"Всего сгенерировано кодовых слов: {len(all_codewords)}")
print()

# Фрагмент множества кодовых слов
print("Фрагмент множества кодовых слов (первые 20 и последние 5):")
print(f"{'№':>6}  {'Инф. вектор':>{m}}  {'Кодовое слово':>{n}}  {'Вес'}")
for idx in (
    list(range(20)) + ["..."] + list(range(len(all_codewords) - 5, len(all_codewords)))
):
    if idx == "...":
        print("   ...")
        continue
    cw = all_codewords[idx]
    weight = sum(cw)
    info_str = "".join(str(b) for b in cw[:m])
    cw_str = "".join(str(b) for b in cw)
    print(f"{idx:>6}  {info_str}  {cw_str}  {weight:>3}")
print()

# --- Вычисление минимального кодового расстояния ---
# Для линейного кода dmin = минимальный вес Хэмминга ненулевого кодового слова,
# т.к. расстояние Хэмминга между словами A и B = вес слова (A xor B),
# а в линейном коде XOR двух любых кодовых слов — тоже кодовое слово
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

# ПУНКТ 2: Характеристики кода
print("=" * 70)
print("ПУНКТ 2: Характеристики кода")
print("=" * 70)
print()

dmin = min_weight

# Кратность гарантированно обнаруживаемых ошибок: q_обн = dmin - 1
# Если произошло до q_обн ошибок, код их заметит
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
print(
    f"  Кратность гарантированно обнаруживаемых ошибок: q_обн = dmin - 1 = {q_detect}"
)
print()
print(f"В режиме ИСПРАВЛЕНИЯ ошибок:")
print(
    f"  Кратность гарантированно исправляемых ошибок: q_исп = (dmin - 1) / 2 = {q_correct}"
)
print()

# ПУНКТ 3: Примеры, иллюстрирующие свойства кода
print("=" * 70)
print("ПУНКТ 3: Примеры, иллюстрирующие свойства кода")
print("=" * 70)

import itertools

# Генерируем таблицу синдромов (сопоставляем остаток деления вектору ошибки)
# Для каждого остатка
# (синдрома) мы запоминаем ошибку (вес 1, 2 или 3), которая его дает.
error_syndromes = {}
for weight in range(1, q_correct + 1):
    for positions in itertools.combinations(range(n), weight):
        e_vector = [0] * n
        for p in positions:
            e_vector[p] = 1
        # Синдром - это остаток от деления (имитация деления в столбик)
        s = tuple(poly_mod(e_vector, generator_poly))
        if s not in error_syndromes:
            error_syndromes[s] = positions

print("\nФрагмент таблицы синдромов (первые 10 исправимых ошибок):")
# Исправленная строка форматирования: {r+2} теперь в фигурных скобках
print(f"{'Синдром (остаток)':<{r+2}} | {'Позиции ошибок'}")
print("-" * (r + 25))
for s_tuple, positions in list(error_syndromes.items())[:10]:
    s_str = "".join(str(b) for b in s_tuple)
    print(f"{s_str:<{r+2}} | {positions}")
print("-" * (r + 25))


def try_correct_with_report(word, original_word=None):
    """
    Процесс исправления:
    1. Вычисляем остаток (синдром) принятого слова.
    2. Если остаток 0 - считаем, что ошибок нет.
    3. Если не 0 - ищем такой остаток в таблице и инвертируем биты в найденных позициях.
    """
    # Вычисляем синдром
    s = tuple(poly_mod(word, generator_poly))
    s_str = "".join(str(b) for b in s)
    print(f"  Деление в столбик выполнено. Остаток (синдром): {s_str}")

    if all(b == 0 for b in s):
        print("  Синдром нулевой. Слово считается верным.")
        return list(word)

    print(
        "  Синдром != 0. Ошибка обнаружена. Обращаемся к таблице синдромов..."
    )

    if s in error_syndromes:
        pos = error_syndromes[s]
        print(
            f"  Совпадение найдено. Синдром соответствует ошибке в битах: {pos}"
        )
        corrected = list(word)
        for p in pos:
            corrected[p] ^= 1  # Исправляем ошибку (инверсия)

        if original_word:
            is_ok = corrected == original_word
            print(
                f"  [Результат] Биты исправлены. Совпадение с оригиналом: {'ДА' if is_ok else 'НЕТ (Ложное исправление)'}"
            )
        return corrected
    else:
        print(
            "  [Результат] ОТКАЗ. Такого остатка нет в таблице (кратность ошибки > 3)."
        )
        return None


example_info = [1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0]
example_cw = encode_systematic(example_info, generator_poly, n, r)

print(f"Исходное слово: {''.join(str(b) for b in example_cw)}\n")

print("--- Пример 3.1: Исправление одиночной ошибки ---")
r1 = list(example_cw)
r1[10] ^= 1  # Вносим 1 ошибку
try_correct_with_report(r1, example_cw)

print("\n--- Пример 3.2: Исправление 3-х ошибок (предел кода) ---")
r3 = list(example_cw)
for p in [2, 15, 30]:
    r3[p] ^= 1  # Вносим 3 ошибки
try_correct_with_report(r3, example_cw)

print("\n--- Пример 3.3: Циклическое свойство ---")
# Циклический сдвиг слова — это тоже разрешенное кодовое слово (остаток будет 0)
shifted = [example_cw[-1]] + example_cw[:-1]
rem_shifted = poly_mod(shifted, generator_poly)
print(f"  Сдвинутое слово: {''.join(str(b) for b in shifted)}")
print(f"  Остаток от деления: {''.join(str(b) for b in rem_shifted)}")
print(f"  Сдвиг является кодовым словом: {all(b == 0 for b in rem_shifted)}")

# ПУНКТ 4: Ошибка, которую код обнаружит, но не исправит
print("\n" + "=" * 70)
print("ПУНКТ 4: Ошибка кратности 4 (обнаруживается, но не исправляется)")
print("=" * 70)

# Вносим 4 ошибки. d_min=7, значит t=3. 4 ошибки — это "серая зона".
r4 = list(example_cw)
err_pos4 = [10, 11, 12, 13]
for p in err_pos4:
    r4[p] ^= 1

print(f"Внесено 4 ошибки в позиции: {err_pos4}")
result4 = try_correct_with_report(r4, example_cw)

if result4 is None:
    print("Код ОБНАРУЖИЛ ошибку (синдром не 0), но произошел ОТКАЗ в исправлении.")
    print(
        "Это случилось, потому что остаток от 4 ошибок не совпал ни с одним остатком из таблицы для 1-3 ошибок."
    )
else:
    print("Код ОБНАРУЖИЛ ошибку, но исправил её НЕВЕРНО.")
    print(
        "4 ошибки от исходного слова сделали его похожим на какое-то другое кодовое слово.")

# ПУНКТ 5: Сводка результатов
print("=" * 70)
print("ПУНКТ 5: СВОДКА РЕЗУЛЬТАТОВ")
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
