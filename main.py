path = []

puzzle = [
    [1, 6, 7], 
    [5, 0, 3], 
    [4, 8, 2]
]

print("\n")
val = int(input("Press 1 for main\nPress 2 for Manhattan Distance\nPress 3 for Misplaced Tiles\n"))

print("Please wait...")

if val == 2 or val == 3:
    if(a_star(node(puzzle)).found == False):
        print("\nNo solution found\n")
    
    else:
        print("\nSolution:\n")
        for i in range(len(path)):
            print("Depth:", i)
            for j in range(len(path[i])):
                print(path[i][j])
            print('\n')

print("Program simulated and tested on:\nIntel(R) Core(TM) i5-7300HQ CPU @ 2.50GHz\n")
