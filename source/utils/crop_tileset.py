from PIL import Image
import numpy as np
from source.utils.settings import TILE_SIZE


def crop_tileset():
    img = Image.open("assets/images/tileset.png")
    img_array = np.array(img)
    count = 0
    width, height = img.size
    for row in range(0, height, TILE_SIZE):
        for col in range(0, width, TILE_SIZE):
            array = np.copy(img_array)
            array = array[row:row + TILE_SIZE,
                          col:col + TILE_SIZE]
            cropped_img = Image.fromarray(array)
            cropped_img.save(f"assets/images/graphics/{count}.png")
            count += 1


crop_tileset()
