"""Лабораторна 1, завдання 1.2, варіант 3.

Табулювання кусочно заданої функції на [-2.5, 2] з кроком 0.5.
Чистий Python: без NumPy, сітка будується через range та індекс i.
"""

import math


# --- Вхідні дані варіанта 3 ---
left = -2.5
right = 2.0
h = 0.5

a = 5
b = 3


# --- Перевірка сітки ---
if h <= 0:
    raise ValueError("Крок h має бути додатним.")
if right < left:
    raise ValueError("Права межа має бути не меншою за ліву.")

steps_real = (right - left) / h
steps = round(steps_real)

if not math.isclose(steps_real, steps, rel_tol=0.0, abs_tol=1e-12):
    raise ValueError("Довжина відрізка має ділитися на h на ціле число кроків.")


# --- Кусочно задана функція ---
def piecewise_value(x):
    """Повертає номер гілки та значення функції для x у [-2.5, 2]."""
    if not left <= x <= right:
        raise ValueError("Аргумент поза областю [-2.5, 2].")

    if abs(x) < a/b:
        return 1, math.sin(abs(a*x + b))

    return 2, math.cos(abs(a*x - b))


# --- Таблиця ---
print(" i |   x | гілка |            y")
print("---|-----|-------|-------------")

for i in range(steps + 1):
    x = left + i * h
    branch, y = piecewise_value(x)
    print(f"{i:2d} | {x:3.1f} | {branch:5d} | {y:11.7f}")


# --- Структурні перевірки зі слайда ---
assert steps + 1 == 10
assert piecewise_value(0.0)[0] == 1
assert piecewise_value(0.5)[0] == 1
assert piecewise_value(2.0)[0] == 2
