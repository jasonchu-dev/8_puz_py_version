import collections
import cpuinfo
import time
import copy
path = []
expanded = 0
q_size = 0
start_time = 0
finish_time = 0

class ucs:
    def __init__(self, puzzle):
        self.queue = []
        self.checked = []
        self.puzzle = puzzle
        self.queue.append(self.puzzle)
        self.found = False
        self.num_of_nodes = 0
        global start_time
        global finish_time
        global expanded
        global q_size
    
        start_time = time.time() # i would think clock starts here the moment first node is in queue
        while range(len(self.queue)) != 0:
            if q_size < len(self.queue):
                q_size = len(self.queue)
            curr = self.queue[0]
            if curr.goal():
                finish_time = time.time() - start_time
                path.append(curr.puzzle)
                while curr.parent != None:
                    curr = curr.parent
                    path.insert(0, curr.puzzle)
                self.checked.append(curr)
                self.found = True
                break
            self.checked.append(curr)
            curr.move()
            for i in range(len(curr.kids)):
                kid = curr.kids[i]
                expanded += 1 # not sure if this includes repeat nodes
                if not self.prev_encounter_check(self.queue, kid) and not self.prev_encounter_check(self.checked, kid):
                    self.queue.append(kid)
            del self.queue[0]

    def prev_encounter_check(self, list, kid):
        for node in range(len(list)):
            if kid.puzzle == list[node].puzzle:
                return True
        return False

class a_star:
    def __init__(self, puzzle):
        self.queue = []
        self.checked = []
        self.puzzle = puzzle
        self.queue.append(self.puzzle)
        self.found = False
        self.g = 0 # number of steps taken
        global start_time
        global finish_time
        global expanded
        global q_size

        start_time = time.time() # i would think clock starts here the moment first node is in queue
        while range(len(self.queue)) != 0:
            if q_size < len(self.queue):
                q_size = len(self.queue)
            self.queue = collections.deque(sorted(list(self.queue), key=lambda node : node.f))
            curr = self.queue[0]
            if curr.goal():
                finish_time = time.time() - start_time
                path.append(curr.puzzle)
                while curr.parent != None:
                    curr = curr.parent
                    path.insert(0, curr.puzzle)
                self.checked.append(curr)
                self.found = True
                break
            self.checked.append(curr)
            if curr.parent == None: # for very root of node that has no parent, set heuristic
                curr.calc_h()
                curr.f = curr.h
            self.g += 1
            curr.move()
            for i in range(len(curr.kids)):
                kid = curr.kids[i]
                expanded += 1 # not sure if this includes repeat nodes
                kid.g = self.g
                kid.f = kid.g + kid.h
                if not self.prev_encounter_check(self.queue, kid) and not self.prev_encounter_check(self.checked, kid):
                    self.queue.append(kid)
            del self.queue[0]

    def prev_encounter_check(self, list, kid):
        for node in range(len(list)):
            if kid.puzzle == list[node].puzzle:
                return True
        return False

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

# 1: UCS
# 2: Manhattan
# 3: Misplaced

val = 3
puzzle = [
    [1, 3, 6], 
    [5, 0, 2], 
    [4, 7, 8]
]
if val == 1: print("\nUCS\n")
elif val == 2: print("\nManhattan\n")
else: print("\nMisplaced\n")
print("Testing in progress...")

if not a_star(node(puzzle, val)).found: # change ucs or a_star
    print("\nNo solution found\n")
else:
    print("\nSolution:\n")
    for i in range(len(path)):
        print("Depth:", i)
        for j in range(len(path[i])):
            print(path[i][j])
        print('\n')
if val == 1: print("UCS")
elif val == 2: print("Manhattan")
else: print("Misplaced")
print("Nodes expanded:", expanded)
print("Max queue size:", q_size)
print("Time in sec:", finish_time)

print("\nExecuted on:\n", cpuinfo.get_cpu_info()['brand_raw'], '\n')