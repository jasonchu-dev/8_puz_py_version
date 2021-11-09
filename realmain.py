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
    
        # clock starts here the moment first node is in queue    
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
        # iterate through queue and checked for repeats
        for node in range(len(list)):
            if kid.puzzle == list[node].puzzle:
                # dont append if repeat
                return True
        # return false if no repeat
        return False

class a_star:
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
        
        # clock starts here the moment first node is in queue
        start_time = time.time()
        # nothing in queue? then return false for no solution
        if len(self.queue) == 0: return False
        # but if there is, then continue checking for a solution
        while range(len(self.queue)) != 0:
        # grab and track record queue size
            heapq.heapify(self.queue)
            if q_size < len(self.queue):
                q_size = len(self.queue)
            # check the smallest object
            curr = heapq.heappop(self.queue)
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
                curr.calc_h()
                curr.f = curr.h # or 0 since root is at depth 0
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
                    heapq.heappush(self.queue, kid)

    def prev_encounter_check(self, list, kid):
        # iterate through queue and checked for repeats
        for node in range(len(list)):
            if kid.puzzle == list[node].puzzle:
                # dont append if repeat
                return True
        # return false if no repeat
        return False

class node:
    def __init__(self, parent_puzzle, val):
        self.puzzle = parent_puzzle # get input of the puzzle from root or previous object
        self.kids = [] # parent might have kids
        self.solution = [[1, 2, 3], [4, 5, 6], [7, 8, 0]] # change here for nxn
        self.i = 0
        self.j = 0
        self.parent = None
        self.h = 0 # estimated distance to goal
        self.g = 0 # cost from initial
        self.f = 0 # heuristic total
        self.val = val # user input taken for which hueristic to calculate h

    # special function to overide iteration system in heapq module
    def __lt__(self, other):
        return self.f < other.f

    # calculate h(n)
    def calc_h(self):
        for row in range(3):
            for col in range(3):
                # is this tile in the right place?
                if self.puzzle[row][col] != self.solution[row][col] and self.puzzle[row][col] != 0:
                    found = False
                    # if not then find the distance
                    if self.val == 2:
                        for row1 in range(3):
                            for col1 in range(3):
                                # find position of where it needs to go
                                if self.solution[row1][col1] == self.puzzle[row][col]:
                                    # calculate h(n) and append for others
                                    self.h += abs(row1-row) + abs(col1-col)
                                    # break loop to save time and move on to next object with bool
                                    found = True
                                if found: break
                            if found: break
                    # or if misplaced then just count the tile
                    else: self.h += 1

    # find blank tile spot to prep for switching
    def get_i_j(self):
        found = False
        # iterate to find 0
        for self.i in range(3):
            for self.j in range(3):
                if self.puzzle[self.i][self.j] == 0:
                    found = True
                # get out the moment its found to save time
                if found: break
            if found: break

    # if goal then save time and get out of search
    def goal(self):
        if self.puzzle == self.solution:
            return True

    # func to make kids and expand
    def move(self):
        # get blank spot
        self.get_i_j()
        self.r()
        self.l()
        self.d()
        self.u()
      
    # go right  
    def r(self):
        # can't go right?
        if self.j != 2:
            # copy so it doesn't just make a pointer to object which will affect its attributes in long run
            next_puzzle = copy.deepcopy(self.puzzle)
            # swap
            next_puzzle[self.i][self.j+1], next_puzzle[self.i][self.j] = next_puzzle[self.i][self.j], next_puzzle[self.i][self.j+1]
            child = node(next_puzzle, self.val)
            # no need to calc h(n) if UCS
            if self.val != 1:
                child.calc_h()
            # correlate child to parent by appending and pointing
            self.kids.append(child)
            child.parent = self

    # go left 
    def l(self):
        # can't go left?
        if self.j != 0:
            # copy so it doesn't just make a pointer to object which will affect its attributes in long run
            next_puzzle = copy.deepcopy(self.puzzle)
            # swap
            next_puzzle[self.i][self.j-1], next_puzzle[self.i][self.j] = next_puzzle[self.i][self.j], next_puzzle[self.i][self.j-1]
            # produce child
            child = node(next_puzzle, self.val)
            # no need to calc h(n) if UCS
            if self.val != 1:
                child.calc_h()
            # correlate child to parent by appending and pointing
            self.kids.append(child)
            child.parent = self

    # go down 
    def d(self):
        # can't go down?
        if self.i != 2:
            # copy so it doesn't just make a pointer to object which will affect its attributes in long run
            next_puzzle = copy.deepcopy(self.puzzle)
            # swap
            next_puzzle[self.i][self.j], next_puzzle[self.i+1][self.j] = next_puzzle[self.i+1][self.j], next_puzzle[self.i][self.j]
            # produce child
            child = node(next_puzzle, self.val)
            # no need to calc h(n) if UCS
            if self.val != 1:
                child.calc_h()
            # correlate child to parent by appending and pointing
            self.kids.append(child)
            child.parent = self

    # go up 
    def u(self):
        # can't go up?
        if self.i != 0:
            # copy so it doesn't just make a pointer to object which will affect its attributes in long run
            next_puzzle = copy.deepcopy(self.puzzle)
            # swap
            next_puzzle[self.i][self.j], next_puzzle[self.i-1][self.j] = next_puzzle[self.i-1][self.j], next_puzzle[self.i][self.j]
            # produce child
            child = node(next_puzzle, self.val)
            # no need to calc h(n) if UCS
            if self.val != 1:
                child.calc_h()
            # correlate child to parent by appending and pointing
            self.kids.append(child)
            child.parent = self

