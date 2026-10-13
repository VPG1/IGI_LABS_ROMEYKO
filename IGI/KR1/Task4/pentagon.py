"""Control work 1: Task 4, Regular pentagon, variant 8.
Version: 1.0. Author: Romeiko Matvey Dmitrievich. Date: 2026-10-13.
Purpose: Calculate, describe and draw a regular pentagon from its side.
"""

import math
from pathlib import Path
from abstract_figure import GeometricFigure
from figure_color import FigureColor


class RegularPentagon(GeometricFigure):
    """Regular pentagon composed with an independently validated color."""
    name = "Правильный пятиугольник"

    def __init__(self, side, color):
        """Create a figure with a finite positive side and a valid color."""
        if isinstance(side, bool):
            raise ValueError("Сторона должна быть положительным числом.")
        self.side = float(side)
        if not math.isfinite(self.side) or self.side <= 0:
            raise ValueError("Сторона должна быть конечным числом больше нуля.")
        if not math.isfinite(self.side * self.side * 1.721):
            raise ValueError("Сторона слишком велика для вычисления площади.")
        self.figure_color = FigureColor(color)

    def calculate_area(self):
        """Return 5*a^2/(4*tan(pi/5)), using the pentagon apothem."""
        return (5 / (4 * math.tan(math.pi / 5))) * self.side ** 2

    def vertices(self):
        """Return five counterclockwise vertices with the first vertex on top."""
        radius = self.side / (2 * math.sin(math.pi / 5))
        return [(radius * math.cos(math.pi / 2 + 2 * math.pi * index / 5),
                 radius * math.sin(math.pi / 2 + 2 * math.pi * index / 5))
                for index in range(5)]

    def describe(self):
        """Format the name, side, color and area using str.format."""
        return "{}: сторона a = {:.4g}, цвет = {}, площадь S = {:.6f}".format(
            self.get_name(), self.side, self.figure_color.color, self.calculate_area())

    def draw(self, label, output_path, show=True):
        """Fill, label, save and optionally display the figure with equal axes."""
        import matplotlib.pyplot as plt
        from matplotlib.patches import Polygon
        output = Path(output_path)
        if output.suffix.lower() not in {".png", ".pdf", ".svg"}:
            raise ValueError("Файл должен иметь расширение png, pdf или svg.")
        points = self.vertices()
        radius = self.side / (2 * math.sin(math.pi / 5))
        figure, axes = plt.subplots(figsize=(7, 7))
        try:
            axes.add_patch(Polygon(points, closed=True,
                                   facecolor=self.figure_color.color,
                                   edgecolor="black", linewidth=1.5))
            for index, (x, y) in enumerate(points, 1):
                axes.annotate("V{}".format(index), (x, y),
                              xytext=(7, 7), textcoords="offset points")
            axes.text(0, -1.10 * radius, label, ha="center", va="center", wrap=True)
            axes.set_xlim(-1.30 * radius, 1.30 * radius)
            axes.set_ylim(-1.30 * radius, 1.30 * radius)
            axes.set_aspect("equal", adjustable="box")
            axes.set_title("{}\na = {:g}, S = {:.6f}".format(
                self.get_name(), self.side, self.calculate_area()))
            axes.set_xlabel("x")
            axes.set_ylabel("y")
            axes.grid(alpha=0.25)
            figure.tight_layout()
            output.parent.mkdir(parents=True, exist_ok=True)
            figure.savefig(output, dpi=180, bbox_inches="tight")
            if show:
                plt.show()
        finally:
            plt.close(figure)
        return output
