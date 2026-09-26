import numpy as np

# 1. Задаем исходную матрицу A и вектор b
A = np.array([
    [-7.0, 2.0, -3.0, 4.0],
    [2.0, 3.0, -1.0, 2.0],
    [-1.0, 1.0, 1.0, -1.0],
    [1.0, 0.0, -2.0, -3.0]
])

b = np.array([-19.0, -13.0, -5.0, -6.0])

# 2. Формируем симметричную систему: S = A^T * A, f = A^T * b
S = A.T @ A
f = A.T @ b

print("--- Матрица S = A^T * A ---")
print(S)
print("\n--- Вектор f = A^T * b ---")
print(f)

# 3. Находим спектр (собственные значения) матрицы S
# eigvalsh возвращает собственные значения вещественной симметричной матрицы в порядке возрастания
lambdas = np.linalg.eigvalsh(S)
lambda_min = lambdas[0]
lambda_max = lambdas[-1]

print("\n--- Спектр (собственные значения) матрицы A^T * A ---")
for i, val in enumerate(lambdas, 1):
    print(f"lambda_{i} = {val:.6f}")

# 4. Коэффициент сжатия k (конспект, стр. 21)
k = 1.0 - (lambda_min / lambda_max)
print(f"\nКоэффициент сжатия k = 1 - lambda_min / lambda_max = {k:.6f}")

# 5. Матрица перехода B и свободный член c: x = Bx + c
E = np.eye(4)
B = E - (1.0 / lambda_max) * S
c = (1.0 / lambda_max) * f


# 6. Функция для проведения итераций до точности eps
def solve_iterations(eps):
    x_prev = np.zeros(4)  # x_0 = (0, 0, 0, 0)
    x_cur = B @ x_prev + c  # x_1

    # Расчет априорной оценки N_apr
    rho_0_1 = np.linalg.norm(x_cur - x_prev)
    N_apr = int(np.floor(np.log(eps * (1.0 - k) / rho_0_1) / np.log(k))) + 1

    step = 1
    # Апостериорный критерий останова: k / (1 - k) * ||x_n - x_{n-1}|| <= eps
    factor = k / (1.0 - k)

    while factor * np.linalg.norm(x_cur - x_prev) > eps:
        x_prev = x_cur
        x_cur = B @ x_prev + c
        step += 1

    delta = factor * np.linalg.norm(x_cur - x_prev)
    return x_cur, step, N_apr, delta


# 7. Вычисляем приближения для двух требуемых точностей
for eps in [1e-2, 1e-4]:
    sol, steps, N_apr, delta = solve_iterations(eps)
    print(f"\n================ Результаты для eps = {eps} ================")
    print(f"Априорная оценка числа шагов N_apr : {N_apr}")
    print(f"Фактически сделано итераций        : {steps}")
    print(f"Апостериорная погрешность Delta     : {delta:.8f}")
    print(
        f"Приближенное решение x:\n  x1 = {sol[0]:.6f}\n  x2 = {sol[1]:.6f}\n  x3 = {sol[2]:.6f}\n  x4 = {sol[3]:.6f}")

# 8. Точное решение для проверки
x_exact = np.linalg.solve(A, b)
print(f"\n--- Точное решение (lsolve / Gauss) ---")
print(f"  x* = {x_exact}")
