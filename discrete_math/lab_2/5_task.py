def print_grid(title, matrix, W, H):

    print(f"\n{title}")
    
    if isinstance(matrix[0][0], list):
        max_val = matrix[H][W][0] + matrix[H][W][1]
    else:
        max_val = matrix[H][W]
        
    col_width = len(str(max_val)) + 2
    
    for y in range(H, -1, -1):
        row_str = f"y={y:<2} |"
        
        for x in range(W + 1):
            if isinstance(matrix[y][x], list):
                val = matrix[y][x][0] + matrix[y][x][1]
            else:
                val = matrix[y][x]
            
            row_str += f"{val:>{col_width}}"
            
        print(row_str)
    
    print("      " + "-" * ((W + 1) * col_width))
    x_axis = "      "
    for x in range(W + 1):
        x_axis += f"{x:>{col_width}}"
    print(x_axis)


def solve_task_5():
    W = 6 # 22
    H = 4 # 18

    dp1 = [[0 for _ in range(W + 1)] for _ in range(H + 1)]
    dp1[0][0] = 1

    for y in range(H + 1):
        for x in range(W + 1):
            if x > 0: dp1[y][x] += dp1[y][x - 1]
            if y > 0: dp1[y][x] += dp1[y - 1][x]

    print_grid("ЧАСТЬ 1: Все пути", dp1, W, H)
    print(f"Ответ (Часть 1): {dp1[H][W]}")

    dp2 = [[[0, 0] for _ in range(W + 1)] for _ in range(H + 1)]
    
    dp2[0][0][0] = 1 

    for y in range(H + 1):
        for x in range(W + 1):
            if x == 0 and y == 0: continue

            if x > 0:
                dp2[y][x][0] = dp2[y][x - 1][0] + dp2[y][x - 1][1]

            if y > 0:
                dp2[y][x][1] = dp2[y - 1][x][0]

    print_grid("ЧАСТЬ 2: Ограничение (нет 2 верт. подряд)", dp2, W, H)
    
    ans2 = dp2[H][W][0] + dp2[H][W][1]
    print(f"Ответ (Часть 2): {ans2}")

if __name__ == "__main__":
    solve_task_5()