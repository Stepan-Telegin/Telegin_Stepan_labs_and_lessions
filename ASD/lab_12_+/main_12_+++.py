import random


def build_multiple_items(weights, capacity):
    by_w = {}
    for i, w in enumerate(weights):
        if w <= 0:
            raise ValueError("Веса должны быть положительными")
        if w <= capacity:
            if w not in by_w:
                by_w[w] = []
            by_w[w].append(i)

    multiple = []
    for w, idxs in by_w.items():
        limit = capacity // w
        if limit <= 0:
            continue

        if len(idxs) > limit:
            idxs = idxs[:limit]

        m = len(idxs)

        pos = 0
        k = 1
        while m > 0:
            take = min(k, m)
            multiple.append((w * take, take, idxs[pos : pos + take]))
            pos += take
            m -= take
            k *= 2

    return multiple


def solve_backpack(capacity: int, weights, values=None):
    if capacity < 0:
        return 0, []
    if capacity == 0:
        return 0, []
    if sum(weights) < capacity:
        return 0, []

    multiple_items = build_multiple_items(weights, capacity)

    NEG = -(10**9)
    costs_of_amounts = [NEG] * (capacity + 1)
    costs_of_amounts[0] = 0

    parent_id = [-1] * (capacity + 1)
    parent_prev = [-1] * (capacity + 1)

    for id, (mw, cnt, _) in enumerate(multiple_items):
        for s in range(capacity, mw - 1, -1):
            prev = costs_of_amounts[s - mw]
            if prev == NEG:
                continue
            cand = prev + cnt
            if cand > costs_of_amounts[s]:
                costs_of_amounts[s] = cand
                parent_id[s] = id
                parent_prev[s] = s - mw

    if costs_of_amounts[capacity] == NEG:
        return 0, []

    selected = []
    s = capacity
    while s > 0:
        id = parent_id[s]
        if id < 0:
            return 0, []
        mw, cnt, orig_list = multiple_items[id]
        selected.extend(orig_list)
        s = parent_prev[s]

    selected.reverse()
    return costs_of_amounts[capacity], selected


random.seed(111)

n = 100000
sum_limit = 200000

item_weights = [1] * n
remaining = sum_limit - n

for i in range(n):
    if remaining <= 0:
        break
    add = random.randint(0, min(100000 - 1, remaining))
    item_weights[i] += add
    remaining -= add

item_values = [1] * n
backpack_capacity = 100000

max_val, taken_items = solve_backpack(backpack_capacity, item_weights, item_values)

print(f"Вместимость рюкзака: {backpack_capacity}")
print(f"Максимальная ценность: {max_val}")
print(f"Индексы взятых предметов: {taken_items}")

print("Состав рюкзака:")
total_check_weight = 0
for idx in taken_items:
    print(f"- Предмет {idx}: Вес = {item_weights[idx]}, Ценность = {item_values[idx]}")
    total_check_weight += item_weights[idx]
print(f"Итоговый вес: {total_check_weight}")
