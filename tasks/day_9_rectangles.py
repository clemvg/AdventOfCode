"""Day 9: [Challenge Name]."""

import sys

sys.path.append(
    "/Users/clementvangoethem/Library/Mobile Documents/com~apple~CloudDocs/Code_projects/AdventOfCode"
)
from utils import common
from typing import List
import matplotlib.pyplot as plt
import seaborn as sns

def plot_red_tiles(coords, title="Red Tiles"):
    """Plot red tile coordinates using seaborn."""
    xs, ys = zip(*coords)
    plt.figure(figsize=(8, 8))
    sns.scatterplot(x=xs, y=ys, color="red", s=100, marker="s", edgecolor="black")
    plt.gca().invert_yaxis()  # Optional: match grid orientation
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()

EXAMPLE = [
    # Add example data here
"7,1",
"11,1",
"11,7",
"9,7",
"9,5",
"2,5",
"2,3",
"7,3",
]

INPUT_PATH = "input/input_day_9.txt"
INPUT_DATA = common.read_text_to_list_of_strings(INPUT_PATH)  # stripped by default


def parse_input(input_data: List[str]):
    """Parse the input data into a list of (x, y) tuples."""
    result = []
    for line in input_data:
        if line.strip():
            parts = line.split(',')
            x = int(parts[0])
            y = int(parts[1])
            result.append((x, y))
    return result

def part1(data) -> int:
    """Find the largest rectangle area using two red tiles as opposite corners."""
    max_area = 0
    n = len(data)
    for i in range(n):
        x1, y1 = data[i]
        for j in range(i + 1, n):
            x2, y2 = data[j]
            if x1 != x2 and y1 != y2:
                area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1) # indexing start at zero
                if area > max_area:
                    print(f"New max area {area} found with corners ({x1},{y1}) and ({x2},{y2})")
                    max_area = area
    return max_area


def part2(data) -> int:
    """Solve part 2 of the challenge."""
    # TODO: Implement part 2 solution
    return 0


if __name__ == "__main__":
    # Parse input
    parsed_data = parse_input(INPUT_DATA)
    example_data = parse_input(EXAMPLE)
    # plot_red_tiles(example_data, title="Example Red Tiles")
    
    # Part 1
    print("=== Part 1 ===")
    example_result1 = part1(example_data)
    print(f"Example result: {example_result1}")
    
    
    result1 = part1(parsed_data)
    print(f"Part 1 result: {result1}")
    plot_red_tiles(parsed_data, title="Input Red Tiles")
    
    # # Part 2
    # print("\n=== Part 2 ===")
    # example_result2 = part2(example_data)
    # print(f"Example result: {example_result2}")
    
    # result2 = part2(parsed_data)
    # print(f"Part 2 result: {result2}")
