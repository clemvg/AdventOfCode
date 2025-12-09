"""Day 7: [Challenge Name]."""

import sys

sys.path.append(
    "/Users/clementvangoethem/Library/Mobile Documents/com~apple~CloudDocs/Code_projects/AdventOfCode"
)
from utils import common
from typing import List, Tuple

EXAMPLE = [
    ".......S.......",
    "...............",
    ".......^.......",
    "...............",
    "......^.^......",
    "...............",
    ".....^.^.^.....",
    "...............",
    "....^.^...^....",
    "...............",
    "...^.^...^.^...",
    "...............",
    "..^...^.....^..",
    "...............",
    ".^.^.^.^.^...^.",
    "...............",
]  # 21 times splitted and not 22 ^ because once not splitted

INPUT_PATH = "/Users/clementvangoethem/Library/Mobile Documents/com~apple~CloudDocs/Code_projects/AdventOfCode/input/input_day_7.txt"
INPUT_DATA = common.read_text_to_list_of_strings(
    INPUT_PATH
)  # stripped by default

# Questions
# What best way to read the data? list of list of str
# Need to find the dimensions of the graph first and the iteratively built the |, find S position first parse input
# Implement counter at each encountered split.


# HOW TO SOLVE THIS:
# 2. Use BFS/simulation to track all active beams
# 3. Each beam moves downward until it hits a splitter '^' or exits the grid
# 4. When a beam hits a splitter, it creates two new beams (left and right)
# 5. Count each split operation
# 6. Use a set to track visited positions to avoid infinite loops
# 7. Each beam state should include position and direction (though all start going down)


def parse_input(
    input_data: List[str],
) -> Tuple[List[List[str]], Tuple[int, int]]:
    """Parse input into a grid and find the starting position 'S'."""
    grid = [list(line) for line in input_data]
    position = None
    for row in range(
        len(grid)
    ):  # possible to use for i, row in enumerate(input_data):
        for col in range(len(grid[0])):
            if grid[row][col] == "S":
                position = (row, col)
                break
        if position:  # add here for beaking
            break
    return grid, position


def part1(data, start_position) -> int:
    """Solve part 1 of the challenge."""
    split_counter = 0
    rows, cols = len(data), len(data[0])
    visited_splitters = set()  # track already visited splitters

    active_beams = [start_position]  # positions to be checked start at S

    while active_beams:
        next_beams = []

        for row, col in active_beams:
            next_row = row + 1  # move down one row

            # bean exit the grid below
            if next_row >= rows:
                continue
            # beam exit the grid sides
            if col < 0 or col >= cols:
                continue

            cell = data[next_row][col]

            if cell == ".":
                next_beams.append((next_row, col))  # continue down
                # remove from visited splitters?

            elif cell == "^":
                # splitter - only count if we haven't hit before
                splitter_pos = (next_row, col)
                if splitter_pos not in visited_splitters:
                    visited_splitters.add(splitter_pos)
                    split_counter += 1

                    # left and right beams from the same row as the splitter
                    if col > 0:  # left
                        next_beams.append((next_row, col - 1))
                    if col < cols - 1:  # right
                        next_beams.append((next_row, col + 1))

        active_beams = next_beams

    return split_counter


def count_paths(data, row, col, memo):
    """Recursively count paths from (row, col) to the bottom of the grid.
    Args:
        data: The grid representing the laboratory.
        row: Current row position.
        col: Current column position.
        memo: A dictionary for memoization to store already computed paths.
        Memo is here the arg passed key to avoid recomputation and exponential blowup.
    Returns:
        The number of valid paths from (row, col) to the bottom."""

    rows, cols = (
        len(data),
        len(data[0]),
    )  # optional could pass arg also outside this function, though data still needed to access cell content

    # RULES
    # if the beam has exited the bottom of the grid, that's a valid timeline
    if row >= rows:
        return 1
    # if the beam has exited the grid to the left or right, that's not a valid timeline
    if col < 0 or col >= cols:
        return 0
    # if we've already computed the number of paths from this position, return it
    # recursive memoization step
    if (row, col) in memo:
        return memo[(row, col)]

    # CELL CONTENT
    # If the cell is empty or the start, continue moving down
    if data[row][col] == "." or data[row][col] == "S":
        result = count_paths(data, row + 1, col, memo)
    # If the cell is a splitter '^', split into two beams: left and right
    elif data[row][col] == "^":
        left = count_paths(data, row + 1, col - 1, memo)  # Move down-left
        right = count_paths(data, row + 1, col + 1, memo)  # Move down-right
        # rules will be checked recursively
        result = left + right  # Add the number of timelines from both splits
    else:  # optional
        # other cell type is treated as a dead end
        result = 0

    # Store the result in the memo dictionary before returning.
    memo[(row, col)] = result
    return result


