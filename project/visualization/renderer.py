from abc import ABC

import matplotlib.image as mpimg


class Renderer(ABC):
    @staticmethod
    def load_image(image_path, ax, grid_pos, axis: bool = False) -> None:
        img = mpimg.imread(image_path)
        ax[grid_pos].imshow(img)
        if axis == False:
            ax[grid_pos].axis("off")
        ax[grid_pos].set_xticks([])
        ax[grid_pos].set_yticks([])
