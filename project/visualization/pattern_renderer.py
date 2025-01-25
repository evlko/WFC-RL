import matplotlib.pyplot as plt

from project.visualization.renderer import Renderer
from project.wfc.pattern import MetaPattern


class PatternRenderer(Renderer):
    def draw(
        self, meta_pattern: MetaPattern, pattern_idx: int = 0, title: str = None
    ) -> None:
        """Draw the pattern with its neighboring rules using a dynamic grid layout."""
        up_neighbors, right_neighbors, down_neighbors, left_neighbors = (
            meta_pattern.rules.get_allowed_neighbors()
        )

        max_horizontal = max(len(left_neighbors), len(right_neighbors), 1)
        max_vertical = max(len(up_neighbors), len(down_neighbors), 1)

        grid_height = max_vertical * 2 + 1
        grid_width = max_horizontal * 2 + 1

        fig, ax = plt.subplots(
            grid_height, grid_width, figsize=(grid_width, grid_height)
        )

        if title:
            fig.suptitle(title)

        self.render_cell(
            image_path=meta_pattern.patterns[pattern_idx].image_path,
            ax=ax[max_vertical, max_horizontal],
        )

        if up_neighbors:
            for i, neighbor in enumerate(up_neighbors):
                self.render_cell(
                    image_path=neighbor.patterns[0].image_path,
                    ax=ax[max_vertical - 1 - i, max_horizontal],
                )

        if down_neighbors:
            for i, neighbor in enumerate(down_neighbors):
                self.render_cell(
                    image_path=neighbor.patterns[0].image_path,
                    ax=ax[max_vertical + 1 + i, max_horizontal],
                )

        if left_neighbors:
            for i, neighbor in enumerate(left_neighbors):
                self.render_cell(
                    image_path=neighbor.patterns[0].image_path,
                    ax=ax[max_vertical, max_horizontal - 1 - i],
                )

        if right_neighbors:
            for i, neighbor in enumerate(right_neighbors):
                self.render_cell(
                    image_path=neighbor.patterns[0].image_path,
                    ax=ax[max_vertical, max_horizontal + 1 + i],
                )

        for i in range(grid_height):
            for j in range(grid_width):
                ax[i, j].axis("off")

        plt.subplots_adjust(wspace=0.1, hspace=0.1)
        plt.show()


pattern_renderer = PatternRenderer()
