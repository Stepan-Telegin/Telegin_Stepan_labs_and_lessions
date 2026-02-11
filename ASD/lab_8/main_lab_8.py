def count_change_ways(coins, target_sum):
    arr = [0] * (target_sum + 1)

    arr[0] = 1

    for coin in coins:
        for current_amount in range(coin, target_sum + 1):

            previous_amount = current_amount - coin
            arr[current_amount] += arr[previous_amount]

    return arr[target_sum]


if __name__ == "__main__":
    coin_denominations = [1, 2, 5, 10, 15, 50, 100, 200, 1000, 2000, 5000]

    print(f"Имеющиеся номиналы монет: {coin_denominations}")

    try:
        user_input = input("Введите сумму для сдачи (целое число): ")
        amount = int(user_input)

        if amount < 0:
            print("Сумма не может быть отрицательной.")
        else:
            ways = count_change_ways(coin_denominations, amount)

            print(f"Количество способов набрать сумму {amount}: {ways}")

    except ValueError:
        print("Ошибка: Введите корректное целое число.")
