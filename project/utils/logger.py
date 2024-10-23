from dataclasses import dataclass

import matplotlib.pyplot as plt


@dataclass
class LogPoint:
    size: int
    tries: int


class Logger:
    def __init__(self) -> None:
        self.log_points = []

    def log(self, size: int, tries: int):
        """Logs a new LogPoint to the logger."""
        self.log_points.append(LogPoint(size=size, tries=tries))

    def draw_log(self) -> None:
        """Draws a linear graph where x is LogPoint.size and y is LogPoint.tries."""
        x_values = [log_point.size for log_point in self.log_points]
        y_values = [log_point.tries for log_point in self.log_points]

        plt.figure(figsize=(10, 5))
        plt.plot(
            x_values,
            y_values,
            marker="o",
            linestyle="-",
            color="b",
            label="Size vs Tries",
        )

        plt.xlabel("Size")
        plt.ylabel("Tries")
        plt.title("Log of Size vs Tries")

        plt.grid(True)
        plt.legend()

        plt.show()
