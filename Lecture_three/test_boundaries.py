"""Готовий навчальний зразок параметризації та граничних випадків.

Для власної роботи створіть test_student.py з додатковими сценаріями.
Очікування потрібно визначати з контракту, а не викликом brighten.
"""

import pytest

from image_ops import brighten


@pytest.mark.parametrize(
    "p,d,expected",
    [
        pytest.param(100, 20, 120, id="ordinary"),
        pytest.param(250, 20, 255, id="upper_saturation"),
        pytest.param(5, -20, 0, id="lower_saturation"),
        pytest.param(0, 0, 0, id="zero_unchanged"),
        pytest.param(255, 0, 255, id="maximum_unchanged"),
        pytest.param(0, 1, 1, id="step_from_zero"),
        pytest.param(255, -1, 254, id="step_from_maximum"),
    ],
)
def test_brighten_cases(p, d, expected):
    assert brighten(p, d) == expected
