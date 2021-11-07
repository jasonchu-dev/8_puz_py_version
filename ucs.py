import collections
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
                path.append(curr.puzzle)
                self.found = True
                break
            self.checked.append(curr)
            curr.move()
            curr.kids = collections.deque(sorted(list(curr.kids), key=lambda node : node.f))
            for i in range(len(curr.kids)):
                kid = curr.kids[i]
                if kid.goal():
                    path.insert(0, kid.puzzle)
                    while kid.parent != None:
                        kid = kid.parent
                        path.insert(0, kid.puzzle)
                    self.found = True
                    break
                if not self.prev_encounter_check(self.queue, kid) and not self.prev_encounter_check(self.checked, kid):
                    self.queue.append(kid)
            self.queue.pop(0)
            if self.found: break

    def prev_encounter_check(self, list, kid):
        for node in range(len(list)):
            if kid.puzzle == list[node].puzzle:
                return True
        return False