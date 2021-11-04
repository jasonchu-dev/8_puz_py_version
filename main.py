import copy

class ucs:
    def __init__(self, puzzle):
        self.queue = []
        self.checked = []
        self.puzzle = puzzle
        self.queue.append(self.puzzle)
        self.found = False
    
    # def runthrough(self):
        while range(len(self.queue)) != 0:
            curr = self.queue[0]
            if curr.goal(): # for root node that is solution
                print(curr.puzzle)
                break
            self.checked.append(curr)
            curr.move()
            for i in range(len(curr.kids)):
                kid = curr.kids[i]
                if kid.goal():
                    print(kid.puzzle)
                    while kid.parent != None:
                        kid = kid.parent
                        print(kid.puzzle)
                    self.found = True
                    break
                if not self.prev_encounter_check(self.queue, kid):
                    if not self.prev_encounter_check(self.checked, kid):
                        self.queue.append(kid)
                        ##################################################
                        for i in range(len(kid.puzzle)):
                            print(kid.puzzle[i])
                        print('\n')
                        ##################################################
            self.queue.pop(0)
            print("next\n")
            if self.found: break

class manhattan:
    def __init__(self, puzzle):
        self.queue = []
        self.checked = []
        self.puzzle = puzzle
        self.queue.append(self.puzzle)
        self.found = False
        self.g = 0 # number of steps taken
    
    # def runthrough(self):
        while range(len(self.queue)) != 0:
            curr = self.queue[0]
            if curr.goal(): # for the very root node that is solution
                print(curr.puzzle)
                break
            self.g += 1
            self.checked.append(curr)
            curr.move()
            estimation = []
            # for i in range(len(curr.kids)):
            #     curr.kids[i].f = self.g + curr.kids[i].h
            #     estimation.append(curr.kids[i].f)
            # minimum = min(estimation)
            kid = None
            self.calc_min_f(curr, estimation)
            if curr.parent == None: # for very root of node that has no parent, set heuristic
                curr.calc_h()
                curr.f = curr.h
            i = 0
            while i < len(curr.kids):
                if curr.f >= min(estimation): # and curr.kids[i].f == min(estimation):
                    kid = curr.kids[i]
                    if not self.prev_encounter_check(self.queue, kid):
                        if not self.prev_encounter_check(self.checked, kid):
                            self.queue.append(kid)
                            i += 1
                            ##################################################
                            for j in range(len(kid.puzzle)):
                                print(kid.puzzle[j])
                            print('\n')
                            ##################################################
                        else: 
                            curr.kids.pop(i)
                    else:
                        curr.kids.pop(i)
                else: i += 1
                if kid.goal():
                    print(kid.puzzle)
                    while kid.parent != None:
                        kid = kid.parent
                        print(kid.puzzle)
                    self.found = True
                    break
                self.queue.pop(0)
                print("next\n")
                if self.found: break

    def calc_min_f(self, curr, estimation):
        for i in range(len(curr.kids)):
            curr.kids[i].f = self.g + curr.kids[i].h
            estimation.append(curr.kids[i].f)

    def prev_encounter_check(self, list, kid):
        for node in range(len(list)):
            if kid.puzzle == list[node].puzzle:
                return True
        return False

class node:
    def __init__(self, parent_puzzle):
        self.puzzle = parent_puzzle
        self.kids = []
        self.solution = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.i = 0
        self.j = 0
        self.parent = None
        self.h = 0 # estimated distance to goal
        self.f = 0 # heuristic total

    def calc_h(self):
        num_in_place = 0
        for row in range(3):
            for col in range(3):
                num_in_place += 1
                if row == 2 and col == 2:
                    num_in_place = 0
                if self.puzzle[row][col] != num_in_place:
                    found = False
                    for row1 in range(3):
                        for col1 in range(3):
                            if self.solution[row1][col1] == self.puzzle[row][col]:
                                self.h += abs(row1-row) + abs(col1-col)
                                found = True
                            if found: break
                        if found: break

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
            child = node(next_puzzle)
            child.calc_h()
            self.kids.append(child)
            child.parent = self

    def l(self):
        if self.j != 0:
            next_puzzle = copy.deepcopy(self.puzzle)
            next_puzzle[self.i][self.j-1], next_puzzle[self.i][self.j] = next_puzzle[self.i][self.j], next_puzzle[self.i][self.j-1]
            child = node(next_puzzle)
            child.calc_h()
            self.kids.append(child)
            child.parent = self

    def d(self):
        if self.i != 2:
            next_puzzle = copy.deepcopy(self.puzzle)
            next_puzzle[self.i][self.j], next_puzzle[self.i+1][self.j] = next_puzzle[self.i+1][self.j], next_puzzle[self.i][self.j]
            child = node(next_puzzle)
            child.calc_h()
            self.kids.append(child)
            child.parent = self

    def u(self):
        if self.i != 0:
            next_puzzle = copy.deepcopy(self.puzzle)
            next_puzzle[self.i][self.j], next_puzzle[self.i-1][self.j] = next_puzzle[self.i-1][self.j], next_puzzle[self.i][self.j]
            child = node(next_puzzle)
            child.calc_h()
            self.kids.append(child)
            child.parent = self

    def print(self):
        print(self.puzzle, '\n')

    # def same(self, parent_puzzle): # might need this
    #     if self.puzzle == parent_puzzle: return True


puzzle = [
    [1, 3, 6], 
    [5, 0, 7], 
    [4, 8, 2]
]
if(manhattan(node(puzzle)).found == False):
    print("no solution found")