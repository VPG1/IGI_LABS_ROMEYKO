"""Control work 1: Task 4, Figure color, variant 8.
Version: 1.0. Author: Romeiko Matvey Dmitrievich. Date: 2026-10-13.
Purpose: Encapsulate and validate colors using a property.
"""

from matplotlib.colors import is_color_like


class FigureColor:
    """Store a valid, visible Matplotlib color."""

    def __init__(self, color):
        """Validate the initial color through the property setter."""
        self.color = color

    @property
    def color(self):
        """Return the selected color."""
        return self._color

    @color.setter
    def color(self, value):
        """Accept a named color or hex code and reject invalid/empty colors."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Цвет не должен быть пустым.")
        value = value.strip()
        if value.lower() == "none" or not is_color_like(value):
            raise ValueError("Цвет должен быть например blue, red или #23A6C8.")
        self._color = value
