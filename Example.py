from SpotIt_MOLS.SpotItGame import *
from SpotIt_MOLS.LatinSquares import *

# Example

spotit4 = MOLSToSpotIt(ls4)
print(spotit4)

# SpotIt Game
# [1, 2, 3, 4, 5]
#
# [1, 6, 10, 14, 18]
# [1, 7, 11, 15, 19]
# [1, 8, 12, 16, 20]
# [1, 9, 13, 17, 21]
#
# [2, 6, 11, 17, 20]
# [2, 7, 10, 16, 21]
# [2, 8, 13, 15, 18]
# [2, 9, 12, 14, 19]
#
# [3, 6, 12, 15, 21]
# [3, 7, 13, 14, 20]
# [3, 8, 10, 17, 19]
# [3, 9, 11, 16, 18]
#
# [4, 6, 13, 16, 19]
# [4, 7, 12, 17, 18]
# [4, 8, 11, 14, 21]
# [4, 9, 10, 15, 20]

print(spotit4.group(1))

# Group 1
# [1, 6, 10, 14, 18]
# [1, 7, 11, 15, 19]
# [1, 8, 12, 16, 20]
# [1, 9, 13, 17, 21]

print("Is a SpotIt! game:", CheckSpotIt(spotit4).is_spotit)
# Is a SpotIt! game: True

mols4 = SpotItToMOLS(spotit4)
print(mols4)

# MOLS(4)
# [0, 1, 2, 3]
# [1, 0, 3, 2]
# [2, 3, 0, 1]
# [3, 2, 1, 0]
#
# [0, 1, 2, 3]
# [3, 2, 1, 0]
# [1, 0, 3, 2]
# [2, 3, 0, 1]
#
# [0, 1, 2, 3]
# [2, 3, 0, 1]
# [3, 2, 1, 0]
# [1, 0, 3, 2]

check1 = CheckMOLS(mols4)
print("Is a latin square:", check1.is_ls(LS4_1))
# Is a latin square: True

print("Are orthogonal:", check1.are_orthog(LS4_1, LS4_2))
# Are orthogonal: True

print("Are a set of MOLS:", check1.are_mols())
# Are a set of MOLS: True

# -----------------------------------------------------------------

# Non-Example

notls = [
    [0, 1, 2, 3],
    [0, 1, 3, 2],
    [2, 3, 0, 1],
    [3, 2, 1, 0]
]
not_mols4 = [LS4_1, notls, LS4_3]
check2 = CheckMOLS(not_mols4, report_steps=True)

print(check2.is_ls(notls))
# First repeated number in column 0
# False

print(check2.are_orthog(notls, LS4_3))
# Repeated (0, 1) at (row, column): [(0, 1), (2, 2)]
# Repeated (1, 3) at (row, column): [(1, 1), (3, 2)]
# False

print(check2.are_mols())
# Checking Latin Square 1
#
# Checking Latin Square 2
# First repeated number in column 0
# False




