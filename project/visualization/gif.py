import glob

from PIL import Image


def create_gif(output_path: str, image_folder: str, duration: int = 100) -> None:
    """Create a GIF from PNG images."""
    images = []
    for filename in sorted(glob.glob(f"{image_folder}/*.png")):
        img = Image.open(filename)
        images.append(img)

    images[0].save(
        output_path, save_all=True, append_images=images[1:], duration=duration, loop=0
    )
