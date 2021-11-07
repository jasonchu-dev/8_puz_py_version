path = []

x, y = 3, 3
puzzle = [[0 for i in range(x)] for j in range(y)]
spot = 0

print("Fill in the array:\n")

for i in range(len(puzzle)):
    for j in range(len(puzzle)):
        spot += 1
        print("spot", spot)
        puzzle[i][j] = int(input())
        
print('\n')
for i in range(len(puzzle)):
    print(puzzle[i])

print("\n")
val = int(input("Press 1 for UCS\nPress 2 for Manhattan Distance\nPress 3 for Misplaced Tiles\n"))

print("Please wait...")

if val == 2 or val == 3:
    if not a_star(node(puzzle, val)).found:
        print("\nNo solution found\n")
    else:
        print("\nSolution:\n")
        for i in range(len(path)):
            print("Depth:", i)
            for j in range(len(path[i])):
                print(path[i][j])
            print('\n')

else: 
    if not ucs(node(puzzle, val)).found:
        print("\nNo solution found\n")
    else:
        print("\nSolution:\n")
        for i in range(len(path)):
            print("Depth:", i)
            for j in range(len(path[i])):
                print(path[i][j])
            print('\n')

print("Program simulated and tested on:\nIntel(R) Core(TM) i5-7300HQ CPU @ 2.50GHz\n")