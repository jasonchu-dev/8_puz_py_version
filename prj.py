import random
    
class UCS:
    def __init__(self):
        self.queue = []
        self.checked = []
        self.path = []

    def add(self, node):
        self.list.append(node)

class Node:

    def __init__(self, parent_puzzle):
        self.puzzle = parent_puzzle
        self.queue = []
        self.solution = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.i = 0
        self.j = 0
        self.parent = None

    def get_i_j(self):
        for i in self.puzzle:
            for j in self.puzzle:
                if self.puzzle[i][j] is 0: break

    def goal(self):
        if self.puzzle == self.solution: return True

    def r(self):
        if self.j != 2:
            next_puzzle = self.puzzle
            next_puzzle[self.i][self.j+1], next_puzzle[self.i][self.j] = next_puzzle[self.i][self.j], next_puzzle[self.i][self.j+1]
            child = Node(next_puzzle)
            self.queue.append(child)
            child.parent = self

    def l(self):
        if self.j != 0:
            next_puzzle = self.puzzle
            next_puzzle[self.i][self.j-1], next_puzzle[self.i][self.j] = next_puzzle[self.i][self.j], next_puzzle[self.i][self.j-1]
            child = Node(next_puzzle)
            self.queue.append(child)
            child.parent = self

    def d(self):
        if self.i != 0:
            next_puzzle = self.puzzle
            next_puzzle[self.i][self.j], next_puzzle[self.i+1][self.j] = next_puzzle[self.i+1][self.j], next_puzzle[self.i][self.j]
            child = Node(next_puzzle)
            self.queue.append(child)
            child.parent = self

    def u(self):
        if self.i != 0:
            next_puzzle = self.puzzle
            next_puzzle[self.i][self.j], next_puzzle[self.i-1][self.j] = next_puzzle[self.i-1][self.j], next_puzzle[self.i][self.j]
            child = Node(next_puzzle)
            self.queue.append(child)
            child.parent = self

    def print(self):
        print(self.puzzle, '\n')

    # def same(self, parent_puzzle): # might need this
    #     if self.puzzle == parent_puzzle: return True


puzzle = [[1, 4, 5], [2, 3, 7], [8, 0, 6]]
p = Node(puzzle)

