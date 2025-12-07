"""Day 6: Math Worksheet Problem."""

import sys

sys.path.append(
    "/Users/clementvangoethem/Library/Mobile Documents/com~apple~CloudDocs/Code_projects/AdventOfCode"
)
from utils import common
from typing import List

EXAMPLE = [
    "123 328  51 64 ",
    " 45 64  387 23 ",
    "  6 98  215 314",
    "*   +   *   +  ",
]

INPUT_PATH = "input/input_day_6.txt"
INPUT_DATA = common.read_text_to_list_of_strings(
    INPUT_PATH
)  # stripped by default


def parse_input(input_data: List[str]) -> List[List[str]]:
    """Parse the input data into individual math problems (by column = single math problem).
    """
    # split each line into its whitespace-separated parts (columns)
    split_lines = []
    max_num_columns = 0

    for line in input_data:
        columns = line.split()
        split_lines.append(columns)
        max_num_columns = max(max_num_columns, len(columns))

    # collect each problem by column
    problems_by_column = []
    for col_idx in range(max_num_columns):
        problem = []
        for row in split_lines:
            if col_idx < len(row):
                problem.append(row[col_idx])
        if problem:  # Only add non-empty columns
            problems_by_column.append(problem)

    return problems_by_column


def solve_problem(problem_data: List[str]) -> int:
    """Solve a single math problem."""
    # operation is either * or + 
    
    operator = problem_data[-1]
    if operator == "+":
        results = 0
        for elem in problem_data[:-1]:
            results += int(elem)
    elif operator == "*":
        results = 1
        for elem in problem_data[:-1]:
            results *= int(elem)
    else:
        raise ValueError(f"Unknown operator: {operator}")
    return results


def add_individual_problems(data) -> int:
    """Solve part 1 of the challenge."""
    total = 0
    for problem in data:
        result = solve_problem(problem)
        total += result
    return total


def part1(data) -> int:
    """Solve part 1 of the challenge."""
    return add_individual_problems(data)


def part2(data) -> int:
    """Solve part 2 of the challenge."""
    pass


if __name__ == "__main__":
    # Parse input
    parsed_data = parse_input(INPUT_DATA)
    example_data = parse_input(EXAMPLE)
    print(parsed_data)
    print(example_data)

    # Part 1
    print("=== Part 1 ===")
    example_result1 = part1(example_data)
    print(f"Example result: {example_result1}")

    result1 = part1(parsed_data)
    print(f"Part 1 result: {result1}")

    # Part 2
    print("\n=== Part 2 ===")
    example_result2 = part2(example_data)
    print(f"Example result: {example_result2}")

    result2 = part2(parsed_data)
    print(f"Part 2 result: {result2}")
