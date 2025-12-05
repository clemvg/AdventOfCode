"""Day 3: The Lobby."""
from utils import common
from typing import List

EXAMPLE = [
    "..@@.@@@@.",
    "@@@.@.@.@@",
    "@@@@@.@.@@",
    "@.@@@@..@.",
    "@@.@@@@.@@",
    ".@@@@@@@.@",
    ".@.@.@.@@@",
    "@.@@@.@@@@",
    ".@@@@@@@@.",
    "@.@.@@@.@."
]
INPUT_PATH = "input/input_day_4.txt"
INPUT_DATA = common.read_text_to_list_of_strings(INPUT_PATH)
print(INPUT_DATA)

# -------- Approach --------
# Problem: Given a grid representing a printing department's layout, where '@' indicates a printer
# and '.' indicates empty space, determine how many printers can be accessed which are printers with fewer than two printers in their eight adjacent positions (horizontally, vertically, diagonally).
# Answer is number of printers accessible
# Probably part two: other rule

# Format to be read as well? List of strings?
 

def to_matrix(grid: List[str]) -> List[List[str]]:
    return [list(row) for row in grid]

def count_accessbible_rolls(grid: List[List[str]], k: int) -> int:
    # Format is list of strings
    accessible_rolls = 0
    number_rows = len(grid[0])
    number_cols = len(grid)

    dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    for r in range(number_rows):
        for c in range(number_cols):
            if grid[r][c] != '@':
                continue
            neighbors = 0
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < number_rows and 0 <= nc < number_cols and grid[nr][nc] == '@':
                    neighbors += 1
            if neighbors < k:
                accessible_rolls += 1
    return accessible_rolls

def count_accessbible_rollsPart2(grid: List[List[str]], k: int) -> int:
    # Format is list of strings
    accessible_rolls = 0
    number_rows = len(grid[0])
    number_cols = len(grid)

    dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    rolls_before = counter_number_of_printers_before(grid)
    rolls_after = 0
    iteration = 1
    while rolls_after < rolls_before or iteration == 1:
        remove_counter = 0
        for r in range(number_rows):
            for c in range(number_cols):
                if grid[r][c] != '@':
                    continue
                neighbors = 0
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < number_rows and 0 <= nc < number_cols and grid[nr][nc] == '@':
                        neighbors += 1
                if neighbors < k:
                    accessible_rolls += 1
                    grid[r][c] = "."
                    remove_counter += 1
                #replace the element by dot
        rolls_after = rolls_before - remove_counter
        iteration += 1
                
    return accessible_rolls


def counter_number_of_printers_before(grid: List[List[str]]) -> int:
    counter = 0
    for row_index in range(0,len(grid)):
        for column_index in range(0,len(grid[0])):
            if grid[row_index][column_index] == '@':
                counter += 1
    return counter
                            


if __name__ == "__main__":
    # part 1
    matrix = to_matrix(INPUT_DATA)
    # print("Accessible printers:", count_accessbible_rolls(matrix, 4))
    # part 2
    example_matrix = to_matrix(EXAMPLE)
    print("Example answer for second part", count_accessbible_rollsPart2(example_matrix,4))
    
    print("Answer for second part", count_accessbible_rollsPart2(matrix,4))
                