import pytest

from src.rectangle import Rectangle
from src.square import Square


@pytest.fixture
def square():
    def _square(a_side):
        return Square(a_side)

    return _square


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.parametrize(
    "a_side, expected_perimeter",
    [
        (10, 40),
        (1.1, 4.4),
    ],
)
def test_square_perimeter(square, a_side, expected_perimeter):
    s = square(a_side)
    assert (
        round(s.perimeter, 2) == expected_perimeter
    ), f"Perimeter should be {expected_perimeter}"


@pytest.mark.positive
@pytest.mark.parametrize(
    "a_side, expected_area",
    [
        (4, 16),
        (9.5, 90.25),
    ],
)
def test_square_area(square, a_side, expected_area):
    c = square(a_side)
    assert round(c.area, 2) == expected_area, f"Area should be {expected_area}"


@pytest.mark.negative
@pytest.mark.parametrize("a_side", [0, -1])
def test_square_invalid_side(square, a_side):
    with pytest.raises(
        ValueError, match="The side for the side of square should be positive."
    ):
        square(a_side)
