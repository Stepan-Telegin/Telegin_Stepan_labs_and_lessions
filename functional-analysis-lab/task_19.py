import math

eps = 1e-4
i_exact = 5 / 24
k = 1 / 3  # Коэффициент сжатия при lambda = 1
rho_01 = 1.0

n_apr = int(math.log(eps * (1 - k) / rho_01) / math.log(k)) + 1

i = 0.0  # коэффициент i_0 = 0

print(f"N_apr = {n_apr}")
print(f"{'Шаг n':<6} | {'Приближение I_n':<17} | {'Погрешность':<12}")

for n in range(1, n_apr + 1):
    i_prev = i
    i = i_prev / 5 + 1 / 6  # формула из решения

    # Погрешность в C([0; 1]): sup(|i - i*| * t^2) = |i - i*|
    error = abs(i - i_exact)
    print(f"{n:<6} | {i:<17.6f} | {error:<12.2e}")

print(f"\nИтог: на шаге {n_apr} погрешность {error:.2e} < {eps}")
print(f"Приближенное решение: x(t) = {i:.6f} * t^2 + t^3")
