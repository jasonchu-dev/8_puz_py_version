import cpuinfo

puzzle = [
    [1, 6, 7], 
    [5, 0, 3], 
    [4, 8, 2]
]

print("\n")

if(a_star(node(puzzle)).found == False):
    print("\nNo solution found\n")

else:
    print("\nSolution:\n")
    for i in range(len(path)):
        print("Depth:", i)
        for j in range(len(path[i])):
            print(path[i][j])
        print('\n')

print("Executed on:\n", cpuinfo.get_cpu_info()['brand_raw'], '\n')