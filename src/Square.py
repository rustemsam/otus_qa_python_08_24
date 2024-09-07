from Rectangle import Rectangle


class Square(Rectangle):
    """
    Initializes a Square with a given side length.

    :param a_side: The length of the side of the square.
    :raises ValueError: If the side length is not positive.
    """

    def __init__(self, a_side: int):
        if a_side <= 0:
            raise ValueError("The side for the side of square should be positive")
        super().__init__(a_side, a_side)
