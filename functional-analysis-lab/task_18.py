import numpy as np
import matplotlib.pyplot as plt

eps = 0.01
k = 0.75
rho_01 = 3.0

N_apr = int(np.log(eps * (1 - k) / rho_01) / np.log(k)) + 1
print(f"N_apr = {N_apr}")

t = np.linspace(-2, 2, 400)
x = np.zeros_like(t)  # Начальное приближение 0 на всей сетке

# Контрольные 5 точек
t_points = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
x_points = np.zeros_like(t_points)

for _ in range(N_apr):
    x = 0.75 * np.arctan(np.abs(x)) - t - 1
    x_points = 0.75 * np.arctan(np.abs(x_points)) - t_points - 1

# Вывод в консоль
print(f"\nЗначения решения x(t) после {N_apr} итераций:")
for tp, xp in zip(t_points, x_points): # zip - соединяет два списка попарно
    print(f"  t = {tp:4.1f}   =>   x(t) ~ {xp:8.4f}")

# Построение графика
plt.figure(figsize=(8, 5))
plt.plot(t, x, 'b-', linewidth=2) # b- означает синяя сплошная линия
plt.scatter(t_points, x_points, color='red', zorder=5)

plt.title(r'Решение уравнения', fontsize=12)
plt.xlabel('t', fontsize=11)
plt.ylabel('x(t)', fontsize=11)
plt.axhline(0, color='black', linewidth=0.8, linestyle=':')
plt.axvline(0, color='black', linewidth=0.8, linestyle=':')
plt.grid(True, linestyle='--', alpha=0.6) # включает фоновую сетку
plt.show()
