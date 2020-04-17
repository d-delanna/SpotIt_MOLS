import itertools
from copy import deepcopy
import numpy as np


class MOLSToSpotIt:
    """ Converts a set of MOLS of any siz and converts them to SpotIt! cards.
        param: mols: type< list(list(ints)) >: latin squares """

    def __init__(self, *mols):
        self.mols = mols
        self.size = len(mols[0])
        self.game = self.full_game()

    # Can make this private
    def _convert_to_spotit(self, table, group_num):
        """
        converts single latin square to group

        :param table:
        :param group_num:
        :return:
        """
        square = deepcopy(table)
        for line in square:
            for i in range(self.size):
                line[i] = line[i] + (self.size + 2) + self.size * i
            line.insert(0, group_num)
        return square

    def full_game(self):
        """ compiles full game into list containing all cards """
        start_card = [[i + 1 for i in range(self.size + 1)]]
        group2 = [[2] + [(self.size + 2) + (self.size * i) + j for i in range(self.size)] for j in range(self.size)]
        group1 = [[1] + list(line) for line in np.array(group2).T[1:]]

        game = [start_card, group1, group2]
        for i, mol in enumerate(self.mols):
            game += [self._convert_to_spotit(mol, i + 3)]
        return game

    def __str__(self):
        """ string of full SpotIt! game """
        print("SpotIt Game")
        print_game = []
        for group in self.full_game():
            print_game += [str(line) + "\n" for line in group] + ["\n"]
        return "".join(print_game)

    def print_group(self, group_num):
        """ prints single group """
        print("Group", group_num)
        for line in self.full_game()[group_num]:
            print(line)
        # [print(line) for line in self.full_game()[group_num]]
        print("\n")


class SpotItToMols:
    """ conversion from SpotIt! game to its generating MOLS
        param: game: list[starting card, group1, group2, ..., groupN]"""

    def __init__(self, game):
        self.game = game[3:]
        self.size = len(self.game[0])
        self.mols = self.compile_mols()

    def convert_to_ls(self, group):
        """ takes group from SpotIt and returns its latin square generator """
        # [print(line) for line in group]
        latin_square = [[(num - (self.size + 2) - self.size * i) for i, num in enumerate(line[1:])] for line in group]
        return latin_square

    def compile_mols(self):
        # Mutating property here
        mols = [self.convert_to_ls(self.game[i]) for i in range(len(self.game))]
        return mols

    def __str__(self):
        print("MOLS(" + str(self.size) + ")")
        print_mols = []
        for mol in self.mols:  # Now we can just use self.mols here
            print_mols += [str(line) + "\n" for line in mol] + ["\n"]
        return "".join(print_mols)


