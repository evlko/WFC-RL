import matplotlib.pyplot as plt

from project.utils.utils import Utils
from project.visualization.renderer import Renderer
from project.wfc.grid import Grid


class GridRenderer(Renderer):
    offset = 0.15

    def draw(
        self,
        grid: Grid,
        title: str = None,
        show_borders: bool = False,
        seed: int | None = 42,
    ) -> None:
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
                meta_pattern = grid.grid[x, y]
                image = None
                if meta_pattern:
                    custom_seed = (lambda s: s + x * 100 + y + y**2 if s else None)(
                        seed
                    )
                    pattern = Utils.weighted_choice(
                        meta_pattern.patterns, seed=custom_seed
                    )
                    image = pattern.image_path
                self.load_image(image, ax, (x, y), show_borders)

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
