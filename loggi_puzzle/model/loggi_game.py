import numpy as np


class Loggi:
    def __init__(self, rows_descriptions, columns_descriptions):
        self.rows_descriptions = rows_descriptions
        self.columns_descriptions = columns_descriptions

        self.width = len(self.columns_descriptions)
        self.height = len(self.rows_descriptions)

        self.game_field = self._create_game_field()

    def _create_game_field(self):
        return np.zeros((self.width, self.height), dtype=bool)

    def validate_solution(self, solution):
        return self._count_rows(solution) == self.rows_descriptions and \
               self._count_columns(solution) == self.columns_descriptions

    def find_random_solution(self):
        i = 0
        solutions = []
        while 1:
            solution = np.random.choice([True, False], size=(self.width, self.height))
            if str(solution) in solutions:
                continue
            solutions.append(str(solution))
            i += 1
            # print(solution)
            if self.validate_solution(solution):
                return solution
            if i > 1000000:
                return


    @staticmethod
    def _append_if_item(_item, _list):
        if _item:
            _list.append(_item)

    @staticmethod
    def _count_rows(solution):
        rows_counter = []
        for row in solution:
            row_counter = []
            row_length = 0
            for item in row:
                if not item:
                    Loggi._append_if_item(row_length, row_counter)
                    row_length = 0
                    continue
                row_length += 1
            Loggi._append_if_item(row_length, row_counter)
            rows_counter.append(row_counter)

        return rows_counter

    @staticmethod
    def _count_columns(solution):
        return Loggi._count_rows(np.transpose(solution))


rows = [[3], [4, 2], [8], [8], [8], [8], [8], [8]]
columns = [[7], [7], [7], [8], [1, 6], [8], [7], [6]]

# rows = [[2, 1], [1, 1], [3]]
# columns = [[2], [1, 1], [1], [3], []]

l = Loggi(rows, columns)
# print(l.game_field)
# s = [[True, True, False, True, False], [True, False, False, True, False], [False, True, True, True, False]]
# print(l.validate_solution(s))
print(l.find_random_solution())