class Check:
    """ tests to verify if nxn tables are MOLS
        param: tables: type< list(list(ints)) >: supposed latin squares """

    def __init__(self, *tables):
        self.tables = tables
        self.size = len(tables[0])

    def __flatten(self, table):
        return list(itertools.chain.from_iterable(table))

    def compiler(self, *tables):
        """ superimposes table2 onto table1: list(list(length-n tuples))"""
        compiled_table = [list(itertools.zip_longest(*[_table[i] for _table in tables])) for i in range(self.size)]
        return self.__flatten(compiled_table)

    def __repeated_pairs(self, table):
        """ if not orthogonal, will print out all repeated pairs """

        copied_table = deepcopy(table)
        # Do we actually want to mutate the table here?
        while copied_table:
            if copied_table.count(copied_table[0]) > 1:
                repeat_pairs = [idx for idx in range(len(copied_table)) if copied_table[idx] == copied_table[0]]
                coord_repeat_pairs = [(idx % self.size, idx // self.size) for idx in repeat_pairs]
                print("Repeated {} at (row, column): {}".format(copied_table[0], coord_repeat_pairs))
                [copied_table.pop(idx) for idx in repeat_pairs[::-1]]

    @staticmethod
    def is_latin_square(table):
        """ checks if a square is a latin square"""
        for row in table:
            if len(row) != len(set(row)):
                # self.__repeated_pairs(table)
                return False
        for column in np.array(table).T:
            if len(column) != len(set(column)):
                # self.__repeated_pairs(table)
                return False
        return True

    def orthogonal(self, table1, table2):
        """ checks if two latin squares form Graeco-Latin square """
        table = self.compiler(table1, table2)
        if len(table) == len(set(table)):
            return True
        self.__repeated_pairs(table)
        return False

    def mutually_orthog(self):
        """ checks if all squares are mutually orthogonal latin squares """
        for table in self.tables:
            if not self.is_latin_square(table):
                return False
        orthog = [self.orthogonal(tab[0], tab[1]) for tab in itertools.combinations(self.tables, 2)]
        if False in orthog:
            return False
        return True


class Table(list):
    def __init__(self, *args, **kwargs):
        super(Table, self).__init__(args[0])

    def __str__(self):
        return "\n".join(str(row) for row in self)


def main():

    # EXAMPLE MOLS ---------------------------------------------
    # LS3 and LS4 orthogonal
    # LS3 and LS4 orthogonal
    # LS4 and LS5 not orthogonal

    LS3 = Table(
        [
            [0, 8, 9, 7, 5, 6, 4, 2, 3, 1],
            [9, 1, 4, 6, 2, 7, 3, 8, 0, 5],
            [7, 4, 2, 5, 1, 3, 8, 6, 9, 0],
            [8, 6, 5, 3, 9, 2, 1, 0, 4, 7],
            [6, 2, 1, 8, 4, 0, 9, 5, 7, 3],
            [4, 9, 3, 2, 7, 5, 0, 1, 6, 8],
            [5, 3, 7, 1, 0, 8, 6, 9, 2, 4],
            [3, 5, 0, 9, 8, 4, 2, 7, 1, 6],
            [1, 7, 6, 0, 3, 9, 5, 4, 8, 2],
            [2, 0, 8, 4, 6, 1, 7, 3, 5, 9],
        ]
    )

    LS4 = Table(
        [
            [0, 7, 8, 9, 1, 2, 3, 4, 5, 6],
            [9, 0, 6, 1, 8, 3, 2, 5, 4, 7],
            [7, 2, 0, 4, 3, 9, 1, 8, 6, 5],
            [8, 5, 3, 0, 2, 1, 7, 6, 9, 4],
            [6, 9, 5, 3, 0, 7, 4, 2, 1, 8],
            [4, 1, 7, 6, 5, 0, 8, 9, 3, 2],
            [5, 4, 2, 8, 9, 6, 0, 3, 7, 1],
            [3, 6, 1, 7, 4, 8, 5, 0, 2, 9],
            [1, 8, 4, 2, 6, 5, 9, 7, 0, 3],
            [2, 3, 9, 5, 7, 4, 6, 1, 8, 0],
        ]
    )

    LS5 = Table(
        [
            [0, 7, 8, 9, 1, 2, 3, 4, 5, 6],
            [6, 4, 2, 8, 9, 5, 1, 3, 7, 0],
            [4, 9, 5, 3, 2, 7, 6, 0, 1, 8],
            [5, 1, 7, 6, 4, 3, 8, 9, 0, 2],
            [3, 2, 9, 0, 7, 1, 5, 6, 8, 4],
            [1, 0, 3, 7, 6, 8, 2, 5, 4, 9],
            [2, 8, 0, 1, 3, 4, 9, 7, 6, 5],
            [9, 5, 4, 2, 8, 6, 0, 1, 3, 7],
            [7, 3, 6, 5, 0, 9, 4, 8, 2, 1],
            [8, 6, 1, 4, 5, 0, 7, 2, 9, 3],
        ]
    )

    game = MOLSToSpotIt(LS3, LS4)
    print(game)

    mols = SpotItToMols(game.full_game())
    print(mols)  # should return back to original form

    check = Check(LS3, LS4, LS5)
    print(check.orthogonal(LS3, LS4))
    print(check.orthogonal(LS3, LS5))
    print(check.orthogonal(LS4, LS5))


if __name__ == "__main__":
    main()
