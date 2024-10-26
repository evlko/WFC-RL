import matplotlib.pyplot as plt

from project import config
from project.utils.utils import Utils
from project.visualization.renderer import Renderer
from project.wfc.grid import Grid, Point


class GridRenderer(Renderer):
    offset = 0.15

    def draw(
        self,
        grid: Grid,
        title: str = None,
        show_borders: bool = False,
        seed: int | None = 42,
        show: bool = True,
        filename: str | None = None,
        show_entropy_on_empty: bool = True,
    ) -> None:
        """Draw the grid using images for the patterns."""
        fig, ax = plt.subplots(
            grid.height,
            grid.width,
            figsize=(grid.width, grid.height),
        )

        if title:
            fig.suptitle(title)

        for x in range(grid.height):
            for y in range(grid.width):
                meta_pattern = grid.grid[x, y]
                cell_entropy = None
                if show_entropy_on_empty:
                    cell_entropy = grid.entropy[x, y]
                image = None
                if meta_pattern:
                    custom_seed = (lambda s: s + x * 100 + y + y**2 if s else None)(
                        seed
                    )
                    pattern = Utils.weighted_choice(
                        meta_pattern.patterns, seed=custom_seed
                    )
                    image = pattern.image_path
                self.render_cell(
                    image_path=image,
                    text=cell_entropy,
                    ax=ax,
                    p=Point(x, y),
                    axis=show_borders,
                )

        plt.subplots_adjust(
            left=self.offset,
            right=1 - self.offset,
            bottom=self.offset,
            top=1 - self.offset,
            hspace=0,
            wspace=0,
        )

        if show:
            plt.show()
        if filename:
            plt.savefig(
                f"{config.IMAGES_PATH}{filename}.png", bbox_inches="tight", pad_inches=0
            )
        plt.close()


grid_renderer = GridRenderer()
