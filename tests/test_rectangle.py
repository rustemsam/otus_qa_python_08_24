import pytest

from src.rectangle import Rectangle


@pytest.fixture
def rectangle():
    def _rectangle(a_side, b_side):
        return Rectangle(a_side, b_side)

    return _rectangle


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.parametrize(
    "a_side, b_side, expected_perimeter",
    [
        (5, 5, 20),
        (5.1, 5.5, 21.2),
    ]
)
def test_rectangle_perimeter(rectangle, a_side, b_side, expected_perimeter):
    c = rectangle(a_side, b_side)
    assert round(c.perimeter, 2) == expected_perimeter, f"Perimeter should be {expected_perimeter}"


@pytest.mark.positive
@pytest.mark.parametrize(
    "a_side, b_side, expected_area",
    [
        (5, 5, 25),
        (3.0, 2.5, 7.5),
    ]
)
def test_rectangle_area(rectangle, a_side, b_side, expected_area):
    c = rectangle(a_side, b_side)
    assert round(c.area, 2) == expected_area, f"Area should be {expected_area}"


@pytest.mark.negative
@pytest.mark.parametrize(
    "a_side, b_side",
    [
        (5, 0),
        (0, 4),
        (4, -1),
        (-4, 30),
    ]
)
def test_rectangle_invalid_sides(rectangle, a_side, b_side):
    with pytest.raises(ValueError, match="The side for the side of rectangle should be positive"):
        rectangle(a_side, b_side)
