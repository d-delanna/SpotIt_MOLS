import itertools
import numpy as np

# TODO: add comments for SpotIt_to_MOLS

class MOLS_to_SpotIt:
    
    # TODO: should make copies of MOLS instead of directly mutating
    """ Converts a set of MOLS of any siz and converts them to SpotIt! cards. 
        param: mols: type< list(list(ints)) >: latin squares """
    
    def __init__(self, *mols):
        self.mols = mols
        self.size = len(mols[0])
        
    def convert_to_spotit(self, square, group_num):
        """ converts single latin square to group """
        for line in square:
            for i in range(self.size):
                line[i] = line[i] + (self.size+2) + self.size*i
            line.insert(0, group_num)
        return square
        
    def full_game(self):
        """ compiles full game into list containing all cards """
        start_card = [[i+1 for i in range(self.size+1)]]
        group2 = [[2] + [(self.size+2) + (self.size*i) + (j) for i in range(self.size)] for j in range(self.size)]
        group1 = [[1]+list(line) for line in np.array(self.group2).T[1:]]

        self.game = [start_card, group1, self.group2]
        for i, mol in enumerate(self.mols):
            self.game += [self.convert_to_spotit(mol, i+3)]
        return self.game
    
    def __str__(self):
        """ prints full SpotIt! game """
        print("SpotIt Game")
        for group in self.full_game():
            [print(line) for line in group]
            print('\n')
        return str(self.full_game())
        
    def print_group(self, group_num):
        """ prints single group """
        print("Group", group_num)
        [print(line) for line in self.full_game()[group_num]]
        print('\n')

 class SpotIt_to_MOLS:
    def __init__(self, game):
        self.game = game[2:]
        self.size = len(self.game[0])
        
    def convert_to_ls(self, group):
        latin_square = [[(num - (self.size+2) - self.size*i) for i, num in enumerate(line[1:])] for line in group]
        return latin_square
    
    def compile_mols(self):
        self.mols = [self.convert_to_ls(self.game[i]) for i in range(len(self.game))]
        return self.mols
    
    def __str__(self):
        print("MOLS(" + str(self.size) + ")")
        for mol in self.compile_mols():
            [print(line) for line in mol]
            print('\n')
        return str(self.compile_mols())
    

class Check:
    """ tests to verify if nxn tables are MOLS 
        param: tables: type< list(list(ints)): supposed latin squares """
    
    def __init__(self, *tables):
        self.tables = tables
        self.size = len(tables[0])
        
    def __compile(self, table1, table2):
        return [[table for table in itertools.zip_longest(table1[i], table2[i])] for i in range(self.size)]
    
    def __flatten(self, table):
        return [tab for tab in itertools.chain.from_iterable(table)]
        
    def latin_square(self, table):
        """ checks if a square is a latin square"""
        for row in table:
            if len(row) != len(set(row)):
                return False
        for column in np.array(table).T:
            if len(column) != len(set(column)):
                return False
        return True
    
    def __repeated_pairs(self, table):
        """ if not orthogonal, will print out all repeated pairs """
        if table != []:
            if table.count(table[0]) > 1:
                repeat_pairs = [idx for idx in range(len(table)) if table[idx] == table[0]]
                coord_repeat_pairs = [(idx%self.size, idx//self.size) for idx in repeat_pairs]
                print("Repeated {} at (row, column): {}".format(table[0], coord_repeat_pairs))
                [table.pop(idx) for idx in repeat_pairs[::-1]]
            return self.__repeated_pairs(table)
    
    def orthogonal(self, table1, table2):
        """ checks if two latin squares form Graeco-Latin square """
        table = self.__flatten(self.__compile(table1, table2))
        if len(table) == len(set(table)):
            return True
        self.__repeated_pairs(table)
        return False
        
    def mutually_orthog(self):
        """ checks if all squares are mutually orthogonal latin squares """
        for table in self.tables:
            if not self.latin_square(table):
                return False
        orthog = [self.orthogonal(tab[0], tab[1]) for tab in itertools.combinations(self.tables,2)]
        if False in orthog:
            return False
        return True   
        
 # EXAMPLE MOLS ---------------------------------------------
 # LS3 and LS4 orthogonal
 # LS3 and LS4 orthogonal
 # LS4 and LS5 not orthogonal
 
 LS3 = [
    [0, 8, 9, 7, 5, 6, 4, 2, 3, 1],
    [9, 1, 4, 6, 2, 7, 3, 8, 0, 5],
    [7, 4, 2, 5, 1, 3, 8, 6, 9, 0],
    [8, 6, 5, 3, 9, 2, 1, 0, 4, 7],
    [6, 2, 1, 8, 4, 0, 9, 5, 7, 3],
    [4, 9, 3, 2, 7, 5, 0, 1, 6, 8],
    [5, 3, 7, 1, 0, 8, 6, 9, 2, 4],
    [3, 5, 0, 9, 8, 4, 2, 7, 1, 6],
    [1, 7, 6, 0, 3, 9, 5, 4, 8, 2],
    [2, 0, 8, 4, 6, 1, 7, 3, 5, 9]
]

LS4 = [   
    [0, 7, 8, 9, 1, 2, 3, 4, 5, 6],
    [9, 0, 6, 1, 8, 3, 2, 5, 4, 7],
    [7, 2, 0, 4, 3, 9, 1, 8, 6, 5],
    [8, 5, 3, 0, 2, 1, 7, 6, 9, 4],
    [6, 9, 5, 3, 0, 7, 4, 2, 1, 8],
    [4, 1, 7, 6, 5, 0, 8, 9, 3, 2],
    [5, 4, 2, 8, 9, 6, 0, 3, 7, 1],
    [3, 6, 1, 7, 4, 8, 5, 0, 2, 9],
    [1, 8, 4, 2, 6, 5, 9, 7, 0, 3],
    [2, 3, 9, 5, 7, 4, 6, 1, 8, 0]
]

LS5 = [   
    [0, 7, 8, 9, 1, 2, 3, 4, 5, 6],
    [6, 4, 2, 8, 9, 5, 1, 3, 7, 0],
    [4, 9, 5, 3, 2, 7, 6, 0, 1, 8],
    [5, 1, 7, 6, 4, 3, 8, 9, 0, 2],
    [3, 2, 9, 0, 7, 1, 5, 6, 8, 4],
    [1, 0, 3, 7, 6, 8, 2, 5, 4, 9],
    [2, 8, 0, 1, 3, 4, 9, 7, 6, 5],
    [9, 5, 4, 2, 8, 6, 0, 1, 3, 7],
    [7, 3, 6, 5, 0, 9, 4, 8, 2, 1],
    [8, 6, 1, 4, 5, 0, 7, 2, 9, 3]
]

game = MOLS_to_SpotIt(LS3, LS4)
print(game)

mols = SpotIt_to_MOLS(LS3, LS4)
print(mols)  # should return back to original form

check = Check(LS3, LS4, LS5)
print(check.orthogonal(LS3, LS4)
print(check.orthogonal(LS3, LS5)
print(check.orthogonal(LS4, LS5)

