from abc import ABC

import matplotlib
import matplotlib.image as mpimg


class Renderer(ABC):
    @staticmethod
    def _render_image(
        image_path: str,
        ax: matplotlib.axes.Axes,
    ) -> None:
        """Load an image and display it in the given axis grid position."""
        if image_path:
            img = mpimg.imread(image_path)
            ax.imshow(img)

    @staticmethod
    def _render_text(
        text: str,
        text_color: str,
        ax: matplotlib.axes.Axes,
    ) -> None:
        ax.text(0.5, 0.5, text, fontsize=12, ha="center", va="center", color=text_color)

    @staticmethod
    def add_background(
        color: str,
        ax: matplotlib.axes.Axes,
    ) -> None:
        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()
        rect = matplotlib.patches.Rectangle(
            (x_min, y_min),
            x_max - x_min,
            y_max - y_min,
            color=color,
            zorder=-1,
        )
        ax.add_patch(rect)

    def render_cell(
        self,
        image_path: str,
        ax: matplotlib.axes.Axes,
        axis: bool = False,
        text: str | None = None,
        text_color: str = "black",
        background_color: str | None = None,
    ):
        if background_color:
            self.add_background(color=background_color, ax=ax)

        if image_path:
            self._render_image(image_path=image_path, ax=ax)
        elif text:
            self._render_text(text=text, text_color=text_color, ax=ax)

        if not axis:
            ax.axis("off")

        ax.set_xticks([])
        ax.set_yticks([])
