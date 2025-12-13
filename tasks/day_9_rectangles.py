"""Day 9: [Challenge Name]."""

import sys

sys.path.append(
    "/Users/clementvangoethem/Library/Mobile Documents/com~apple~CloudDocs/Code_projects/AdventOfCode"
)
from utils import common
from typing import List, Set, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
# shapely
from shapely.geometry import Polygon, Point # could also be used
from shapely.prepared import prep

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

def point_in_polygon(point, polygon):
    """Check if point is inside or on the boundary of polygon using ray casting algorithm.

    Args:
        point: (x, y) coordinate to test
        polygon: List of (x, y) coordinates forming a closed polygon

    Returns:
        True if point is inside or on the boundary, False otherwise
    """
    is_inside = False
    num_vertices = len(polygon)

    # Iterate through each edge of the polygon
    for i in range(num_vertices):
        # Create vectors from the test point to current vertex and next vertex
        vec_to_current = (polygon[i][0] - point[0], polygon[i][1] - point[1])
        vec_to_next = (polygon[(i+1) % num_vertices][0] - point[0],
                       polygon[(i+1) % num_vertices][1] - point[1])

        # Ensure vec_to_current has the lower y-coordinate for consistent ray casting
        if vec_to_current[1] > vec_to_next[1]:
            vec_to_current, vec_to_next = vec_to_next, vec_to_current

        # Ray casting: cast a ray from point to the right and count edge crossings
        # Check if horizontal ray from point intersects this edge
        if (vec_to_current[1] <= 0 and vec_to_next[1] > 0 and
            vec_to_current[0] * vec_to_next[1] < vec_to_current[1] * vec_to_next[0]):
            is_inside = not is_inside

        # Check if point lies exactly on this edge (collinearity check)
        # Two conditions: vectors are collinear AND point is between the vertices
        cross_product = vec_to_current[0] * vec_to_next[1] - vec_to_current[1] * vec_to_next[0]
        dot_product = vec_to_current[0] * vec_to_next[0] + vec_to_current[1] * vec_to_next[1]
        if cross_product == 0 and dot_product <= 0:
            return True

    return is_inside

def segments_intersect(segment1, segment2):
    """Check if two line segments intersect (not just touching at endpoints).

    Uses cross product to determine if segments properly intersect.
    Two segments intersect if their endpoints are on opposite sides of each other.

    Args:
        segment1: Tuple of two points ((x1, y1), (x2, y2))
        segment2: Tuple of two points ((x3, y3), (x4, y4))

    Returns:
        True if segments intersect, False otherwise
    """
    (point1, point2), (point3, point4) = segment1, segment2
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    x4, y4 = point4

    # Check if point3 and point4 are on opposite sides of line segment1 (p1-p2)
    # Using cross product: if signs differ, points are on opposite sides
    cross1 = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
    cross2 = (x2 - x1) * (y4 - y1) - (y2 - y1) * (x4 - x1)

    # If both cross products have same sign (or are zero), points are on same side
    if (cross1 <= 0 and cross2 <= 0) or (cross1 >= 0 and cross2 >= 0):
        return False

    # Check if point1 and point2 are on opposite sides of line segment2 (p3-p4)
    cross3 = (x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)
    cross4 = (x4 - x3) * (y2 - y3) - (y4 - y3) * (x2 - x3)

    # If both cross products have same sign (or are zero), points are on same side
    if (cross3 <= 0 and cross4 <= 0) or (cross3 >= 0 and cross4 >= 0):
        return False

    # If we reach here, the segments properly intersect
    return True

def part2(data) -> int:
    """Find the largest rectangle area using only red and green tiles.

    Strategy:
    - Red tiles form a closed loop connected by green tiles
    - Find largest rectangle with 2 red tiles as opposite corners
    - All tiles in rectangle must be red or green (inside/on the polygon boundary)

    Validation approach:
    - Check all 4 rectangle corners are inside or on the polygon
    - Ensure no rectangle edges cross through the polygon boundary

    Args:
        data: List of (x, y) coordinates of red tiles forming a closed loop

    Returns:
        Maximum rectangle area that fits within red/green tile region
    """
    max_area = 0
    num_red_tiles = len(data)

    # Try all pairs of red tiles as opposite corners of a potential rectangle
    for i in range(num_red_tiles):
        x1, y1 = data[i]
        for j in range(i + 1, num_red_tiles):
            x2, y2 = data[j]

            # Skip invalid rectangles: must have different x AND y coordinates
            if x1 == x2 or y1 == y2:
                continue

            # Calculate the area of this potential rectangle (inclusive of boundaries)
            potential_area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)

            # Optimization: skip if this can't beat our current maximum
            if potential_area <= max_area:
                continue

            # Validate that the rectangle is fully contained within the polygon
            is_valid_rectangle = True

            # Define the four edges of the rectangle
            # Each edge is defined by its two endpoints
            rectangle_edges = [
                ((x1, y1), (x1, y2)),  # Left vertical edge
                ((x1, y2), (x2, y2)),  # Top horizontal edge
                ((x2, y2), (x2, y1)),  # Right vertical edge
                ((x2, y1), (x1, y1))   # Bottom horizontal edge
            ]

            # Check each edge of the rectangle
            for rect_edge in rectangle_edges:
                edge_start, edge_end = rect_edge

                # Validation 1: Both endpoints must be inside or on the polygon
                if not point_in_polygon(edge_start, data) or not point_in_polygon(edge_end, data):
                    is_valid_rectangle = False
                    break

                # Validation 2: Edge must not cross through the polygon boundary
                # (it can touch at vertices, but not cut through)
                for k in range(num_red_tiles):
                    # Get each edge of the polygon (from vertex k to vertex k-1)
                    polygon_edge = (data[k], data[k-1])

                    # Check if rectangle edge intersects with this polygon edge
                    if segments_intersect(rect_edge, polygon_edge):
                        is_valid_rectangle = False
                        break

                # Break outer loop if rectangle is invalid
                if not is_valid_rectangle:
                    break

            # If rectangle passed all validation checks, update maximum
            if is_valid_rectangle:
                max_area = potential_area
                print(f"New max area {max_area} found with corners ({x1}, {y1}) and ({x2}, {y2})")

    return max_area


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
    # plot_red_tiles(parsed_data, title="Input Red Tiles")

    # Part 2
    print("\n=== Part 2 ===")
    example_result2 = part2(example_data)
    print(f"Example result: {example_result2}")

    result2 = part2(parsed_data)
    print(f"Part 2 result: {result2}")