def part2_recursion(data, start_position) -> int:
    """Solve part 2 of the challenge."""
    # Position based memoization is needed

    # Idea: not BFS but look at all possible paths recursively with memoization
    # This function counts all possible timelines (paths) the beam can take
    # from the starting position to the bottom of the grid, splitting at each '^' splitter.

    # It uses memoization to avoid recalculating the number of paths from the same position.

    # DISCLAIMER: part 2 required some help of dearest AI to be solved!

    memo = {}  # Dictionary to store results for (row, col) positions
    start_row, start_col = start_position
    return count_paths(data, start_row, start_col, memo)


def part_2_dp_bottom_up(data, start_position) -> int:
    """Solve part 2 using Ruben's bottom-up approach.
    BOTTOM-UP DYNAMIC PROGRAMMING APPROACH
    This approach avoids recursion by working backwards from the bottom of the grid.
    Key insight: If we know how many timelines reach each position at row i+1,
    we can calculate how many timelines reach each position at row i.
    """
    input_grid = [list(line) for line in data]
    start_index = start_position[1]  # column index of start position

    # Initialize: each position at the bottom row represents 1 timeline
    # (any beam that reaches the bottom counts as 1 valid timeline)
    n_time_lines = [1] * len(input_grid[0])
    start = len(input_grid) - 1  # bottom row index

    # Work backwards from bottom to top (excluding row 0 which contains 'S')
    # This bottom-up approach eliminates the need for recursion
    for current_line in range(start, 0, -1):
        line = input_grid[current_line]

        # For each position in the current row
        for index, char in enumerate(line):
            if char == "^":  # Found a splitter
                # A splitter combines timelines from its left and right children
                # (the positions it would split TO in the next row down)
                l_count = 0  # timelines from left child
                r_count = 0  # timelines from right child

                # Check left child (index - 1 in the row below)
                if index > 0:
                    l_count = n_time_lines[index - 1]

                # Check right child (index + 1 in the row below)
                if index < len(line) - 1:
                    r_count = n_time_lines[index + 1]

                # Total timelines through this splitter = sum of child timelines
                count = r_count + l_count
                n_time_lines[index] = count

                # Note: Empty cells '.' don't need special handling because beams
                # pass through them without splitting, so their timeline count
                # remains whatever was calculated from positions above them

    # The answer is the number of timelines that reach the start position
    return n_time_lines[start_index]


if __name__ == "__main__":
    # Parse input
    example_data, start_pos = parse_input(EXAMPLE)
    print(f"Start position: {start_pos}")

    # Part 1 - Example
    print("=== Part 1 (Example) ===")
    example_result1 = part1(example_data, start_pos)
    print(f"Example result: {example_result1}")

    # Part 2 - Example
    print("\n=== Part 2 (Example) ===")
    example_result2 = part2_recursion(example_data, start_pos)
    print(f"Example result (recursive): {example_result2}")

    example_result2_dp_bottom_up = part_2_dp_bottom_up(example_data, start_pos)
    print(f"Example result (DP bottom-up approach): {example_result2_dp_bottom_up}")
    print("Expected: 40")

    # Run on real input
    print("\n=== Real Input ===")
    parsed_data, start_pos_part_1 = parse_input(INPUT_DATA)
    result1 = part1(parsed_data, start_pos_part_1)
    print(f"Part 1 result: {result1}")
    result2_recursion = part2_recursion(parsed_data, start_pos_part_1)
    print(f"Part 2 result (recursive): {result2_recursion}")
    result2_dp_bottom_up = part_2_dp_bottom_up(parsed_data, start_pos_part_1)
    print(f"Part 2 result (DP bottom-up approach): {result2_dp_bottom_up}")