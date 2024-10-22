import matplotlib.pyplot as plt

from project.wfc.pattern import Pattern
from project.visualization.renderer import Renderer


class PatternRenderer(Renderer):
    def draw(self, pattern: Pattern) -> None:
        """Draw the pattern with rules."""
        up_neighbors, right_neighbors, down_neighbors, left_neighbors = (
            pattern.rules.get_allowed_neighbors()
        )

        max_horizontal = max(len(left_neighbors), len(right_neighbors), 1)
        max_vertical = max(len(up_neighbors), len(down_neighbors), 1)

        grid_height = max_vertical * 2 + 1
        grid_width = max_horizontal * 2 + 1

        fig, ax = plt.subplots(
            grid_height, grid_width, figsize=(grid_width, grid_height)
        )

        center_pos = (max_vertical, max_horizontal)
        self.load_image(pattern.image_path, ax, center_pos)

        if up_neighbors:
            for i, neighbor in enumerate(up_neighbors):
                self.load_image(
                    neighbor.image_path, ax, (max_vertical - 1 - i, max_horizontal)
                )

        if down_neighbors:
            for i, neighbor in enumerate(down_neighbors):
                self.load_image(
                    neighbor.image_path, ax, (max_vertical + 1 + i, max_horizontal)
                )

        if left_neighbors:
            for i, neighbor in enumerate(left_neighbors):
                self.load_image(
                    neighbor.image_path, ax, (max_vertical, max_horizontal - 1 - i)
                )

        if right_neighbors:
            for i, neighbor in enumerate(right_neighbors):
                self.load_image(
                    neighbor.image_path, ax, (max_vertical, max_horizontal + 1 + i)
                )

        for i in range(grid_height):
            for j in range(grid_width):
                ax[i, j].axis("off")

        plt.subplots_adjust(wspace=0.1, hspace=0.1)
        plt.show()


pattern_renderer = PatternRenderer()
