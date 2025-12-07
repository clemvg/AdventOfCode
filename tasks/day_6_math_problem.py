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
        result = solve_problem(problem) # switch part 1/2
        total += result
    return total

# Part 2 ---
 
def part_2(lines: List[str]) -> int:
    """Solve cephalopod math worksheet by reading columns right-to-left."""

    # longest line width to know where to start
    max_width = max(len(line) for line in lines)

    # pad all line to same width - used ai therefore
    padded_lines = [line.ljust(max_width) for line in lines]

    # do all problems at once
    total = 0
    col = max_width - 1 # index of rightmost column

    while col >= 0:
        # skip columns that are all spaces
        if all(
            padded_lines[row][col] == " " for row in range(len(padded_lines))
        ):
            col -= 1
            continue

        # find the start of this problem (ie rightmost non-space column)
        problem_start = col
        while problem_start >= 0 and not all(
            padded_lines[row][problem_start] == " "
            for row in range(len(padded_lines))
        ):
            problem_start -= 1

        # Extract numbers and operator for this problem
        numbers = []
        operator = None

        for c in range(col, problem_start - 1, -1):  # Read right-to-left
            # Build number from top-to-bottom in this column
            number_str = ""
            for row in range(len(padded_lines) - 1):  # Exclude operator row
                char = padded_lines[row][c]
                if char.isdigit():
                    number_str += char

            if number_str:
                numbers.append(int(number_str))

            # Get operator from last row
            if operator is None:
                op_char = padded_lines[-1][c]
                if op_char in ["+", "*"]:
                    operator = op_char

        # Calculate result for this problem
        if numbers and operator:
            result = numbers[0]
            for num in numbers[1:]:
                if operator == "+":
                    result += num
                elif operator == "*":
                    result *= num
            total += result

        # Move to next problem (skip the space column)
        col = problem_start - 2

    return total   
        


if __name__ == "__main__":
    # Parse input
    parsed_data = parse_input(INPUT_DATA)
    example_data = parse_input(EXAMPLE)
    # print(parsed_data)
    # print(example_data)

    # Part 1
    print("=== Part 1 ===")
    example_result1 = add_individual_problems(example_data)
    print(f"Example result: {example_result1}")

    result1 = add_individual_problems(parsed_data)
    print(f"Part 1 result: {result1}")

    # Part 2
    print("\n=== Part 2 ===")
    example_result2 = part_2(EXAMPLE)
    print(f"Example result: {example_result2}")

    result2 = part_2(INPUT_DATA)
    print(f"Part 2 result: {result2}")
