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

    def prev_encounter_check(self, list, kid):
        for node in range(len(list)):
            if kid.puzzle == list[node].puzzle:
                return True
        # for node in list:
        #     if node.compare_puzzle(kid): 
        #         print("fgkjhdfkjhgfkjdj") ###################################################################
        #         return True
        return False

class node:
    def __init__(self, parent_puzzle):
        self.puzzle = parent_puzzle
        self.kids = []
        self.solution = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.i = 0
        self.j = 0
        self.parent = None

    def get_i_j(self):
        found = False
        for self.i in range(3):
            for self.j in range(3):
                if self.puzzle[self.i][self.j] == 0:
                    found = True
                if found: break
            if found: break

    def goal(self):
        # for row in range(len(self.puzzle)):
        #     for col in range(len(self.puzzle[row])):
        #         if self.puzzle[row][col] != self.solution[row][col]: return False
        # return True
        if self.puzzle == self.solution:
            return True

    def compare_puzzle(self, puzzle):
        # for row in range(len(self.puzzle)):
        #     for col in range(len(self.puzzle[row])):
        #         if self.puzzle[row][col] != puzzleb.puzzle[row][col]: return False
        # return True
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
            self.kids.append(child)
            child.parent = self

    def l(self):
        if self.j != 0:
            next_puzzle = copy.deepcopy(self.puzzle)
            next_puzzle[self.i][self.j-1], next_puzzle[self.i][self.j] = next_puzzle[self.i][self.j], next_puzzle[self.i][self.j-1]
            child = node(next_puzzle)
            self.kids.append(child)
            child.parent = self

    def d(self):
        if self.i != 2:
            next_puzzle = copy.deepcopy(self.puzzle)
            next_puzzle[self.i][self.j], next_puzzle[self.i+1][self.j] = next_puzzle[self.i+1][self.j], next_puzzle[self.i][self.j]
            child = node(next_puzzle)
            self.kids.append(child)
            child.parent = self

    def u(self):
        if self.i != 0:
            next_puzzle = copy.deepcopy(self.puzzle)
            next_puzzle[self.i][self.j], next_puzzle[self.i-1][self.j] = next_puzzle[self.i-1][self.j], next_puzzle[self.i][self.j]
            child = node(next_puzzle)
            self.kids.append(child)
            child.parent = self

    def print(self):
        print(self.puzzle, '\n')

    # def same(self, parent_puzzle): # might need this
    #     if self.puzzle == parent_puzzle: return True


puzzle = [
    [1, 2, 0], 
    [4, 5, 3], 
    [7, 8, 6]
]
if(ucs(node(puzzle)).found == False):
    print("no solution found")