# set up blank array
x, y = 3, 3 # change here for nxn
puzzle = [[0 for i in range(x)] for j in range(y)]
spot = 0
# saved list of user inputs to prevent repeat values
userinput = []
# prompt user
print("\nFill in the array:\n")

# fill array with user input
for i in range(len(puzzle)):
    for j in range(len(puzzle)):
        spot += 1
        print("spot", spot)
        # check for valid inputs or repeat number
        while True:
            inp = int(input())
            if -1 < inp < 9 and not inp in userinput: # change here for nxn
                puzzle[i][j] = inp
                # if valid, append and break
                userinput.append(inp)
                break
            # if not, keep looping
            else:
                print("Invalid or already added, try again")
        
# print puzzle for user reference
print('\n')
for i in range(len(puzzle)):
    print(puzzle[i])

# what does the user want?
print("\n")
val = int(input("Press 1 for Uniform Cost Search\nPress 2 for A* with Manhattan Distance heuristic\nPress 3 for A* with Misplaced Tiles heuristic\n"))

# tell to wait
print("Please wait...")

# produce node object
p = node(puzzle, val)
search = None
str = ""

# Which A*?
if val == 2 or val == 3:
    if val == 2:
        str = "A* with Manhattan Distance heuristic\n"
    else: str = "A* with Misplaced Tiles heuristic\n"
    # make the search object to start its work
    search = a_star(p)
# UCS
else: 
    str = "Uniform Cost Search\n"
    # make the search object to start its work
    search = ucs(p)

# nothing? then no solution
if not search.found:
        print("\nNo solution found\n")
else:
    print("\nSolution:\n")
    # traverse through solution list
    for i in range(len(path)):
        # print out attributes of each node object
        print("Depth:", i)
        print("g(n) =", path[i].g)
        print("h(n) =", path[i].h)
        for j in range(len(path[i].puzzle)):
            print(path[i].puzzle[j])
        print('\n')

    # print out specs of search object
    print(str)
    print("Nodes expanded:", expanded)
    print("Max queue size:", q_size)
    print("Time in sec:", finish_time)

print("\nBy Jason Chu")
print("Program simulated and tested on:\nIntel(R) Core(TM) i5-7300HQ CPU @ 2.50GHz\n")