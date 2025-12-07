#!/usr/bin/env python3
"""Script to create template files for new Advent of Code challenges."""

import os
import sys
from pathlib import Path


def create_day_files(day_number: int):
    """Create Python and input files for a new Advent of Code day challenge."""

    # Base directory (where this script is located)
    base_dir = Path(__file__).parent

    # File paths
    py_filename = f"day_{day_number}.py"
    input_filename = f"input_day_{day_number}.txt"

    py_filepath = base_dir / "tasks" / py_filename
    input_filepath = base_dir / "input" / input_filename

    # Create directories if they don't exist
    py_filepath.parent.mkdir(exist_ok=True)
    input_filepath.parent.mkdir(exist_ok=True)

    # Python file template
    py_template = f'''"""Day {day_number}: [Challenge Name]."""

import sys

sys.path.append(
    "/Users/clementvangoethem/Library/Mobile Documents/com~apple~CloudDocs/Code_projects/AdventOfCode"
)
from utils import common
from typing import List

EXAMPLE = [
    # Add example data here
]

INPUT_PATH = "input/{input_filename}"
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
    print(f"Example result: {{example_result1}}")
    
    result1 = part1(parsed_data)
    print(f"Part 1 result: {{result1}}")
    
    # Part 2
    print("\\n=== Part 2 ===")
    example_result2 = part2(example_data)
    print(f"Example result: {{example_result2}}")
    
    result2 = part2(parsed_data)
    print(f"Part 2 result: {{result2}}")
'''

    # Check if files already exist
    if py_filepath.exists():
        print(f"Warning: {py_filepath} already exists!")
        response = input("Overwrite? (y/N): ")
        if response.lower() != "y":
            print("Skipping Python file creation.")
        else:
            with open(py_filepath, "w") as f:
                f.write(py_template)
            print(f"Created: {py_filepath}")
    else:
        with open(py_filepath, "w") as f:
            f.write(py_template)
        print(f"Created: {py_filepath}")

    # Create empty input file
    if input_filepath.exists():
        print(f"Warning: {input_filepath} already exists!")
        response = input("Overwrite? (y/N): ")
        if response.lower() != "y":
            print("Skipping input file creation.")
        else:
            input_filepath.touch()
            print(f"Created: {input_filepath}")
    else:
        input_filepath.touch()
        print(f"Created: {input_filepath}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_day.py <day_number>")
        print("Example: python create_day.py 6")
        sys.exit(1)

    try:
        day = int(sys.argv[1])
        if day < 1 or day > 25:
            print("Day number must be between 1 and 25")
            sys.exit(1)

        create_day_files(day)

    except ValueError:
        print("Day number must be a valid integer")
        sys.exit(1)
