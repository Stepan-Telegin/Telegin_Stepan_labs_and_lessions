def solve_grid_paths():

    W = 22
    H = 18

    dp1 = [[0 for _ in range(W + 1)] for _ in range(H + 1)]

    dp1[0][0] = 1

    for y in range(H + 1):
        for x in range(W + 1):
            if x > 0:
                dp1[y][x] += dp1[y][x - 1]
            if y > 0:
                dp1[y][x] += dp1[y - 1][x]

    print(f"Размеры сетки: {W}x{H}")
    print(f"1. Всего кратчайших путей: {dp1[H][W]}")

    dp2 = [[[0, 0] for _ in range(W + 1)] for _ in range(H + 1)]

    dp2[0][0][0] = 1 

    for y in range(H + 1):
        for x in range(W + 1):
            if x == 0 and y == 0:
                continue

            if x > 0:
                ways_from_left = dp2[y][x - 1][0] + dp2[y][x - 1][1]
                dp2[y][x][0] = ways_from_left

            if y > 0:
                ways_from_bottom = dp2[y - 1][x][0]
                dp2[y][x][1] = ways_from_bottom

    total_restricted = dp2[H][W][0] + dp2[H][W][1]
    print(f"2. Путей без двух вертикальных подряд: {total_restricted}")

if __name__ == "__main__":
    solve_grid_paths()
    