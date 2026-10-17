"""Лабораторна 1, завдання 1.1, варіант 3.

Формули з матеріалів:
    y = e^(-bt) * sin(at+b) - sqrt(abs(bt+a))
    s = b * sin(at^2 * cos(2t)) - 1

Використовується лише стандартний модуль math.
"""

import math


# --- Вхідні дані варіанта 3 ---
a = -0.5
b = 1.7
t = 0.44


# --- Перша величина y ---
y = math.exp(-b * t) * math.sin (a*t + b) - math.sqrt(math.abs(b*t + a))


# --- Друга величина m ---
s = b * math.sin(a*(t**2) * math.cos(2t)) - 1


# --- Результат ---
print(f"y = {y:.8f}")
print(f"s = {s:.8f}")
