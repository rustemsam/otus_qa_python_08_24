from src.figure import Figure


class Rectangle(Figure):
    """
    Initializes a Rectangle with given side lengths.

    :param a_side: The length of side 'a' of the rectangle.
    :param b_side: The length of side 'b' of the rectangle.
    :raises ValueError: If either side length is not positive.
    """

    def __init__(self, a_side: float, b_side: float):
        if a_side <= 0 or b_side <= 0:
            raise ValueError("The side for the side of rectangle should be positive.")
        self.a_side = a_side
        self.b_side = b_side

    @property
    def perimeter(self) -> float:
        """
        Calculates and returns the perimeter of the rectangle.

        :return: The perimeter of the rectangle.
        """
        return (self.a_side + self.b_side) * 2

    @property
    def area(self) -> float:
        """
        Calculates and returns the area of the rectangle.

        :return: The area of the rectangle.
        """
        return self.a_side * self.b_side
