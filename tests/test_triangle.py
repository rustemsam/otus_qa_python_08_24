import pytest

from src.triangle import Triangle


@pytest.fixture
def triangle():
    def _triangle(a_side, b_side, c_side):
        return Triangle(a_side, b_side, c_side)

    return _triangle


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.parametrize(
    "a_side, b_side, c_side, expected_perimeter",
    [
        (5, 5, 5, 15),
        (5.1, 5.5, 5.9, 16.5),
    ]
)
def test_triangle_perimeter(triangle, a_side, b_side, c_side, expected_perimeter):
    tri = triangle(a_side, b_side, c_side)
    assert tri.perimeter == expected_perimeter, f"Perimeter should be {expected_perimeter}, but got {tri.perimeter}"


@pytest.mark.positive
@pytest.mark.parametrize(
    "a_side, b_side, c_side, expected_area",
    [
        (5, 5, 5, 10.825317547305483),
        (5.1, 5.5, 5.9, 12.959329409734131),
    ]
)
def test_triangle_area(triangle, a_side, b_side, c_side, expected_area):
    tri = triangle(a_side, b_side, c_side)
    assert tri.area == expected_area, f"Area should be {expected_area}, but got {tri.area}"


@pytest.mark.negative
@pytest.mark.parametrize(
    "a_side, b_side, c_side",
    [
        (5, 5, 0),
        (-1, 5, 5),
        (4, 0, 5)
    ]
)
def test_triangle_invalid_sides(triangle, a_side, b_side,c_side):
    with pytest.raises(ValueError, match="The sides of the triangle must be positive."):
        triangle(a_side, b_side, c_side)


@pytest.mark.negative
@pytest.mark.parametrize(
    "a_side, b_side, c_side",
    [
        (5, 5, 10),
        (6, 13, 6),
        (14, 7, 7)
    ]
)
def test_triangle_invalid_triangle(triangle, a_side, b_side,c_side):
    with pytest.raises(ValueError, match="The sides do not form a valid triangle."):
        triangle(a_side, b_side, c_side)
