"""Перший приклад зі слайда: Arrange, Act, Assert."""

from image_ops import brighten


def test_brighten_increases_brightness():
    # Arrange: незалежно визначені початкові дані.
    pixel = 100
    delta = 20

    # Act: один виклик перевірюваної дії.
    result = brighten(pixel, delta)

    # Assert: очікування походить із контракту.
    assert result == 120
