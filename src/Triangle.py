import math

from src.Figure import Figure


class Triangle(Figure):
    def __init__(self, a_side: int, b_side: int, c_side: int):
        """
        Initializes a Triangle with the given side lengths.

        :param a_side: Length of side 'a' of the triangle.
        :param b_side: Length of side 'b' of the triangle.
        :param c_side: Length of side 'c' of the triangle.
        :raises ValueError: If any side length is non-positive or if the sides do not form a valid triangle.
        """
        if a_side <= 0 or b_side <= 0 or c_side <= 0:
            raise ValueError("The sides of the triangle must be positive.")
        if not self._is_valid_triangle(a_side, b_side, c_side):
            raise ValueError("The sides do not form a valid triangle.")
        self.a_side = a_side
        self.b_side = b_side
        self.c_side = c_side

    @staticmethod
    def _is_valid_triangle(a: int, b: int, c: int) -> bool:
        """
        Checks if the given sides form a valid triangle.

        :param a: Length of side 'a'.
        :param b: Length of side 'b'.
        :param c: Length of side 'c'.
        :return: True if the sides form a valid triangle, False otherwise.
        """
        return a + b > c and a + c > b and b + c > a

    @property
    def perimeter(self) -> float:
        """
        Calculates and returns the perimeter of the triangle.

        :return: The perimeter of the triangle.
        """
        return self.a_side + self.b_side + self.c_side

    @property
    def area(self) -> float:
        """
        Calculates and returns the area of the triangle using Heron's formula.

        :return: The area of the triangle.
        """
        half_perimeter = self.perimeter / 2
        return math.sqrt(
            half_perimeter
            * (half_perimeter - self.a_side)
            * (half_perimeter - self.b_side)
            * (half_perimeter - self.c_side)
        )
