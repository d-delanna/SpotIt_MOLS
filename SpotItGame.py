import numpy as np
import itertools
from collections import defaultdict
from copy import deepcopy


class Table(list):
    """ List of multiple-depth manipulation. """
    def __init__(self, tables):
        self.tables = tables
        self.size = len(self.tables[0])
        super(Table, self).__init__(tables)

    def __repr__(self):
        for i in range(len(self)):
            self[i] = "\n".join(str(row) for row in self[i]) + "\n"
            # self[i] = "    " + ",\n    ".join(str(row) for row in self[i]) + "\n"
        return "\n".join(str(table) for table in self)

    @staticmethod
    def flatten(table):
        return [tab for tab in itertools.chain.from_iterable(table)]

    def compile_list(self):
        """
        Superimposes all tables onto each other.
        param: tables: tuple of n tables
        return: compiled_table: list of (length-n) tuples
        """
        compiled_list = []
        for i in range(self.size):
            compiled_list += [itertools.zip_longest(*[_table[i] for _table in self.tables])]
        return self.flatten(compiled_list)

    def compile_table(self):
        """ return: compiled_table: compile_list to a table of same dimensions """
        compiled_list = self.compile_list()
        compiled_table = []
        for i in range(self.size):
            compiled_table += [compiled_list[i::self.size]]
            compiled_list = [line for line in compiled_list]
        return compiled_table


class StandardForm:
    """ Checks for MOLS in standard form.
        Standard = all first rows or all first columns are in ascending order (0, 1, 2,...)
        :param: mols: type list (depth-3) of ints : list of MOLS """
    def __init__(self, mols):
        self.mols = mols
        self.range = (min(self.mols[0][0]), max(self.mols[0][0]))
        self.compiled_mols = Table(self.mols).compile_table()
        self.__is_standard()

    def __ordered_row(self):
        for i in range(self.range[0], self.range[1]):
            if tuple([i] * len(self.mols)) not in self.compiled_mols[0]:
                return False
        return True

    def __ordered_column(self):
        for i in range(self.range[0], self.range[1]):
            if tuple([i] * len(self.mols)) not in [elem[0] for elem in self.compiled_mols]:
                return False
        return True

    def __is_standard(self):
        if self.__ordered_row():
            return True
        elif self.__ordered_column():
            self.mols = [np.array(square).T.tolist() for square in self.mols]
            return True
        else:
            raise ValueError("MOLS not in standard form.")


class MOLSToSpotIt:
    """ Converts a set of MOLS (mutually orthogonal latin squares)
        of any size and converts them to SpotIt! cards.

        :param: mols: type list (depth-3) of ints : list of MOLS
        NOTE: MOLS must be complete set in standard form """

    def __init__(self, mols):
        if not CheckMOLS(mols).are_mols():
            raise ValueError("Input are not MOLS.")
        self.mols = StandardForm(mols).mols
        self.card_size = len(self.mols[0])  # size mols = num elements per card
        self.smallest_num = min(self.mols[0][0])
        self.group_templates = Table(self.mols).compile_table()
        self.game = self.__full_game()

    def __convert_to_spotit(self, group_template, group_num):
        """ Making a group using the group_template design.
            A group is the set of cards that have the same group number.

            :param: group_template: type list of tuples: template conversion from MOLS to SpotIt
            :param: group_num: type int: number should exists on the starting card """
        group = []
        for j, template in enumerate(group_template):
            card = [j + self.card_size + 2]
            for i in range(self.card_size - 1):
                card += [template[i] + (self.card_size - self.smallest_num + 2) + (self.card_size * (i + 1))]
            card = [group_num] + card  # put group_num on every card in group
            group += [card]
        return group

    def __full_game(self):
        """ Compiles full game into list containing all cards.
            Uses MOLS to generate the design on the cards.
            :return: type list (depth-3) of ints: [[Starting Card], [Group_1], ..., [Group_N]] """
        start_card = [[i + 1 for i in range(self.card_size + 1)]]

        game = [start_card]
        for i, group_template in enumerate(self.group_templates):
            game += [self.__convert_to_spotit(group_template, i + 1)]
        return game

    def __str__(self):
        """ :return: string of full SpotIt! game """
        print("SpotIt Game")
        return repr(Table(tuple(self.game)))

    def group(self, group_num):
        """ :param group_num: first number that appears on every card
            :return: string of single group """
        print("Group", group_num)
        return repr(Table(tuple([self.game[group_num]])))


