import matplotlib.pyplot as plt

from project.visualization.renderer import Renderer
from project.wfc.grid import Grid


class GridRenderer(Renderer):
    offset = 0.15

    def draw(self, grid: Grid, title: str = None, show_borders: bool = False) -> None:
        """Draw the grid using images for the patterns."""
        fig, ax = plt.subplots(
            grid.height,
            grid.width,
            figsize=(grid.width, grid.height),
        )

        if title:
            fig.suptitle(title)

        for x in range(grid.width):
            for y in range(grid.height):
                pattern = grid.grid[x, y]
                if pattern:
                    self.load_image(pattern.image_path, ax, (x, y), show_borders)

        plt.subplots_adjust(
            left=self.offset,
            right=1 - self.offset,
            bottom=self.offset,
            top=1 - self.offset,
            hspace=0,
            wspace=0,
        )
        plt.show()


grid_renderer = GridRenderer()
