"""Day 7: [Challenge Name]."""

import sys

sys.path.append(
    "/Users/clementvangoethem/Library/Mobile Documents/com~apple~CloudDocs/Code_projects/AdventOfCode"
)
from utils import common
from typing import List
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

INPUT_PATH = "input/input_day_7.txt"
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


def part2(data) -> int:
    """Solve part 2 of the challenge."""
    # TODO: Implement part 2 solution
    return 0


if __name__ == "__main__":
    # Parse input
    parsed_data, start_pos_part_1 = parse_input(INPUT_DATA)
    example_data, start_pos = parse_input(EXAMPLE)
    # print type of parsed data
    print(f"Start position: {start_pos}")
    print(f"Parsed example data: {example_data}")
    # todo for input data

    # Part 1
    print("=== Part 1 ===")
    example_result1 = part1(example_data, start_pos)
    print(f"Example result: {example_result1}")

    result1 = part1(parsed_data, start_pos_part_1)
    print(f"Part 1 result: {result1}")

    # Part 2
    print("\n=== Part 2 ===")
    # example_result2 = part2(example_data)
    # print(f"Example result: {example_result2}")

    # result2 = part2(parsed_data)
    # print(f"Part 2 result: {result2}")
