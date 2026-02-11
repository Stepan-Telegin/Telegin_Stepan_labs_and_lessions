def solve_egg_drop(eggs_count, floors_count):

    table = [[0 for _ in range(floors_count + 1)] for _ in range(eggs_count + 1)]

    for j in range(1, floors_count + 1):
        table[1][j] = j

    for i in range(1, eggs_count + 1):
        table[i][0] = 0
        table[i][1] = 1

    inf = 10**10

    for i in range(2, eggs_count + 1):
        for j in range(2, floors_count + 1):

            table[i][j] = inf

            for x in range(1, j + 1):

                broken = table[i - 1][x - 1]

                not_broken = table[i][j - x]

                res = 1 + max(broken, not_broken)

                if res < table[i][j]:
                    table[i][j] = res

    return table[eggs_count][floors_count]


if __name__ == "__main__":
    N_FLOORS = 100
    K_EGGS = 2

    result = solve_egg_drop(K_EGGS, N_FLOORS)

    print(f"Дано:")
    print(f"Этажей: {N_FLOORS}")
    print(f"Яиц: {K_EGGS}")
    print("-" * 20)
    print(f"Минимальное количество бросков (гарантированно): {result}")
