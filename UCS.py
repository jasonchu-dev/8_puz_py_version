import Node

class ucs:
    def __init__(self, parent_puzzle):
        self.queue = []
        self.checked = []
        self.puzzle = parent_puzzle
        self.queue.append(self.puzzle)
    
    def runthrough(self):
        while len(self.queue) != 0:
            curr = self.queue[0]
            self.checked.append(curr) # move at the end of this loop
            curr.Node.move()
            for i in len(self.puzzle.kids):
                kid = self.puzzle.kids[i]
                if kid.goal():
                    print(kid)
                    while kid.parent != None:
                        kid = kid.parent
                        print(kid)
                    print("tgrdthfyfg", kid)
                if not (self.prev_encounter_check(self.queue, kid) and self.prev_encounter_check(self.checked, kid)):
                    self.queue.append(kid)

    def prev_encounter_check(list, kid):
        for i in list:
            if kid == list[i]: return True
        return False