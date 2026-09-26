import numpy as np
import matplotlib.pyplot as plt

# 1. Задаем сетку точек по t на отрезке [-2; 2]
t = np.linspace(-2, 2, 400)
x = np.zeros_like(t)  # Начальное приближение x_0(t) = 0

# Контрольные точки для вывода в консоль
t_points = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
x_points = np.zeros_like(t_points)

# 2. Априорное число шагов посчитано на бумаге: N_apr = 25
N_apr = 25

# 3. Метод простых итераций: x_n(t) = 0.75 * arctg(|x_{n-1}(t)|) - t - 1
for _ in range(N_apr):
    x = 0.75 * np.arctan(np.abs(x)) - t - 1
    x_points = 0.75 * np.arctan(np.abs(x_points)) - t_points - 1

# 4. Вывод значений в консоль
print(f"Значения решения x(t) после {N_apr} итераций (точность eps = 0.01):")
print("-" * 45)
for tp, xp in zip(t_points, x_points):
    print(f"  t = {tp:4.1f}   --->   x(t) ≈ {xp:8.4f}")
print("-" * 45)

# 5. Построение графика решения
plt.figure(figsize=(8, 5))
plt.plot(t, x, 'b-', linewidth=2, label=r'Приближение $x_{25}(t)$')
plt.scatter(t_points, x_points, color='red', zorder=5, label='Контрольные точки')

plt.title(r'Решение уравнения $\frac{3}{4}\operatorname{arctg}|x(t)| - x(t) = t + 1$', fontsize=12)
plt.xlabel('t', fontsize=11)
plt.ylabel('x(t)', fontsize=11)
plt.axhline(0, color='black', linewidth=0.8, linestyle=':')
plt.axvline(0, color='black', linewidth=0.8, linestyle=':')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=11)
plt.show()
