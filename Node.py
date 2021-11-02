from UCS import ucs

class node:
    def __init__(self, parent_puzzle):
        self.puzzle = parent_puzzle
        self.kids = []
        self.solution = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.i = 0
        self.j = 0
        self.parent = None

    def get_i_j(self):
        for self.i in range(3):
            for self.j in range(3):
                if self.puzzle[self.i][self.j] == 0: break

    def goal(self):
        if self.puzzle == self.solution: return True

    def move(self):
        self.r(self)
        self.l(self)
        self.d(self)
        self.u(self)

    def r(self):
        if self.j != 2:
            next_puzzle = self.puzzle
            next_puzzle[self.i][self.j+1], next_puzzle[self.i][self.j] = next_puzzle[self.i][self.j], next_puzzle[self.i][self.j+1]
            child = node(next_puzzle)
            self.kids.append(child)
            child.parent = self

    def l(self):
        if self.j != 0:
            next_puzzle = self.puzzle
            next_puzzle[self.i][self.j-1], next_puzzle[self.i][self.j] = next_puzzle[self.i][self.j], next_puzzle[self.i][self.j-1]
            child = node(next_puzzle)
            self.kids.append(child)
            child.parent = self

    def d(self):
        if self.i != 0:
            next_puzzle = self.puzzle
            next_puzzle[self.i][self.j], next_puzzle[self.i+1][self.j] = next_puzzle[self.i+1][self.j], next_puzzle[self.i][self.j]
            child = node(next_puzzle)
            self.kids.append(child)
            child.parent = self

    def u(self):
        if self.i != 0:
            next_puzzle = self.puzzle
            next_puzzle[self.i][self.j], next_puzzle[self.i-1][self.j] = next_puzzle[self.i-1][self.j], next_puzzle[self.i][self.j]
            child = node(next_puzzle)
            self.kids.append(child)
            child.parent = self

    def print(self):
        print(self.puzzle, '\n')

    # def same(self, parent_puzzle): # might need this
    #     if self.puzzle == parent_puzzle: return True