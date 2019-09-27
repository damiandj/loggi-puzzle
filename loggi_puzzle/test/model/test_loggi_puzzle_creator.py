import os
import numpy as np

from loggi_puzzle.model import LoggiPuzzleCreator

ASSETS_PATH = os.path.join("loggi_puzzle", "test", "assets")


def test_prepare_black_white_image():
    lpc = LoggiPuzzleCreator(image_path=os.path.join(ASSETS_PATH, 'apple.jpg'),
                             out_height=10, out_width=10)
    img = lpc.prepare_black_white_image()

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
    np.testing.assert_array_equal(exp, img)


def test_prepare_puzzle_data():
    lpc = LoggiPuzzleCreator()
    lpc.black_white_image = [
        [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
        [  0,   0,   0,   0, 255, 255, 255,   0,   0,   0],
        [  0, 255, 255, 255, 255,   0, 255, 255,   0,   0],
        [255,   0, 255, 255, 255, 255,   0, 255, 255,   0],
        [  0, 255, 255, 255,   0, 255, 255, 255, 255, 255],
        [255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
        [255,   0, 255, 255,   0,   0, 255, 255, 255,   0],
        [  0,   0, 255, 255, 255, 255, 255, 255,   0,   0]
    ]
    rows, max_row = lpc.prepare_puzzle_data()

    rows_exp = [
        [],
        [3],
        [4, 2],
        [1, 4, 2],
        [3, 5],
        [10],
        [1, 2, 3],
        [6]
    ]
    assert max_row == 3
    np.testing.assert_array_equal(rows_exp, rows)

    columns, max_col = lpc.prepare_puzzle_data(transpose=True)

    columns_exp = [
        [1, 2],
        [1, 2],
        [6],
        [6],
        [3, 1, 1],
        [1, 3, 1],
        [2, 4],
        [6],
        [4],
        [2]
    ]
    assert max_col == 3
    np.testing.assert_array_equal(columns_exp, columns)


def test_strip_image():
    lpc = LoggiPuzzleCreator()
    image = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 255, 255, 255, 0, 0, 0],
        [0, 255, 255, 255, 255, 0, 255, 255, 0, 0],
        [0, 0, 255, 255, 255, 255, 0, 255, 255, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 255, 255, 255, 0, 255, 255, 255, 255, 0],
        [0, 255, 255, 255, 255, 255, 255, 255, 255, 0],
        [0, 0, 255, 255, 0, 0, 255, 255, 255, 0],
        [0, 0, 255, 255, 255, 255, 255, 255, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    image_out_exp = [
        [0, 0, 0, 255, 255, 255, 0, 0],
        [255, 255, 255, 255, 0, 255, 255, 0],
        [0, 255, 255, 255, 255, 0, 255, 255],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [255, 255, 255, 0, 255, 255, 255, 255],
        [255, 255, 255, 255, 255, 255, 255, 255],
        [0, 255, 255, 0, 0, 255, 255, 255],
        [0, 255, 255, 255, 255, 255, 255, 0],
    ]

    image_out = lpc.strip_image(image)

    np.testing.assert_array_equal(image_out_exp, image_out)