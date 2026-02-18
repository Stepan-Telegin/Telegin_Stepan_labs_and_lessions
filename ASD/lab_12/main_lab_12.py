def solve_backpack(capacity, weights, values):
    num_items = len(weights)

    table = [[0 for _ in range(capacity + 1)] for _ in range(num_items + 1)]

    for i in range(1, num_items + 1):
        for w in range(capacity + 1):

            current_weight = weights[i - 1]
            current_value = values[i - 1]

            if current_weight <= w:
                val_without = table[i - 1][w]

                val_with = current_value + table[i - 1][w - current_weight]

                table[i][w] = max(val_without, val_with)
            else:
                table[i][w] = table[i - 1][w]

    max_value = table[num_items][capacity]

    selected_items_indices = []
    current_w = capacity

    for i in range(num_items, 0, -1):
        if table[i][current_w] != table[i - 1][current_w]:
            item_index = i - 1
            selected_items_indices.append(item_index)

            current_w -= weights[item_index]

    selected_items_indices.reverse()

    return max_value, selected_items_indices


item_weights = [2, 3, 5, 7]
item_values = [10, 15, 20, 25]
backpack_capacity = 8

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
