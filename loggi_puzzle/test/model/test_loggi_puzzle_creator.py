import os
import numpy as np

from loggi_puzzle.model import LoggiPuzzleCreator

ASSETS_PATH = os.path.join("loggi_puzzle", "test", "assets")


def init():
    lpc = LoggiPuzzleCreator(image_path=os.path.join(ASSETS_PATH, 'apple.jpg'),
                             out_height=10, out_width=10)

    return lpc


def test_prepare_black_white_image():
    lpc = init()
    lpc.prepare_black_white_image()

    exp = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 255, 255, 255, 0, 0, 0],
        [0, 255, 255, 255, 255, 0, 255, 255, 0, 0],
        [255, 255, 255, 255, 255, 255, 255, 255, 255, 0],
        [0, 255, 255, 255, 255, 255, 255, 255, 255, 255],
        [255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
        [255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
        [255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
        [255, 255, 255, 255, 255, 255, 255, 255, 255, 0],
        [0, 0, 255, 255, 255, 255, 255, 255, 0, 0]
    ]
    np.testing.assert_array_equal(exp, lpc.black_white_image)

