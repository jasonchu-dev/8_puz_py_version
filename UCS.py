from Node import check
from Node import goal

class UCS:
    def __init__(self, parent_puzzle):
        self.queue = []
        self.checked = []
        self.path = []
        self.queue.append(parent_puzzle)
        found = False
        while (len(self.queue) > 0 and found == False):
            curr = self.queue[0]
            self.checked.append(self.queue[0])
            self.queue.pop(0)
            curr.check() # curr.Node.check() won't work
            
