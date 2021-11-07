import copy
class node:
    def __init__(self, parent_puzzle, val):
        self.puzzle = parent_puzzle
        self.kids = []
        self.solution = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.i = 0
        self.j = 0
        self.parent = None
        self.g = 0 # distance away from initial
        self.h = 0 # estimated distance to goal
        self.f = 0 # heuristic total
        self.val = val # user input taken for which hueristic to calculate h

    def calc_h(self):
        num_in_place = 0
        for row in range(3):
            for col in range(3):
                num_in_place += 1
                if num_in_place == 9:
                    num_in_place = 0
                if self.puzzle[row][col] != num_in_place and self.puzzle[row][col] != 0:
                    found = False
                    if self.val == 2:
                        for row1 in range(3):
                            for col1 in range(3):
                                if self.solution[row1][col1] == self.puzzle[row][col]:
                                    self.h += abs(row1-row) + abs(col1-col)
                                    found = True
                                if found: break
                            if found: break
                        else: self.h += 1


    def get_i_j(self):
        found = False
        for self.i in range(3):
            for self.j in range(3):
                if self.puzzle[self.i][self.j] == 0:
                    found = True
                if found: break
            if found: break

    def goal(self):
        if self.puzzle == self.solution:
            return True

    def compare_puzzle(self, puzzle):
        if self.puzzle == puzzle:
            return True

    def move(self):
        self.get_i_j()
        self.r()
        self.l()
        self.d()
        self.u()
      
    def r(self):
        if self.j != 2:
            next_puzzle = copy.deepcopy(self.puzzle)
            next_puzzle[self.i][self.j+1], next_puzzle[self.i][self.j] = next_puzzle[self.i][self.j], next_puzzle[self.i][self.j+1]
            child = node(next_puzzle, self.val)
            if self.val != 1:
                child.calc_h()
            self.kids.append(child)
            child.parent = self

    def l(self):
        if self.j != 0:
            next_puzzle = copy.deepcopy(self.puzzle)
            next_puzzle[self.i][self.j-1], next_puzzle[self.i][self.j] = next_puzzle[self.i][self.j], next_puzzle[self.i][self.j-1]
            child = node(next_puzzle, self.val)
            if self.val != 1:
                child.calc_h()
            self.kids.append(child)
            child.parent = self

    def d(self):
        if self.i != 2:
            next_puzzle = copy.deepcopy(self.puzzle)
            next_puzzle[self.i][self.j], next_puzzle[self.i+1][self.j] = next_puzzle[self.i+1][self.j], next_puzzle[self.i][self.j]
            child = node(next_puzzle, self.val)
            if self.val != 1:
                child.calc_h()
            self.kids.append(child)
            child.parent = self

    def u(self):
        if self.i != 0:
            next_puzzle = copy.deepcopy(self.puzzle)
            next_puzzle[self.i][self.j], next_puzzle[self.i-1][self.j] = next_puzzle[self.i-1][self.j], next_puzzle[self.i][self.j]
            child = node(next_puzzle, self.val)
            if self.val != 1:
                child.calc_h()
            self.kids.append(child)
            child.parent = self