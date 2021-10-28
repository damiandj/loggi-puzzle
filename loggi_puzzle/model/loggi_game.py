import copy
import random
import itertools
import numpy as np

import time


class Loggi:
    def __init__(self, rows_descriptions, columns_descriptions):
        self.raw_rows_descriptions = rows_descriptions
        self.raw_columns_descriptions = columns_descriptions
        self.rows_descriptions = self._prepare_descriptions(rows_descriptions)
        self.columns_descriptions = self._prepare_descriptions(columns_descriptions)

        self.width = len(self.columns_descriptions)
        self.height = len(self.rows_descriptions)

        self.game_sum = self._compute_game_sum()
        self.game_field = self._create_game_field()

    @staticmethod
    def _prepare_descriptions(_descriptions):
        extend_descriptions = []
        max_size = max(len(_item) for _item in _descriptions)
        for row in copy.deepcopy(_descriptions):
            [row.append(0) for _ in range(max_size - len(row))]
            extend_descriptions.append(row)

        return np.array(extend_descriptions)

    def _compute_game_sum(self):
        self._validate_game()
        return np.sum(self.rows_descriptions)

    def _validate_game(self):
        row_sum = np.sum(self.rows_descriptions)
        col_sum = np.sum(self.columns_descriptions)
        if not row_sum == col_sum:
            raise Exception(f"Sum of row_descriptions must be equal to sum of column_description, given: {row_sum} != {col_sum}")

    def _create_game_field(self):
        return np.full((self.width, self.height), -1, dtype=int)

    def validate_solution(self, solution):
        return np.array_equal(self._count_rows(solution), self.rows_descriptions) and \
               np.array_equal(self._count_columns(solution), self.columns_descriptions)

    def _get_good_rows(self):
        good_rows = {}
        for row_num, row in enumerate(self.rows_descriptions):
            all_poss = [np.bincount(xs, minlength=self.width) for xs in itertools.combinations(range(self.width), np.sum(row))]
            for pos in all_poss:
                if np.array_equal(self._count_in_line(pos), self.raw_rows_descriptions[row_num]):
                    if row_num not in good_rows:
                        good_rows[row_num] = []
                    good_rows[row_num].append(pos)
        return good_rows

    def _get_good_cols(self):
        good_rows = {}
        for row_num, row in enumerate(self.columns_descriptions):

            all_poss = [np.bincount(xs, minlength=self.width) for xs in itertools.combinations(range(self.width), np.sum(row))]
            for pos in all_poss:
                if np.array_equal(self._count_in_line(pos), self.raw_columns_descriptions[row_num]):
                    if row_num not in good_rows:
                        good_rows[row_num] = []
                    good_rows[row_num].append(pos)
        return good_rows

    def find_random_solution(self):
        good_rows = self._get_good_rows().values()
        good_colls = self._get_good_cols().values()

        i = 0
        for solution in itertools.product(*good_rows):
            i += 1
            # print(solution)
            if self.validate_solution(solution):
                return np.array(solution)

    @staticmethod
    def _append_if_item(_item, _list):
        if _item:
            _list.append(_item)

    @staticmethod
    def _count_in_line(line):
        line_counter = []
        line_length = 0
        for item in line:
            if not item:
                Loggi._append_if_item(line_length, line_counter)
                line_length = 0
                continue
            line_length += 1
        Loggi._append_if_item(line_length, line_counter)

        return line_counter

    @staticmethod
    def _count_lines(solution):
        rows_counter = []
        for line in solution:
            line_counter = Loggi._count_in_line(line)
            rows_counter.append(line_counter)

        return Loggi._prepare_descriptions(rows_counter)

    @staticmethod
    def _count_columns(solution):
        return Loggi._count_lines(np.transpose(solution))

    @staticmethod
    def _count_rows(solution):
        return Loggi._count_lines(solution)


rows = [[4], [1, 1], [9], [12], [1, 11], [12], [13], [13], [13], [13], [13], [13], [11]]
columns = [[2, 6], [2, 8], [11], [11], [11], [1, 11], [13], [1, 11], [1, 11], [12], [10], [10], [8]]

#
# rows = [[2, 1], [4], [4], [1, 2]]
# columns = [[4], [3], [3], [4]]

rows = [[2, 1, 4], [2, 2, 1], [1, 1], [4, 2, 2], [16], [2, 14], [1, 15], [18], [18], [18], [18], [18], [18], [18], [18], [17], [15], [12]]

columns =[[12], [2, 10], [2, 11], [15], [2, 15], [2, 15], [14], [1, 15], [17], [2, 14], [1, 14], [1, 15], [18], [14], [14], [13], [11], [8]]

l = Loggi(rows, columns)
# print(l.game_field)
# s = [[True, True, False, True, False], [True, False, False, True, False], [False, True, True, True, False]]
# print(l.validate_solution(s))
print(l.find_random_solution())