import math


def solve_bin_packing_backtracking(items, bin_capacity):
    sorted_items = sorted(items, reverse=True)

    min_bins_possible = math.ceil(sum(sorted_items) / bin_capacity)

    max_bins_possible = len(sorted_items)

    for number_of_bins in range(min_bins_possible, max_bins_possible + 1):
        bins = [0] * number_of_bins

        if can_distribute_items(sorted_items, bins, bin_capacity, 0):
            return number_of_bins

    return max_bins_possible


def can_distribute_items(items, bins, capacity, item_index):
    if item_index == len(items):
        return True

    current_item_weight = items[item_index]

    for i in range(len(bins)):

        if bins[i] + current_item_weight <= capacity:

            bins[i] += current_item_weight

            if can_distribute_items(items, bins, capacity, item_index + 1):
                return True

            bins[i] -= current_item_weight

        if bins[i] == 0:
            break

    return False


if __name__ == "__main__":
    items_to_pack = [2, 5, 4, 7, 1, 3, 8]
    capacity_of_one_bin = 10

    if max(items_to_pack) > capacity_of_one_bin:
        raise ValueError("The things are too big")

    print(f"Items: {items_to_pack}")
    print(f"Bin Capacity: {capacity_of_one_bin}")

    min_bins = solve_bin_packing_backtracking(items_to_pack, capacity_of_one_bin)

    print(f"Minimum bins required: {min_bins}")
