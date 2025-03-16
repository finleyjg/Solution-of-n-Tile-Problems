
import time

#generating possible moves for the blank tile
def move_blank(i, j, n):
    if i + 1 < n:
        yield (i + 1, j) #moves down (if not on last row)
    if i - 1 >= 0:
        yield (i - 1, j) #moves up (if not on first row)
    if j + 1 < n:
        yield (i, j + 1) #moves right (if not on last column)
    if j - 1 >= 0:
        yield (i, j - 1) #moves left (if not on first column)

#generating possible new states through swapping blank tile with neighbouring tiles
def move(state):
    i, j, grid = state
    n = len(grid)
    for i1, j1 in move_blank(i, j, n):
        new_grid = [row[:] for row in grid]
        new_grid[i][j], new_grid[i1][j1] = new_grid[i1][j1], new_grid[i][j]
        yield [i1, j1, new_grid]

#calculating the heuristic, manhattan distance
def manhattan_distance(grid, goal_grid):
    n = len(grid)
    goal_positions = {goal_grid[i][j]: (i, j) for i in range(n) for j in range(n)}
    return sum(abs(i - goal_positions[val][0]) + abs(j - goal_positions[val][1])
               for i in range(n) for j in range(n) if (val := grid[i][j]) != 0)

#a recursive version of the depth-limited search accounting for cost-bound
#could also be called the search function, but i felt recursive dls made more sense to read
def recursive_dls(path, g, bound, goal_state):
    state = path[-1]
    f = g + manhattan_distance(state[2], goal_state[2])
    #f is indicative of the total cost, a combination of the moves made (g) and the manhattan distance

    if f > bound: #adjust cost
        return f

    if state[2] == goal_state[2]:
        return "found"

    min_cost = float('inf')
    #by setting the min cost to infinity it allows any actual path cost to replace it
    for next_state in move(state):
        if next_state not in path: #ensures previous states are not revisited
            path.append(next_state)
            result = recursive_dls(path, g + 1, bound, goal_state)
            if result == "found":
                return "found"
            if result < min_cost:
                min_cost = result
            path.pop() #remove last move

    return min_cost

#iterative deepening A*
def ida_star(start_state, goal_state):
    bound = manhattan_distance(start_state[2], goal_state[2]) #initial bound
    path = [start_state]

    while True:
        result = recursive_dls(path, 0, bound, goal_state)
        if result == "found":
            return path
        if result == float('inf'):
            return None
        bound = result #updates bound

#solves multiple cases and prints the moves and the time taken
def solve_puzzle(start_states, goal_states):
    for case_number, start_state in enumerate(start_states, start=1):
        goal_state = goal_states[0] if case_number <= 5 else goal_states[1]

        start_time = time.time()
        result = ida_star(start_state, goal_state)
        end_time = time.time()
        time_taken = end_time - start_time

        if result:
            moves = len(result) - 1
            print(f"Case {case_number}")
            #print("Manhattan Distance:", manhattan_distance(start_state[2], goal_state[2]))#checking if manhattan works correctly
            print(f"Number of moves: {moves}")
            print(f"Time taken: {time_taken:.4f} seconds\n")
        else:
            print(f"Case {case_number}")
            print("Puzzle not solved for this case.\n")

goal_states = [
    [0, 2, [[3, 2, 0], [6, 1, 8], [4, 7, 5]]], #first goal state
    [2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]]  #second goal state
]

initial_states = [
    [0, 0, [[0, 7, 1], [4, 3, 2], [8, 6, 5]]],#1
    [0, 2, [[5, 6, 0], [1, 3, 8], [4, 7, 2]]],#2
    [2, 0, [[3, 5, 6], [1, 2, 7], [0, 8, 4]]],#3
    [1, 1, [[7, 3, 5], [4, 0, 2], [8, 1, 6]]],#4
    [2, 0, [[6, 4, 8], [7, 1, 3], [0, 2, 5]]],#5
    [0, 0, [[0, 1, 8], [3, 6, 7], [5, 4, 2]]],#6
    [2, 0, [[6, 4, 1], [7, 3, 2], [0, 5, 8]]],#7
    [0, 0, [[0, 7, 1], [5, 4, 8], [6, 2, 3]]],#8
    [0, 2, [[5, 4, 0], [2, 3, 1], [8, 7, 6]]],#9
    [2, 1, [[8, 6, 7], [2, 5, 4], [3, 0, 1]]]#10
]

solve_puzzle(initial_states, goal_states)
