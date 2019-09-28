import os
from PIL import Image
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
    exp_max_row = 3
    if not max_row == exp_max_row:
        raise AssertionError("{} == {}".format(max_row, exp_max_row))
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

    exp_max_col = 3
    if not max_col == exp_max_col:
        raise AssertionError("{} == {}".format(max_col, exp_max_col))

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


def test_create_blank():
    blank = LoggiPuzzleCreator.create_blank(2, 3, rgb_color=(1, 2, 3))
    blank_exp = [[[1, 2, 3], [1, 2, 3]],
                 [[1, 2, 3], [1, 2, 3]],
                 [[1, 2, 3], [1, 2, 3]]]

    np.testing.assert_array_equal(blank, blank_exp)


def test_save_black_white_image():
    lpc = LoggiPuzzleCreator(image_path=os.path.join(ASSETS_PATH, 'apple.jpg'),
                             out_height=25, out_width=25, save_path=os.path.join(ASSETS_PATH, 'out'))
    lpc.black_white_image = lpc.prepare_black_white_image()
    lpc.save_black_white_image(pix_dpi=25)

    img_out = Image.open(os.path.join(ASSETS_PATH, 'out', 'solution_apple.jpg'))
    img_out.load()
    data_out = np.asarray(img_out, dtype="int32")

    img_exp = Image.open(os.path.join(ASSETS_PATH, 'solution_apple.jpg'))
    img_exp.load()
    data_exp = np.asarray(img_out, dtype="int32")

    np.testing.assert_array_equal(data_out, data_exp)


def test_prepare_loggi():
    lpc = LoggiPuzzleCreator(image_path=os.path.join(ASSETS_PATH, 'apple.jpg'),
                             out_height=25, out_width=25, save_path=os.path.join(ASSETS_PATH, 'out'))
    lpc.prepare_loggi()

    img_out = Image.open(os.path.join(ASSETS_PATH, 'out', 'puzzle_apple.jpg'))
    img_out.load()
    data_out = np.asarray(img_out, dtype="int32")

    img_exp = Image.open(os.path.join(ASSETS_PATH, 'puzzle_apple.jpg'))
    img_exp.load()
    data_exp = np.asarray(img_exp, dtype="int32")

    np.testing.assert_array_equal(data_exp, data_out)