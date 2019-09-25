import os

import numpy as np
import cv2
import copy

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from PIL import Image


class LoggiCreator:
    def __init__(self, image_path: str = None, out_width: int = 0, out_height: int = 0):
        self.image_path = image_path
        self.out_width = out_width
        self.out_height = out_height

        self.image_name = os.path.basename(self.image_path)

        self.black_white_image = None
        self.max_row = None
        self.rows = None
        self.columns = None
        self.max_col = None

    def prepare_loggi(self):
        self.prepare_black_white_image()
        self.rows, self.max_row = self.prepare_puzzle_data()
        self.columns, self.max_col = self.prepare_puzzle_data(transpose=True)
        my_dpi, pix_dpi = self.prepare_grid_image()
        self.save_black_white_image(pix_dpi=pix_dpi)
        print(self.fig)
        self.fig.savefig("puzzle_{}".format(self.image_name), dpi=my_dpi)

    def prepare_black_white_image(self):
        img = cv2.imread(self.image_path, 0)
        img = cv2.resize(img, dsize=(self.out_width, self.out_height), interpolation=cv2.INTER_AREA)
        edges = cv2.Canny(img, 30, 500, True)
        _, image_interior = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        for row_num, row in enumerate(image_interior):
            for item_num, item in enumerate(row):
                image_interior[row_num][item_num] = 255 - item
        ready_image = cv2.add(edges, image_interior)

        self.black_white_image = ready_image

    def prepare_puzzle_data(self, transpose: bool = False):
        output = dict()
        if transpose:
            data = np.transpose(self.black_white_image)
        else:
            data = self.black_white_image
        for num_row, row in enumerate(data):
            output[num_row] = []
            counter = 0
            for item in row:
                if item > 0:
                    counter += 1
                else:
                    if counter > 0:
                        output[num_row].append(counter)
                        counter = 0
            if counter > 0:
                output[num_row].append(counter)

        max_len = max([len(val) for val in output.values()])
        return output, max_len

    @staticmethod
    def create_blank(width, height, rgb_color=(0, 0, 0)):
        image = np.zeros((height, width, 3), np.uint8)
        color = tuple(reversed(rgb_color))
        image[:] = color

        return image

    def prepare_grid_image(self):
        pix_dpi = 15.
        width = int(pix_dpi * (len(self.columns) + self.max_row + 5.))
        height = int(pix_dpi * (len(self.rows) + self.max_col + 5.))
        image = self.create_blank(width, height, rgb_color=(255, 255, 255))
        image = Image.fromarray(np.uint8(image))
        my_dpi = 5.
        self.fig = plt.figure(figsize=(float(image.size[0] / my_dpi), float(image.size[1] / my_dpi)))
        self.ax = self.fig.add_subplot(111)

        # Remove whitespace from around the image
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

        # Set the gridding interval
        loc_x_minor = plticker.IndexLocator(base=pix_dpi, offset=(1 + self.max_col) * pix_dpi)
        loc_y_minor = plticker.IndexLocator(base=pix_dpi, offset=(1 + self.max_row) * pix_dpi)
        self.ax.xaxis.set_minor_locator(loc_x_minor)
        self.ax.yaxis.set_minor_locator(loc_y_minor)
        major_axis_dist = 5 * pix_dpi
        loc_x_major = plticker.IndexLocator(base=major_axis_dist, offset=(1 + self.max_col) * pix_dpi)
        loc_y_major = plticker.IndexLocator(base=major_axis_dist, offset=(1 + self.max_row) * pix_dpi)
        self.ax.xaxis.set_major_locator(loc_x_major)
        self.ax.yaxis.set_major_locator(loc_y_major)

        # Add the grid
        self.ax.grid(which='major', axis='both', linestyle='-', linewidth=10)
        self.ax.grid(which='minor', axis='both', linestyle='-', linewidth=2)
        # Add the image
        self.ax.imshow(image)
        # Find number of gridsquares in x and y direction
        nx = abs(int(float(self.ax.get_xlim()[1] - self.ax.get_xlim()[0]) / float(pix_dpi)))
        ny = abs(int(float(self.ax.get_ylim()[1] - self.ax.get_ylim()[0]) / float(pix_dpi)))

        self.add_numbers_on_top(nx, ny, pix_dpi)
        self.add_numbers_on_left(nx, ny, pix_dpi)

        return my_dpi, pix_dpi

    def add_numbers_on_left(self, nx, ny, pix_dpi):
        for j in range(ny):
            for i in range(nx):
                x = pix_dpi / 2. + float(i) * pix_dpi
                try:
                    text = (self.columns[i - self.max_col - 1][j])
                except IndexError:
                    continue
                except KeyError:
                    continue
                y = (self.max_row - len(self.columns[i - self.max_col - 1]) + j + 1.5) * pix_dpi
                self.ax.text(x, y, '{}'.format(text), color='black', ha='center', va='center', fontsize=int(pix_dpi))

    def add_numbers_on_top(self, nx, ny, pix_dpi):
        for j in range(ny):
            y = pix_dpi / 2 + j * pix_dpi
            for i in range(nx):
                x = pix_dpi / 2. + float(i) * pix_dpi
                try:
                    text = (self.rows[j - self.max_row - 1][i])
                except IndexError:
                    continue
                except KeyError:
                    continue
                x = x + (self.max_col - len(self.rows[j - self.max_row - 1]) + 1) * pix_dpi
                self.ax.text(x, y, '{}'.format(text), color='black', ha='center', va='center', fontsize=int(pix_dpi))

    def save_black_white_image(self, pix_dpi):
        ready_image = copy.deepcopy(self.black_white_image)
        for row_num, row in enumerate(ready_image):
            for item_num, item in enumerate(row):
                ready_image[row_num][item_num] = 255 - item
        ready_image = cv2.resize(ready_image,
                                 (int(self.out_width * pix_dpi), int(self.out_height * pix_dpi)),
                                 interpolation=cv2.INTER_AREA)
        im = Image.fromarray(ready_image)
        im.save("solution_{}".format(self.image_name))


# def do_job(image_path, out_size):
#     ready_image = prepare_black_white_image(image_path, out_size)
#     rows, max_row = prepare_rows(ready_image)
#     columns, max_col = prepare_rows(ready_image, transpose=True)
#
#     fig, my_dpi, pix_dpi = prepare_grid_image(columns, max_col, max_row, rows)
#
#     fig.savefig('out.jpg', dpi=my_dpi)
#
#     save_black_white_image(out_size, pix_dpi, ready_image)


def main():
    # prompt = '> '
    # print('Provide input image path:')
    # image_path = input(prompt)
    # print('Provide puzzle width:')
    # puzzle_size_x = input(prompt)
    # print('Provide puzzle height:')
    # puzzle_size_y = input(prompt)
    image_path = 'apple.jpg'
    puzzle_size_x = 70
    puzzle_size_y = 50
    lc = LoggiCreator(image_path=image_path, out_width=puzzle_size_x, out_height=puzzle_size_y)
    lc.prepare_loggi()

    # do_job(image_path, (int(puzzle_size_x), int(puzzle_size_y)))

main()

# args = parser.parse_args()
# parser = argparse.ArgumentParser(description='Create puzzle.')
# parser.add_argument('-ip', '--image_path',
#                     help='image path')
# parser.add_argument('-size_x', '--puzzle_size_x',
#                     help='Puzzle size x')
# parser.add_argument('-size_y', '--puzzle_size_y',
# #                     help='Puzzle size y')



