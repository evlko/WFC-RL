from abc import ABC
from typing import Tuple

import matplotlib
import matplotlib.image as mpimg


class Renderer(ABC):
    @staticmethod
    def load_image(
        image_path: str,
        ax: matplotlib.axes.Axes,
        grid_pos: Tuple[int, int],
        axis: bool = False,
    ) -> None:
        """Load an image and display it in the given axis grid position."""
        if image_path:
            img = mpimg.imread(image_path)
            ax[grid_pos].imshow(img)

        if not axis:
            ax[grid_pos].axis("off")

        ax[grid_pos].set_xticks([])
        ax[grid_pos].set_yticks([])
