"""Day 8: [Challenge Name]."""

import sys
import heapq

sys.path.append(
    "/Users/clementvangoethem/Library/Mobile Documents/com~apple~CloudDocs/Code_projects/AdventOfCode"
)
from utils import common
from typing import List

EXAMPLE = [
    "162,817,812",
    "57,618,57",
    "906,360,560",
    "592,479,940",
    "352,342,300",
    "466,668,158",
    "542,29,236",
    "431,825,988",
    "739,650,466",
    "52,470,668",
    "216,146,977",
    "819,987,18",
    "117,168,530",
    "805,96,715",
    "346,949,466",
    "970,615,88",
    "941,993,340",
    "862,61,35",
    "984,92,344",
    "425,690,689",
]  # 40

INPUT_PATH = "input/input_day_8.txt"
INPUT_DATA = common.read_text_to_list_of_strings(INPUT_PATH)


def parse_coordinates(data: List[str]) -> List[List[int]]:
    """Parse comma-separated coordinate strings into lists of integers."""
    return [list(map(int, line.split(","))) for line in data]


# len() count and multiply
def distance_3d(coordinate_1: List[int], coordinate_2: List[int]) -> float:
    """Calculate the Euclidean distance between two points in 3D space."""
    return (
        (coordinate_1[0] - coordinate_2[0]) ** 2
        + (coordinate_1[1] - coordinate_2[1]) ** 2
        + (coordinate_1[2] - coordinate_2[2]) ** 2
    ) ** 0.5


def combinations_to_consider(
    data: List[List[int]], existing_connections: List[set]
) -> List[tuple]:
    """Generate all unique pairs of coordinates that are not already connected."""
    combinations = []
    n = len(data)
    for i in range(n):
        for j in range(i + 1, n):
            # if one set in existing_connections contains both i and j, skip
            if any(i in conn and j in conn for conn in existing_connections):
                continue
            else:
                combinations.append((i, j))
    return combinations


def part1_out_of_range_rapidly(data, number_shortest_connections: int) -> int:
    """Solve part 1 of the challenge.
    Brute forcing needs to much time O(n²) pairs for each iteration"""

    connections = 0
    list_of_circuits = []
    while connections < number_shortest_connections:
        min_distance = 1000000000000000000  # large number
        min_pair = None
        # bruteforce all combinations
        combinations_to_check = combinations_to_consider(data, list_of_circuits)
        for i, j in combinations_to_check:
            dist = distance_3d(data[i], data[j])
            if dist < min_distance:
                min_distance = dist
                min_pair = (i, j)
        # add the new connection
        i, j = min_pair
        # if i or j is already in a circuit, add the other to that circuit
        for circuit in list_of_circuits:
            if i in circuit and j in circuit:
                # already connected no increase
                break
            elif i in circuit or j in circuit:
                circuit.add(i)
                circuit.add(j)  # sets so no duplicates
                connections += 1
                break
            else:
                list_of_circuits.append(set([i, j]))
                connections += 1
    # connection counter is not used for now
    # Multiplying together the sizes of the three largest circuits
    list_of_circuits.sort(key=len, reverse=True)
    result = 1
    for circuit in list_of_circuits[:3]:
        result *= len(circuit)
    return result


def part1_non_bruteforce(data, number_shortest_connections: int) -> int:
    """Solve part 1 efficiently using a priority queue approach.
    Solved with the help of AI"""
    n = len(data)

    # Pre-calculate all distances and store in a priority queue
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance_3d(data[i], data[j])
            heapq.heappush(distances, (dist, i, j))

    # Simple connected components tracking
    components = {
        i: {i} for i in range(n)
    }  # Each point starts in its own component

    connections_attempted = 0

    # Process edges in order of increasing distance (shortest first)
    while connections_attempted < number_shortest_connections and distances:
        dist, idx_a, idx_b = heapq.heappop(distances)

        # Find which components idx_a and idx_b belong to
        component_a = None
        component_b = None
        for comp in components.values():
            if idx_a in comp:
                component_a = comp
            if idx_b in comp:
                component_b = comp
            if component_a and component_b:  # both are defined
                break

        # If they are in different components, merge them
        if component_a is not component_b:
            merged_component = component_a | component_b  # Union of sets
            # Remove old components and add the merged one
            components = {
                k: v
                for k, v in components.items()
                if v not in [component_a, component_b]
            }
            # Use the smallest index as the new key for the merged component
            components[min(merged_component)] = merged_component

        # Count this connection attempt (whether merged or not)
        connections_attempted += 1

    # Get component sizes and multiply the three largest
    sizes = sorted([len(comp) for comp in components.values()], reverse=True)
    result = 1
    for size in sizes[:3]:
        result *= size

    return result


def part2(data) -> int:
    """Solve part 2 of the challenge.
    Connect until all junction boxes are in one circuit, return product of X coordinates of last connection.
    NO BIG ADDITION COMPARED TO PART 1"""
    n = len(data)

    # Pre-calculate all distances and store in a priority queue
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance_3d(data[i], data[j])
            heapq.heappush(distances, (dist, i, j))

    # Simple connected components tracking
    components = {
        i: {i} for i in range(n)
    }  # Each point starts in its own component

    last_connection = None

    # Process edges in order of increasing distance until we have one component
    while len(components) > 1 and distances: # ONE SINGLE COMPONENT LEFT
        dist, idx_a, idx_b = heapq.heappop(distances)

        # Find which components idx_a and idx_b belong to
        component_a = None
        component_b = None
        for comp in components.values():
            if idx_a in comp:
                component_a = comp
            if idx_b in comp:
                component_b = comp
            if component_a and component_b:
                break

        # If they are in different components, merge them
        if component_a is not component_b:
            merged_component = component_a | component_b
            # Remove old components and add the merged one
            components = {
                k: v
                for k, v in components.items()
                if v not in [component_a, component_b]
            }
            components[min(merged_component)] = merged_component

            # Record this as the last successful connection
            last_connection = (idx_a, idx_b)

    # RECORD LAST CONNECTION X COORDINATES PRODUCT
    if last_connection:
        x1 = data[last_connection[0]][0]  # X coordinate of first junction box
        x2 = data[last_connection[1]][0]  # X coordinate of second junction box
        return x1 * x2

    return 0


if __name__ == "__main__":
    # Parse input
    parsed_example = parse_coordinates(EXAMPLE)
    parsed_input = parse_coordinates(INPUT_DATA)

    # Part 1
    print("=== Part 1 ===")
    example_result1 = part1_non_bruteforce(parsed_example, 10)
    print(f"Example result: {example_result1}")

    result1 = part1_non_bruteforce(parsed_input, 1000)
    print(f"Part 1 result: {result1}")

    # Part 2
    print("\n=== Part 2 ===")
    example_result2 = part2(parsed_example)
    print(f"Example result: {example_result2}")

    result2 = part2(parsed_input)
    print(f"Part 2 result: {result2}")
