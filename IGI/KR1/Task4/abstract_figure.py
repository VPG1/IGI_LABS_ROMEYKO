"""Control work 1: Task 4, Abstract geometric figure, variant 8.
Version: 1.0. Author: Romeiko Matvey Dmitrievich. Date: 2026-10-13.
Purpose: Declare the shared area interface and class-level figure name.
"""

from abc import ABC, abstractmethod


class GeometricFigure(ABC):
    """Abstract base class for geometric figures."""
    name = "Геометрическая фигура"

    @abstractmethod
    def calculate_area(self):
        """Return the area in square units."""
        raise NotImplementedError

    @classmethod
    def get_name(cls):
        """Return the figure name stored in a class data field."""
        return cls.name
