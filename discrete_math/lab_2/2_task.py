def task_2():

    x_sequence = [2, 4, 5]
    
    target_index = 20
    a=-2
    b=9
    c=18
    d=7
    
    for i in range(3, target_index + 1):

        val_n_plus_2 = x_sequence[i-1]
        val_n_plus_1 = x_sequence[i-2]
        val_n        = x_sequence[i-3]
        
        next_val = a * val_n_plus_2 + b * val_n_plus_1 + c * val_n + d
        x_sequence.append(next_val)

        print(f"x_{i} = {next_val}")
        
    result = x_sequence[target_index]
    
    n = target_index
    term1 = (27 / 20) * (3 ** n)
    term2 = (17 / 8)  * ((-3) ** n)
    term3 = (46 / 15) * ((-2) ** n)
    term4 = 7 / 24
    
    result_formula = term1 - term2 + term3 - term4

    print(f"Проверка для n = {target_index}")
    print(f"Результат рекурсии: {result}")
    print(f"Результат формулы:  {result_formula:.4f}")
    
    diff = result - round(result_formula)
    
    print(f"Разница: {diff}")
    if diff == 0:
        print("ВЫВОД: Формула выведена верно!")
    else:
        print("ВЫВОД: Ошибка в формуле.")

if __name__ == "__main__":
    task_2()