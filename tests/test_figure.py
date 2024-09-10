import pytest

from src.circle import Circle
from src.rectangle import Rectangle
from src.square import Square
from src.triangle import Triangle


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.parametrize(
    "figure1, figure2, expected_area",
    [
        (Rectangle(3, 5), Square(4), 31),
        (Triangle(3, 5, 6), Circle(4), 57.75)
    ]
)
def test_add_area(figure1, figure2, expected_area):
    result = figure1.add_area(figure2)
    assert round(result, 2) == expected_area, f"Perimeter should be {expected_area}"


@pytest.mark.negative
@pytest.mark.parametrize(
    "invalid_figure",
    [
        "not_a_figure",
        42,
        3.14,
        None,
        [],
        {},
        (3, 4),
        True
    ]
)
def test_add_area_invalid_figure(invalid_figure):
    figure1 = Rectangle(4, 4)

    with pytest.raises(ValueError, match="should be part of Figure"):
        figure1.add_area(invalid_figure)
