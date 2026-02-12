def solve_max_subarray():
    try:
        path = "C:/Users/user/Documents/GitHub/Telegin_Stepan_labs_and_lessions/ASD/lab_7/input.txt"
        with open(path, "r", encoding="utf-8") as f:
            nums = [float(x) for x in f.read().split()]
    except FileNotFoundError:
        print("Файл input.txt не найден.")
        return
    except ValueError:
        print("Ошибка: файл должен содержать только числа.")
        return

    if not nums:
        print("Файл пуст.")
        return

    current_sum = nums[0]
    temp_start = 0
    max_sum = nums[0]
    best_start = 0
    best_end = 0

    for i in range(1, len(nums)):
        x = nums[i]

        if x > current_sum + x:
            current_sum = x
            temp_start = i
        else:
            current_sum += x

        if current_sum > max_sum:
            max_sum = current_sum
            best_start = temp_start
            best_end = i

    best_subarray = nums[best_start : best_end + 1]

    print(f"Максимальная сумма: {max_sum}")
    print(f"Искомый подмассив: {best_subarray}")


if __name__ == "__main__":
    solve_max_subarray()
