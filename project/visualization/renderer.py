from abc import ABC

import matplotlib
import matplotlib.image as mpimg

from project.wfc.grid import Point


class Renderer(ABC):
    @staticmethod
    def _render_image(
        image_path: str,
        ax: matplotlib.axes.Axes,
        p: Point,
    ) -> None:
        """Load an image and display it in the given axis grid position."""
        if image_path:
            img = mpimg.imread(image_path)
            ax[p.x, p.y].imshow(img)

    @staticmethod
    def _render_text(
        text: str,
        ax: matplotlib.axes.Axes,
        p: Point,
    ) -> None:
        ax[p.x, p.y].text(0.5, 0.5, text, fontsize=12, ha="center", va="center")

    def render_cell(
        self,
        image_path: str,
        ax: matplotlib.axes.Axes,
        p: Point,
        axis: bool = False,
        text: str | None = None,
    ):
        if image_path:
            self._render_image(image_path=image_path, ax=ax, p=p)
        elif text:
            self._render_text(text=text, ax=ax, p=p)

        if not axis:
            ax[p.x, p.y].axis("off")

        ax[p.x, p.y].set_xticks([])
        ax[p.x, p.y].set_yticks([])
