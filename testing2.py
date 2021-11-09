import heapq
import time
import copy
# variables for main to print
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
        # initial puzzle into queue
        self.queue.append(self.puzzle)
        self.found = False
        global start_time
        global finish_time
        global expanded
        global q_size
    
        # i would think clock starts here the moment first node is in queue    
        start_time = time.time()
        # nothing in queue? then return false for no solution
        if len(self.queue) == 0: return False
        # but if there is, then continue checking for a solution
        while range(len(self.queue)) != 0:
        # grab and track record queue size
            if q_size < len(self.queue):
                q_size = len(self.queue)
            # check the smallest object
            curr = self.queue[0]
            # is it a goal?
            if curr.goal():
                # the moment goal is found, then timer for search stops
                finish_time = time.time() - start_time
                # start traversing back to add solution
                path.append(curr)
                while curr.parent != None:
                    curr = curr.parent
                    path.insert(0, curr)
                # checked already, put in here
                self.checked.append(curr)
                # true if solution is found
                self.found = True
                # now get out of this class
                break
            # checked already, put in here
            self.checked.append(curr)
            # for very root of node that has no parent, set heuristic
            if curr.parent == None: 
                curr.f = curr.h # or 0 since root is at depth 0
            # expand
            curr.move()
            # check parent objects to calculate heuristics and to check whether it should be appended to queue to avoid repeats
            for i in range(len(curr.kids)):
                kid = curr.kids[i]
                # track number of nodes expanded
                expanded += 1
                # heuristics calculation
                kid.g = kid.parent.g + 1
                kid.f = kid.g + kid.h
                # repeat object?
                if not self.prev_encounter_check(self.queue, kid) and not self.prev_encounter_check(self.checked, kid):
                    # then add
                    self.queue.append(kid)
            # take object out of queue since we are done checking it
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
        global start_time
        global finish_time
        global expanded
        global q_size

        start_time = time.time() # i would think clock starts here the moment first node is in queue
        while range(len(self.queue)) != 0:
            heapq.heapify(self.queue)
            if q_size < len(self.queue):
                q_size = len(self.queue)
            curr = heapq.heappop(self.queue)
            if curr.goal():
                finish_time = time.time() - start_time
                path.append(curr)
                while curr.parent != None:
                    curr = curr.parent
                    path.insert(0, curr)
                self.checked.append(curr)
                self.found = True
                break
            self.checked.append(curr)
            if curr.parent == None: # for very root of node that has no parent, set heuristic
                curr.calc_h()
                curr.f = curr.h
            curr.move()
            for i in range(len(curr.kids)):
                kid = curr.kids[i]
                expanded += 1 # not sure if this includes repeat nodes
                kid.g = kid.parent.g + 1
                kid.f = kid.g + kid.h
                if not self.prev_encounter_check(self.queue, kid) and not self.prev_encounter_check(self.checked, kid):
                    heapq.heappush(self.queue, kid)

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
        self.h = 0 # estimated distance to goal
        self.g = 0 # cost from initial
        self.f = 0 # heuristic total
        self.val = val # user input taken for which hueristic to calculate h

    def __lt__(self, other):
        return self.f < other.f

    def calc_h(self):
        for row in range(3):
            for col in range(3):
                if self.puzzle[row][col] != self.solution[row][col] and self.puzzle[row][col] != 0:
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

x, y = 3, 3
puzzle = [[0 for i in range(x)] for j in range(y)]
spot = 0

print("\nFill in the array:\n")

for i in range(len(puzzle)):
    for j in range(len(puzzle)):
        spot += 1
        print("spot", spot)
        puzzle[i][j] = int(input())
        
print('\n')
for i in range(len(puzzle)):
    print(puzzle[i])

print("\n")
val = int(input("Press 1 for Uniform Cost Search\nPress 2 for A* with Manhattan Distance heuristic\nPress 3 for A* with Misplaced Tiles heuristic\n"))

print("Please wait...")

p = node(puzzle, val)
search = None
str = ""

if val == 2 or val == 3:
    if val == 2:
        str = "A* with Manhattan Distance heuristic\n"
    else: str = "A* with Misplaced Tiles heuristic\n"
    search = a_star(p)
else: 
    str = "Uniform Cost Search\n"
    search = ucs(p)

if not search.found:
        print("\nNo solution found\n")
else:
    print("\nSolution:\n")
    for i in range(len(path)):
        print("Depth:", i)
        print("g(n) =", path[i].g)
        print("h(n) =", path[i].h)
        for j in range(len(path[i].puzzle)):
            print(path[i].puzzle[j])
        print('\n')
    print(str)
    print("Nodes expanded:", expanded)
    print("Max queue size:", q_size)
    print("Time in sec:", finish_time)

print("\nProgram simulated and tested on:\nIntel(R) Core(TM) i5-7300HQ CPU @ 2.50GHz\n")