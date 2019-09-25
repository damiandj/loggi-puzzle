import os
import numpy as np
import cv2
import copy

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from PIL import Image


class LoggiPuzzleCreator:
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
        self.box_size_pix = 25.

    def prepare_loggi(self):
        self.prepare_black_white_image()
        self.rows, self.max_row = self.prepare_puzzle_data(transpose=True)
        self.columns, self.max_col = self.prepare_puzzle_data()
        my_dpi = self.prepare_grid_image()

        self.fig.savefig("puzzle_{}".format(self.image_name), dpi=my_dpi)
        self.save_black_white_image(pix_dpi=self.box_size_pix)

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
        width = int(self.box_size_pix * (len(self.rows) + self.max_col))
        height = int(self.box_size_pix * (len(self.columns) + self.max_row))
        image = self.create_blank(width, height, rgb_color=(255, 255, 255))
        image = Image.fromarray(np.uint8(image))
        my_dpi = 50
        self.fig = plt.figure(figsize=(float(width / (2*self.box_size_pix)), float(height / (2*self.box_size_pix))))
        self.ax = self.fig.add_subplot(111)

        # Remove whitespace from around the image
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

        # Set the gridding interval
        loc_x_minor = plticker.IndexLocator(base=self.box_size_pix, offset=self.max_col * self.box_size_pix)
        loc_y_minor = plticker.IndexLocator(base=self.box_size_pix, offset=self.max_row * self.box_size_pix)
        self.ax.xaxis.set_minor_locator(loc_x_minor)
        self.ax.yaxis.set_minor_locator(loc_y_minor)
        major_axis_dist = 5 * self.box_size_pix
        loc_x_major = plticker.IndexLocator(base=major_axis_dist, offset=self.max_col * self.box_size_pix)
        loc_y_major = plticker.IndexLocator(base=major_axis_dist, offset=self.max_row * self.box_size_pix)
        self.ax.xaxis.set_major_locator(loc_x_major)
        self.ax.yaxis.set_major_locator(loc_y_major)

        # Add the grid
        self.ax.grid(which='major', axis='both', linestyle='-', linewidth=5)
        self.ax.grid(which='minor', axis='both', linestyle='-', linewidth=2)
        # Add the image
        self.ax.imshow(image)

        self.add_numbers_on_top()
        self.add_numbers_on_left()

        return my_dpi

    def add_numbers_on_top(self):
        for i in self.rows:
            for j in range(len(self.rows[i])):
                x = self.box_size_pix / 2 + (i + self.max_col) * self.box_size_pix
                y = self.box_size_pix / 2. + float(j + (self.max_row - len(self.rows[i]))) * self.box_size_pix

                text = self.rows[i][j]
                self.ax.text(x, y, '{}'.format(text), color='black', ha='center', va='center',
                             fontsize=int(self.box_size_pix))

    def add_numbers_on_left(self):
        for i in self.columns:
            for j in range(len(self.columns[i])):
                y = self.box_size_pix / 2 + (i + self.max_row) * self.box_size_pix
                x = self.box_size_pix / 2. + float(j + (self.max_col - len(self.columns[i]))) * self.box_size_pix

                text = self.columns[i][j]
                self.ax.text(x, y, '{}'.format(text), color='black', ha='center', va='center',
                             fontsize=int(self.box_size_pix))

    def save_black_white_image(self, pix_dpi):
        ready_image = copy.deepcopy(self.black_white_image)
        for row_num, row in enumerate(ready_image):
            for item_num, item in enumerate(row):
                ready_image[row_num][item_num] = 255 - item
        ready_image = cv2.resize(ready_image,
                                 (int(self.out_width * pix_dpi),
                                  int(self.out_height * pix_dpi)),
                                 interpolation=cv2.INTER_AREA)
        im = Image.fromarray(ready_image)
        im.save("solution_{}".format(self.image_name))
