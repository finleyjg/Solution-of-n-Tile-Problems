
import time

#generating possible moves for the blank tile
def move_blank(i, j, n):
    if i + 1 < n:
        yield (i + 1, j)
    if i - 1 >= 0:
        yield (i - 1, j)
    if j + 1 < n:
        yield (i, j + 1)
    if j - 1 >= 0:
        yield (i, j - 1)

#generating possible new states through swapping blank tile with neighbouring tiles
def move(state):
    i, j, grid = state
    n = len(grid)
    for i1, j1 in move_blank(i, j, n):
        new_grid = [row[:] for row in grid] 
        new_grid[i][j], new_grid[i1][j1] = new_grid[i1][j1], new_grid[i][j] 
        yield [i1, j1, new_grid]

#depth-limited search
def dls(state, goal_state, depth, visited):
    if state == goal_state:
        return [state]

    if depth <= 0:
        return None
    
    if tuple(map(tuple, state[2])) in visited:
        return None
    
    visited.add(tuple(map(tuple, state[2])))

    for next_state in move(state):
        if tuple(map(tuple, next_state[2])) not in visited:
            result = dls(next_state, goal_state, depth - 1, visited)
            if result is not None:
                return [state] + result

    visited.remove(tuple(map(tuple, state[2])))
    return None

#iterative deepening depth-first search 
def iddfs(start_state, goal_state, max_depth):
    for depth in range(max_depth):
        visited = set()
        path = dls(start_state, goal_state, depth, visited)
        if path:
            return path
    return None

#solves multiple cases and prints the moves and the time taken
def solve_puzzle(start_states, goal_states):
    for case_number, start_state in enumerate(start_states, start=1):
        goal_state = goal_states[0] if case_number <= 5 else goal_states[1]
        start_time = time.time()
        result = iddfs(start_state, goal_state, max_depth=35)
        end_time = time.time()
        time_taken = end_time - start_time

        if result:
            moves = len(result) - 1
            print(f"Case {case_number}")
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
