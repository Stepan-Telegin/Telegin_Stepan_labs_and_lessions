def solve_lab_9(matrix):

    n = len(matrix)

    total_states = 1 << n

    inf = 10**10
    table = [[inf] * n for _ in range(total_states)]

    parent = [[-1] * n for _ in range(total_states)]

    table[1][0] = 0

    for mask in range(1, total_states):
        for u in range(n):
            if not (mask & (1 << u)):
                continue

            prev_mask = mask ^ (1 << u)

            if prev_mask == 0:
                continue

            for v in range(n):
                if prev_mask & (1 << v):
                    if table[prev_mask][v] + matrix[v][u] < table[mask][u]:
                        table[mask][u] = table[prev_mask][v] + matrix[v][u]
                        parent[mask][u] = v

    final_mask = total_states - 1
    min_path_cost = inf
    last_city = -1

    for i in range(1, n):
        cost = table[final_mask][i] + matrix[i][0]
        if cost < min_path_cost:
            min_path_cost = cost
            last_city = i

    path = []
    curr_city = last_city
    curr_mask = final_mask

    while curr_city != -1:
        path.append(curr_city)
        prev_city = parent[curr_mask][curr_city]
        curr_mask = curr_mask ^ (1 << curr_city)
        curr_city = prev_city

    path = path[::-1]
    path.append(0)

    return min_path_cost, path


example_matrix = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

try:
    cost, route = solve_lab_9(example_matrix)

    print(f"Минимальная стоимость маршрута: {cost}")
    print(f"Кратчайший маршрут: {route}")
except IndexError:
    print("Ошибка: Матрица должна быть размером NxN")
