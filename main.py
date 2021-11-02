from Node import node
from UCS import ucs

puzzle = [[1, 4, 5], [2, 3, 7], [8, 0, 6]]
p = node(puzzle)

search = ucs(p)