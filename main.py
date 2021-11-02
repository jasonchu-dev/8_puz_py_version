import Node
from UCS import ucs

puzzle = [[1, 4, 5], [2, 3, 7], [8, 0, 6]]
p = Node.node(puzzle)
p.print()
search = ucs(p)