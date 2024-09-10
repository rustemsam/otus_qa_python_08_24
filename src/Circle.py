import math

from src.Figure import Figure


class Circle(Figure):
    """
    Initializes a Circle with the given radius.

    :param radius: The radius of the circle.
    :raises ValueError: If the radius is not positive.
    """

    def __init__(self, radius: float):
        if radius <= 0:
            raise ValueError("The radius of the circle must be positive.")
        self.radius = radius

    @property
    def perimeter(self) -> float:
        """
        Calculates and returns the perimeter (circumference) of the circle.

        :return: The perimeter of the circle.
        """
        return 2 * math.pi * self.radius

    @property
    def area(self) -> float:
        """
        Calculates and returns the area of the circle.

        :return: The area of the circle.
        """
        return math.pi * self.radius**2
