from abc import abstractmethod, ABC


class Figure(ABC):
    @property
    @abstractmethod
    def area(self) -> float:
        """
        Abstract method to calculate the area of the figure.
        Must be implemented by subclasses.
        """
        pass

    @property
    @abstractmethod
    def perimeter(self) -> float:
        """
        Abstract method to calculate the perimeter of the figure.
        Must be implemented by subclasses.
        """
        pass

    def add_area(self, figure: "Figure") -> float:
        """
        Adds the area of another figure to the current figure's area.

        :param figure: Another figure instance.
        :return: The sum of the areas of the two figures.
        :raises ValueError: If the argument is not an instance of Figure.
        """
        if not isinstance(figure, Figure):
            raise ValueError(f"This argument {figure} should be part of Figure")
        return self.area + figure.area
