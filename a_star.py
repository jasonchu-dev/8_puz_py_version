import collections

class a_star:
    def __init__(self, puzzle):
        self.queue = []
        self.checked = []
        self.puzzle = puzzle
        self.queue.append(self.puzzle)
        self.found = False
        self.g = 0 # number of steps taken
    
        while range(len(self.queue)) != 0:
            self.queue = collections.deque(sorted(list(self.queue), key=lambda node : node.f))
            curr = self.queue[0]
            if curr.goal(): # for the very root node that is solution
                path.insert(0, kid.puzzle)
                self.found = True
                break
            self.checked.append(curr)
            curr.move()
            kid = None
            if curr.parent == None: # for very root of node that has no parent, set heuristic
                curr.calc_h()
                curr.f = curr.h
            curr.kids = collections.deque(sorted(list(curr.kids), key=lambda node : node.f))
            for i in range(len(curr.kids)):
                kid = curr.kids[i]
                self.g += 1
                kid.g = self.g
                kid.f = kid.g + kid.h
                if not self.prev_encounter_check(self.queue, kid) and not self.prev_encounter_check(self.checked, kid):
                    self.queue.append(kid)
            for i in range(len(curr.kids)):
                kid = curr.kids[i]
                if kid.goal():
                    path.insert(0, kid.puzzle)
                    while kid.parent != None:
                        kid = kid.parent
                        path.insert(0, kid.puzzle)
                    self.found = True
            if self.found: break
            del self.queue[0]

    def prev_encounter_check(self, list, kid):
        for node in range(len(list)):
            if kid.puzzle == list[node].puzzle:
                return True
        return False