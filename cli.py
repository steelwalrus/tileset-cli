import cv2
import numpy as np
import glob
import click
from math import ceil, sqrt
from helper import Helper


@click.command()
@click.option('--path', required=True, help="Input directory of tileset images.")
@click.option('--output', required=True, help="Path and filename of the tileset.")
@click.option('--tile-size', required=True, type=click.INT, help="Size of each tile.")
@click.option('--tile-padding', default=0, type=click.INT, help="Space in pixels between each tile.")
@click.option('--scale', default=1, type=click.INT,
              help='Scale factor for each tile. With a scale factor of 2, 16x16 tiles will be 32x32 in the tileset.')
def create_tileset(path, output, tile_size, tile_padding, scale):
    """
    Creates a single tileset PNG from a directory of individual tiles.
    """
    tile_size = tile_size * scale

    tiles = []

    for img in glob.iglob(path + "\\*.png"):
        read_image = cv2.imread(img)
        read_image = Helper.scale_image(image=read_image, scale=scale)

        tiles.append(read_image)

    ncol = ceil(len(tiles) / sqrt(len(tiles)))

    tiles = [tiles[i:i + ncol] for i in range(0, len(tiles), ncol)]

    width = len(tiles) * (tile_size + tile_padding)
    height = ncol * (tile_size + tile_padding)

    tileset = np.zeros((width, height, 3), np.uint8)

    for x in range(len(tiles)):
        end_x = ((x + 1) * tile_size) + (tile_padding * x)

        for y, tile in enumerate(tiles[x]):
            end_y = ((y + 1) * tile_size) + (tile_padding * y)

            start_x = (x * tile_size) + (tile_padding * x)
            start_y = (y * tile_size) + (tile_padding * y)

            tileset[start_x:end_x, start_y:end_y] = tile

    tileset = Helper.apply_transparency_mask(image=tileset)

    cv2.imwrite(output, tileset)


if __name__ == '__main__':
    create_tileset()
