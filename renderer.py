import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class Renderer:
    @staticmethod
    def draw(grid):
        """Draw the grid using images for the patterns."""
        fig, ax = plt.subplots(
            grid.height,
            grid.width,
            figsize=(grid.width, grid.height),
        )
        for x in range(grid.width):
            for y in range(grid.height):
                pattern = grid.grid[x, y]
                if pattern:
                    img = mpimg.imread(pattern.image_path)
                    ax[y, x].imshow(img)  
                ax[y, x].axis("on") 

        plt.subplots_adjust(wspace=0, hspace=0)
        plt.show()