class SpotItToMOLS:
    """ Conversion from SpotIt! game to its generating MOLS.
        :param: game: type list (depth-3) of ints: [[Starting Card], [Group_1], ..., [Group_N]]
        NOTE: SpotIt! game must be full game """

    def __init__(self, game):
        self.game = game[1:]  # ignore staring card
        self.card_size = len(self.game[0])  # number of elements on a card
        self.mols = self.__convert_game()

    def __ls_template(self, group):
        """ Takes a SpotIt! group and returns its latin square template
            :param: group: type list (depth-2) of ints: SpotIt! cards that have the same group number"""
        template = []
        for line in group:
            template += [[(num - (self.card_size + 2) - (self.card_size * (i+1))) for i, num in enumerate(line[2:])]]
        template = np.array(template).T.tolist()
        return template

    def __convert_game(self):
        """ :return: mols: type list (depth-3) of ints: list of latin squares """
        templates = [self.__ls_template(self.game[i]) for i in range(len(self.game))]

        mols = []
        for i in range(self.card_size - 1):
            mol = []
            for j in range(self.card_size):
                mol += [templates[j][i]]
            mols += [mol]

        return mols

    def __str__(self):
        """ :return: string of all mols """
        print("MOLS(" + str(self.card_size) + ")")
        return repr(Table(tuple(self.mols)))


class CheckMOLS:
    """ Different tests to verify if nxn tables are MOLS.
        :param: tables: type list (depth-2) of ints: potential latin squares
        :param: report_steps: type bool: True prints intermediate steps and location of error """

    def __init__(self, tables, report_steps=False):
        self.tables = tables
        self.report = report_steps
        self.size = len(tables[0])
        self.compiled = Table(self.tables).compile_list()

    def __repeated_pairs(self, pairs_list):
        """ Prints out all repeated pairs of a pairs list,
            and its coordinates in relation to the non-compiled nxn table.
            Top left starts at (0,0)."""
        pair_index_map = defaultdict(list)
        for idx, pair in enumerate(pairs_list):
            pair_index_map[pair].append(idx)
        for pair in pair_index_map:
            indices = pair_index_map[pair]
            if len(indices) > 1:
                coord_repeat_pairs = [(idx % self.size, idx // self.size) for idx in indices]
                if self.report:
                    print("Repeated {} at (row, column): {}".format(pair, coord_repeat_pairs))

    def is_ls(self, table):
        """ Checks if a square is a latin square. """
        square = deepcopy(table)
        for row in square:
            if len(row) != len(set(row)):
                if self.report:
                    print("First repeated number in row {}".format(square.index(row)))  # (top left starts at (0,0))
                return False

        square = list(np.array(table).T)
        for index, column in enumerate(square):
            if len(column) != len(set(column)):
                if self.report:
                    print("First repeated number in column {}".format(index))
                return False
        return True

    def are_orthog(self, table1, table2):
        """ Checks if two latin squares form Graeco-Latin square. """
        table = Table([table1, table2]).compile_list()
        if len(table) == len(set(table)):
            return True
        self.__repeated_pairs(table)
        return False

    def are_mols(self):
        """ Checks if all squares are mutually orthogonal latin squares. """
        # checks if all squares are latin squares
        for table in self.tables:
            if self.report:
                print("\nChecking Latin Square", self.tables.index(table) + 1)
            if not self.is_ls(table):
                return False

        # checks if every combinations of the LSs are orthogonal to each other
        labeled_tables = [(table, label + 1) for label, table in enumerate(self.tables)]
        combination_pairs = itertools.combinations(labeled_tables, 2)
        for pair in combination_pairs:
            if self.report:
                print("\nChecking Orthogonality of Latin Squares", (pair[0][1], pair[1][1]))
            orthog = self.are_orthog(pair[0][0], pair[1][0])
            if not orthog:
                return False

        return True


class CheckSpotIt:
    """ Checks if set of cards make a SpotIt game.
        :param: game = [[start_card], [group1], ..., [groupN]] """
    def __init__(self, game):
        self.game = game
        self.is_spotit = True
        self.__compare_cards()

    def __check_conditions(self, group, comparison_cards):
        """ A pair of cards has to have exactly one item in common. """
        for card1 in group:
            for card2 in comparison_cards:
                if len(set(card1).intersection(set(card2))) != 1:
                    print(card1, '\t', card2, '\t', set(card1).intersection(set(card2)))
                    self.is_spotit = False

    def __compare_cards(self):
        """ Compares pairs of cards from deck. """
        self.is_spotit = True
        game = deepcopy(self.game[2:])  # ignore group1
        for i in range(len(game) - 1):
            group = game[0]
            comparison_cards = [cards for cards in itertools.chain.from_iterable(game)][len(group):]
            self.__check_conditions(group, comparison_cards)
            game = game[1:]

