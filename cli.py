import cv2
import numpy as np
import glob
import click
import os
from helper import Helper
from math import ceil, sqrt


def validate_path(ctx, param, value):
    if os.path.isdir(value):
        return value
    else:
        raise click.BadParameter('Invalid path')


@click.group()
def cli():
    pass


@cli.command()
@click.option('--path', required=True, type=click.Path(), callback=validate_path,
              help="Input directory of tileset images.")
@click.option('--output', required=True, type=click.Path(), help="Path and filename of the tileset.")
@click.option('--tile-size', required=True, type=click.INT, help="Size in pixels of each tile.")
@click.option('--tile-padding', default=0, type=click.INT, help="Space in pixels between each tile.")
@click.option('--scale', default=1, type=click.FLOAT, help='Scale factor for each tile.')
def tileset_from_images(path, output, tile_size, tile_padding, scale):
    """
    Creates a single tileset PNG from a directory of individual tiles.
    """

    tile_size = ceil(tile_size * scale)

    tiles = []

    for img in glob.iglob(path + "\\*.png"):
        read_image = cv2.imread(img, cv2.IMREAD_UNCHANGED)
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


@cli.command()
@click.option('--path', required=True, type=click.Path(), callback=validate_path,
              help="Input directory of images to resize.")
@click.option('--output', required=True, type=click.Path(), callback=validate_path,
              help="Output directory for re-sized images.")
@click.option('--scale', default=1, type=click.FLOAT, help='Scale factor for each image.')
def resize_images(path, output, scale):
    """
    Re-sizes each image in a given directory by a given scale.
    """

    for img in glob.iglob(path + "\\*.png"):

        file_name = os.path.split(img)[-1]
        write_path = os.path.join(output, file_name)

        read_image = cv2.imread(img, cv2.IMREAD_UNCHANGED)

        resized_image = Helper.scale_image(read_image, scale)

        cv2.imwrite(write_path, resized_image)


if __name__ == '__main__':
    cli()
