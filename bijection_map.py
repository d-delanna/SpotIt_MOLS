import math
import numpy as np
import itertools 
from copy import deepcopy

class MOLSToSpotIt:   
    """ 
    Converts a set of MOLS (mutually orthogonal latin squares)
    of any size and converts them to SpotIt! cards.
    
    param: mols: type list (depth-3) of ints : list of mutually orthogonal latin squares
    """
    
    def __init__(self, *mols):
        self.mols = mols
        self.size = len(mols[0])  # size mols = num elements per card - 1
        self.game = self.__full_game()
        
    def __convert_to_spotit(self, latin_square, group_num):
        """ 
        Converts a single latin square to a group 
        where group is the family of cards that contain the group number.
        
        param: latin_square: type list (depth-2) of ints: nxn square
        param: group_num: type int: number should exists on the starting card
        """
        group = deepcopy(latin_square)
        for line in group:
            for i in range(self.size):
                line[i] = line[i] + (self.size+2) + self.size*i
            line.insert(0, group_num)
        return group
        
    def __full_game(self):
        """ 
        Compiles full game into list containing all cards.
        Uses MOLS to generate Group_i for i more than 2.
        
        return: type list (depth-3) of ints: [Starting Card, Group_1, ..., Group_N]
        """
        start_card = [[i+1 for i in range(self.size+1)]]
        group2 = [[2] + [(self.size+2) + (self.size*i) + (j) for i in range(self.size)] for j in range(self.size)]
        group1 = [[1] + list(line) for line in np.array(group2).T[1:]]

        game = [start_card, group1, group2]
        for i, mol in enumerate(self.mols):
            game += [self.__convert_to_spotit(mol, i+3)]
        return game
    
    def __str__(self):
        """ return: string of full SpotIt! game """
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
        print("\n")

        
class SpotItToMOLS:
    """ 
    Conversion from SpotIt! game to its generating MOLS.
    param: game: type list (depth-3) of ints: [Starting Card, Group_1, ..., Group_N]
    """
    
    def __init__(self, game):
        self.game = game[3:]
        self.size = len(self.game[0])  # number of elements on a card
        self.mols = self.__compile_mols()
        
    def __convert_to_ls(self, group):
        """ 
        Takes a SpotIt! group and returns its latin square generator
        param: group: type list (depth-2) of ints: SpotIt! cards that have the same group number
        """
        latin_square = [[(num - (self.size+2) - self.size*i) for i, num in enumerate(line[1:])] for line in group]
        return latin_square
    
    def __compile_mols(self):
        """ return: type list (depth-3) of ints: """
        mols = [self.__convert_to_ls(self.game[i]) for i in range(len(self.game))]
        return mols
    
    def __str__(self):
        """ return: string of all mols """
        print("MOLS(" + str(self.size) + ")")
        print_mols = []
        for mol in self.mols:
            print_mols += [str(line) + "\n" for line in mol] + ["\n"]
        return "".join(print_mols)
    
    
class Check:
    """ 
    Different tests to verify if nxn tables are MOLS.
    param: tables: type< list(list(ints)) >: supposed latin squares 
    """
    
    def __init__(self, *tables):
        self.tables = tables
        self.size = len(tables[0]) 
        self.unique_pairs = self.__flatten([[(i, j) for i in range(10)] for j in range(10)])
        self.unique_nums = [i for i in range(self.size)]
        self.compiled = self.__compile(self, self.tables)
    
    @staticmethod
    def __flatten(table):
        return [tab for tab in itertools.chain.from_iterable(table)]
        
    def __compile(self, *tables):
        """ 
        Superimposes all tables onto each other. 
        param: tables: list of n tables
        return: compiled_table: list of length-n tuples
        """
        compiled_table = []
        for i in range(self.size):
            for table in itertools.zip_longest(*[table[i] for table in tables]):
                compiled_table += [table]
        return compiled_table
    
    def __repeated_pairs(self, pairs_list):
        """ Prints out all repeated pairs of a pairs list
            and its coordinates in relation to the non-compiled nxn table"""
        pairs = deepcopy(pairs_list)
        for pair in self.unique_pairs:
            if pairs.count(pair) > 1:  # if a pair is repeated
                idx_repeat_pairs = [idx for idx in range(len(pairs)) if pair == pairs[idx]]
                coord_repeat_pairs = [(idx % self.size, idx // self.size) for idx in idx_repeat_pairs]
                print("Repeated {} at (row, column): {}".format(pair, coord_repeat_pairs))
    
    @staticmethod
    def is_latin_square(table):
        """ Checks if a square is a latin square. """
        square = deepcopy(table)
        for row in square:
            if len(row) != len(set(row)):
                print("First repeated number in row {}".format(square.index(row)))
                return False
        print("No repeated numbers in rows.")
        
        square = list(np.array(table).T)
        for column in square:
            if len(column) != len(set(column)):
                print("First repeated number in column {}".format(square.index(column)))
                return False
        print("No repeated numbers in columns.")
        return True
    
    def is_orthogonal(self, table1, table2):
        """ Checks if two latin squares form Graeco-Latin square. """
        table = self.__compile(table1, table2)
        if len(table) == len(set(table)):
            return True
        self.__repeated_pairs(table)
        return False
        
    def is_mutually_orthog(self):
        """ Checks if all squares are mutually orthogonal latin squares. """
        for table in self.tables:
            if not self.is_latin_square(table):
                return False
        orthog = [self.is_orthogonal(table[0], table[1]) for table in itertools.combinations(self.tables, 2)]
        if False in orthog:
            return False
        return True        

