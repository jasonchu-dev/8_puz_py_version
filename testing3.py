import collections
import cpuinfo
import heapq
import time
import copy
path = []
expanded = 0
q_size = 0
test_q = []
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
        global test_q
    
        start_time = time.time() # i would think clock starts here the moment first node is in queue
        while range(len(self.queue)) != 0:
            if q_size < len(self.queue):
                q_size = len(self.queue)
            #####################################
            test_q.insert(0, self.queue)
            #####################################
            curr = self.queue[0]
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
                curr.f = curr.h # or 0 since root is at depth 0
            curr.move()
            # print("next\n")
            for i in range(len(curr.kids)):
                kid = curr.kids[i]
                # ##############################################
                # for i in range(len(kid.puzzle)):
                #     print(kid.puzzle[i])
                # print('\n')
                # ##############################################
                expanded += 1 # not sure if this includes repeat nodes
                kid.g = kid.parent.g + 1
                kid.f = kid.g + kid.h
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
        global start_time
        global finish_time
        global expanded
        global q_size
        global test_q

        start_time = time.time() # i would think clock starts here the moment first node is in queue
        while range(len(self.queue)) != 0:
            heapq.heapify(self.queue)
            if q_size < len(self.queue):
                q_size = len(self.queue)
            # just for other tests
            # test_q.append(self.queue)
            # print(test_q[0])
            # #####################################
            curr = heapq.heappop(self.queue)
            if curr.goal():
                finish_time = time.time() - start_time
                path.append(curr)
                # print (curr.f, curr.puzzle, 'h(n)="{}" g(n)="{}" f(n)="{}"' .format(curr.h, curr.g, curr.f))
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
            # print(curr.f, curr.puzzle)
            # print (curr.f, curr.puzzle, 'h(n)= {} g(n)= {}' .format(curr.h, curr.g))
            # "10"
            curr.move() # expand
            for i in range(len(curr.kids)):
                kid = curr.kids[i]
                # loop is just for other tests
                # for i in range(len(kid)):
                #     for j in range(len(kid[i])):
                #         print(kid[i].puzzle[j])
                #     print('\n')
                # ##############################################
                expanded += 1 # increment expand count
                kid.g = kid.parent.g + 1
                kid.f = kid.g + kid.h
                if not self.prev_encounter_check(self.queue, kid) and not self.prev_encounter_check(self.checked, kid):
                    heapq.heappush(self.queue, kid)
            # del self.queue[0]

    def prev_encounter_check(self, list, kid):
        for node in range(len(list)):
            if kid.puzzle == list[node].puzzle:
                return True
        return False

class node:
    def __init__(self, parent_puzzle, val: int):
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
                    if self.val == 2: # manhattan distance, calculate distance
                        for row1 in range(3):
                            for col1 in range(3):
                                if self.solution[row1][col1] == self.puzzle[row][col]:
                                    self.h += abs(row1-row) + abs(col1-col)
                                    found = True
                                if found: break
                            if found: break
                    else: self.h += 1 # misplaced tiles, just increment if misplaced is encountered

    def get_i_j(self): # find where 0 is to set up for swapping
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
            if self.val != 1: # if ucs
                child.calc_h()
            self.kids.append(child)
            child.parent = self

    def l(self):
        if self.j != 0:
            next_puzzle = copy.deepcopy(self.puzzle)
            next_puzzle[self.i][self.j-1], next_puzzle[self.i][self.j] = next_puzzle[self.i][self.j], next_puzzle[self.i][self.j-1]
            child = node(next_puzzle, self.val)
            if self.val != 1: # if ucs
                child.calc_h()
            self.kids.append(child)
            child.parent = self

    def d(self):
        if self.i != 2:
            next_puzzle = copy.deepcopy(self.puzzle)
            next_puzzle[self.i][self.j], next_puzzle[self.i+1][self.j] = next_puzzle[self.i+1][self.j], next_puzzle[self.i][self.j]
            child = node(next_puzzle, self.val)
            if self.val != 1: # if ucs
                child.calc_h()
            self.kids.append(child)
            child.parent = self

    def u(self):
        if self.i != 0:
            next_puzzle = copy.deepcopy(self.puzzle)
            next_puzzle[self.i][self.j], next_puzzle[self.i-1][self.j] = next_puzzle[self.i-1][self.j], next_puzzle[self.i][self.j]
            child = node(next_puzzle, self.val)
            if self.val != 1: # if ucs
                child.calc_h()
            self.kids.append(child)
            child.parent = self

# 1: UCS
# 2: Manhattan
# 3: Misplaced

# # Depth: 0
# puzzle = [
#     [1, 2, 3], 
#     [4, 5, 6], 
#     [7, 8, 0]
# ]

# # Depth: 2
# puzzle = [
#     [1, 2, 3], 
#     [4, 5, 6], 
#     [0, 7, 8]
# ]

# # Depth 4:
# puzzle = [
#     [1, 2, 3], 
#     [5, 0, 6], 
#     [4, 7, 8]
# ]

# # Depth 8:
# puzzle = [
#     [1, 3, 6], 
#     [5, 0, 2], 
#     [4, 7, 8]
# ]

# # Depth 12:
# puzzle = [
#     [1, 3, 6], 
#     [5, 0, 7], 
#     [4, 8, 2]
# ]

# Depth 16:
puzzle = [
    [1, 6, 7], 
    [5, 0, 3], 
    [4, 8, 2]
]

# # Depth 20:
# puzzle = [
#     [7, 1, 2], 
#     [4, 8, 5], 
#     [6, 3, 0]
# ]

# # Depth 24:
# puzzle = [
#     [0, 7, 2], 
#     [4, 6, 1], 
#     [3, 5, 8]
# ]

print("\n")
val = int(input("1 for UCS\n2 for Manhattan Distance\n3 for Misplaced\n"))

print("Testing in progress...")

p = node(puzzle, val)
search = None
str = ""

if val == 2 or val == 3:
    if val == 2:
        str = "Manhattan Distance\n"
    else: str = "Misplaced Tiles\n"
    search = a_star(p)
else: 
    str = "UCS\n"
    search = ucs(p)

if not search.found:
        print("\nNo solution found\n")
else:
    print("\nSolution:\n")
    for i in range(len(path)):
        print("Depth:", i)
        print("g(n):", path[i].g)
        print("h(n):", path[i].h)
        print("f(n):", path[i].f)
        for j in range(len(path[i].puzzle)):
            print(path[i].puzzle[j])
        print('\n')
    print(str)
    print("Nodes expanded:", expanded)
    print("Max queue size:", q_size)
    print("Time in sec:", finish_time)

print("\nExecuted on:\n", cpuinfo.get_cpu_info()['brand_raw'], '\n')