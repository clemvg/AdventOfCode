"""Day 7: [Challenge Name]."""

import sys

sys.path.append(
    "/Users/clementvangoethem/Library/Mobile Documents/com~apple~CloudDocs/Code_projects/AdventOfCode"
)
from utils import common
from typing import List

EXAMPLE = [
    # Add example data here
]

INPUT_PATH = "input/input_day_7.txt"
INPUT_DATA = common.read_text_to_list_of_strings(INPUT_PATH)  # stripped by default


def parse_input(input_data: List[str]):
    """Parse the input data into the required format."""
    # TODO: Implement input parsing
    return input_data


def part1(data) -> int:
    """Solve part 1 of the challenge."""
    # TODO: Implement part 1 solution
    return 0


def part2(data) -> int:
    """Solve part 2 of the challenge."""
    # TODO: Implement part 2 solution
    return 0


if __name__ == "__main__":
    # Parse input
    parsed_data = parse_input(INPUT_DATA)
    example_data = parse_input(EXAMPLE)
    
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
