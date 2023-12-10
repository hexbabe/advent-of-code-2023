from collections import deque
import sys
from typing import List


class Tile:
    tile_type: str
    steps_away: int
    def __init__(self, tile_type: str) -> None:
        self.tile_type = tile_type
        self.steps_away = float("inf")
    
    def __repr__(self) -> str:
        return str((self.tile_type, self.steps_away))
    

def dfs1(maze: List[List[Tile]]) -> None:
    def get_starting_tile():
        for i, row in enumerate(maze):
            for j, tile in enumerate(row):
                if tile.tile_type == "S":
                    return i, j
        raise Exception("No starting tile found!")

    def add_next_tile_to_stack(stack: deque, i: int, j: int, valid_tile_types: List[str], steps_taken_here: int) -> None:
        if i < 0 or i >= len(maze) or j < 0 or j >= len(maze[0]):
            return
        next_tile = maze[i][j]
        if next_tile.tile_type in valid_tile_types:
            stack.append((i, j, steps_taken_here))

    start_i, start_j = get_starting_tile()
    stack = deque()
    stack.append((start_i, start_j, 0))
    
    while stack:
        i, j, steps_taken_so_far = stack.pop()
        if steps_taken_so_far < maze[i][j].steps_away:
            maze[i][j].steps_away = steps_taken_so_far
            add_next_tile_to_stack(stack, i, j-1, ["-", "L", "F"], steps_taken_so_far+1)
            add_next_tile_to_stack(stack, i, j+1, ["-", "J", "7"], steps_taken_so_far+1)
            add_next_tile_to_stack(stack, i-1, j, ["|", "7", "F"], steps_taken_so_far+1)
            add_next_tile_to_stack(stack, i+1, j, ["|", "J", "L"], steps_taken_so_far+1)

def print_answer_part_1():
    text = open(sys.argv[1]).read().strip()  # arg is filepath
    maze = text.split("\n")
    for i, row in enumerate(maze):
        maze[i] = [Tile(tile_type) for tile_type in row]
    dfs1(maze)

    furthest_distance = 0
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            tile = maze[row][col]
            if tile.steps_away != float("inf") and tile.steps_away > furthest_distance:
                furthest_distance = tile.steps_away
    print(f"Dec 10 part 1: {furthest_distance}")
    
def is_enclosed(maze: List[List[Tile]], i: int, j: int) -> None:
    stack = deque()
    stack.append((i, j))
    seen = set()
    while len(stack) > 0:
        i, j = stack.pop()
        seen.add((i, j))

        for ii in range(i-1, i+2):
            for jj in range(j-1, j+2):
                out_of_range = ii < 0 or ii >= len(maze) or jj < 0 or jj >= len(maze[0])
                is_lateral = abs(i - ii) + abs(j - jj) > 1
                if is_lateral and not out_of_range and (ii, jj) not in seen and not is_main_pipe_or_asterisk(maze, i, j):
                    stack.append((ii, jj))
    
    for i, j in seen:
        if i == 0 or j == 0 or i == len(maze)-1 or j == len(maze[0])-1:
            return False
    return True

def is_junk_pipe(maze: List[List[Tile]], i: int, j: int) -> bool:
    tile = maze[i][j]
    return tile.tile_type not in [".", "*"] and tile.steps_away == float("inf")

def print_answer_part_2():
    text = open(sys.argv[1]).read().strip()
    maze_rows_as_str = text.split("\n")
    temp_maze: List[List[Tile]] = []

    # modify maze to to have gap in every other element in a row
    for i in range(len(maze_rows_as_str)):
        temp_maze.append([])
        for j in range(len(maze_rows_as_str[0])):
            temp_maze[i].append(Tile(maze_rows_as_str[i][j]))
            if j < len(maze_rows_as_str[0]) - 1:
                temp_maze[i].append(Tile("*"))

    # modify maze to have gap between every col
    maze: List[List[Tile]] = []
    for i, row in enumerate(temp_maze):
        maze.append(row)
        if i < len(temp_maze) - 1:
            maze.append([Tile("*")] * len(row))
    
    # modify maze to have pipes close row (horizontal) gaps
    for row in maze:
        for i, tile in enumerate(row):
            if tile.tile_type != "*" or i % 2 == 0:
                continue
            left_tile, right_tile = row[i-1], row[i+1]
            left_pipes = ["-", "L", "F", "S"]
            right_pipes = ["-", "J", "7", "S"]
            if left_tile.tile_type in left_pipes and right_tile.tile_type in right_pipes:
                row[i] = Tile("-")
    
    # modify maze to have pipes close col (vertical) gaps
    for j in range(len(maze[0])):
        if j % 2 == 1:
            continue
        for i, row in enumerate(maze):
            tile = row[j]
            if i >= len(maze) - 1:
                continue
            if tile.tile_type == "*":
                above_tile, below_tile = maze[i-1][j], maze[i+1][j]
                above_pipes = ["|", "7", "F", "S"]
                below_pipes = ["|", "J", "L", "S"]
                if above_tile.tile_type in above_pipes and below_tile.tile_type in below_pipes:
                    row[j] = Tile("|")
    
    dfs1(maze)
    acc = 0
    acc_tiles = []
    for i in range(len(maze)):
        print(maze[i])
        for j in range(len(maze[0])):
            if not is_main_pipe_or_asterisk(maze, i, j) and is_enclosed(maze, i, j):
                acc += 1
                acc_tiles.append(maze[i][j])
    print(f"Dec 10 part 2: {acc}")
    print(acc_tiles)


if __name__ == "__main__":
    print_answer_part_1()
    print_answer_part_2()
