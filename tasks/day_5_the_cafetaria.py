"""Day 5: The Cafetaria."""

import sys

sys.path.append(
    "/Users/clementvangoethem/Library/Mobile Documents/com~apple~CloudDocs/Code_projects/AdventOfCode"
)
from utils import common
from typing import List

EXAMPLE = [
    "3-5",
    "10-14",
    "16-20",
    "12-18",
    "1",
    "5",
    "8",
    "11",
    "17",
    "32",
]
INPUT_PATH = "input/input_day_5.txt"
INPUT_DATA = common.read_text_to_list_of_strings(
    INPUT_PATH
)  # tripped by default


def split_ranges_and_product(input_data: List[str]) -> (List[tuple], List[int]):
    """
    Splits input_data into two lists:
    - ranges: list of tuples (start, end) for elements like 'number-number'
    - singles: list of integers for single number elements
    """
    ranges = []
    singles = []
    for elem in input_data:
        if "-" in elem:
            parts = elem.split("-")
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                ranges.append((int(parts[0]), int(parts[1])))
        elif elem.isdigit():
            singles.append(int(elem))
    return ranges, singles


product_ranges, proudct_ids = split_ranges_and_product(INPUT_DATA)
# print(len(product_ranges))
# print(len(proudct_ids))
example_ranges, example_ids = split_ranges_and_product(EXAMPLE)
# ------ Approach -------


def part1(product_ranges: List[tuple], products: List[int]) -> int:
    """
    For each element in products, check if it falls within any of the product_ranges.
    Returns the count of products that are within any range.
    """
    count = 0
    for elem in products:
        for start, end in product_ranges:
            if start <= elem <= end:
                count += 1
                break
    return count


# Part1
result = part1(product_ranges, proudct_ids)
print("Count of products in ranges:", result)


# Part2
# non working brute forcing is not possible
def part2_bruteforcing_non_working(product_ranges: List[tuple]) -> int:
    """
    Create a list with al number in the ranges, make ten a set to have unique values, an return its length.
    """
    all_numbers = []
    for start, end in product_ranges:
        numbers_in_range = range(start, end + 1)
        all_numbers.extend(numbers_in_range)
    unique_numbers = set(all_numbers)
    return len(unique_numbers)

def part2_buggy(product_ranges: List[tuple]) -> int:
    """
    Merge overlapping ranges. For each range check if start end overlaps with another range so star1 bigger start2 and end1 smaller than end2 (three options left join join right join)
    Create a variable updating lists stating updated ranges min max
    Continue checking that variable with updated new ranges
    Return new ranges"""

    merged = [product_ranges[0]]  # to be checked
    for range in product_ranges[1:]:
        start = range[0]
        end = range[1]
        ranges_to_be_removed = []
        for range_already in merged:
            start_already = range_already[0]
            end_already = range_already[1]
            # comparing two ranges that do not overlap at all
            if (start < start_already and end < start_already) or (
                start > end_already and end > end_already
            ):
                continue
            elif (
                # left join: s1 < s2 and e1 <= e2
                # right join: s1 >= s2 and e1 > e2
                # outer join: s1 < s2 and e1 > e2
                (start < start_already and end <= end_already)
                or (start >= start_already and end > end_already)
                or (start < start_already and end > end_already)
            ):
                new_start = min(start, start_already)
                new_end = max(end, end_already)
                new_range = (new_start, new_end)
                # remove range_already in merged
                ranges_to_be_removed.append(range_already)
                # update range variable on the fly
                range = new_range
                start = range[0]
                end = range[1]
            else:
                continue
        # remove ranges to be removed
        for r in ranges_to_be_removed:
            merged.remove(r)
        merged.append(range)

    # print(merged)

    total_elements = sum(end - start + 1 for start, end in merged)
    return total_elements


def part2_old_buggy_fixed(product_ranges: List[tuple]) -> int:
    """
    The main problem is that when I modified ranges on-the-fly and removed ranges from the merged list, 
    I needed to check the updated range against ALL remaining ranges as well! (not just continue with the next one)
    
    For this, I added a while loop that continues checking until no more merges are possible.
    
    I guess could be also done quicker by sorting the range initially (see part2_ai_sorting)
    """

    merged = [product_ranges[0]]

    for range_to_add in product_ranges[1:]:
        start = range_to_add[0]
        end = range_to_add[1]

        # keep merging until no more overlaps found
        merged_something = True
        while merged_something:
            merged_something = False
            ranges_to_be_removed = []

            for range_already in merged:
                start_already = range_already[0]
                end_already = range_already[1]

                # check if ranges overlap or touch
                # no need to check all three joins separately
                if not (
                    (start < start_already and end < start_already)
                    or (start > end_already and end > end_already)
                ):
                    # ranges overlap merge them - but final range will be updated after the loop
                    new_start = min(start, start_already)
                    new_end = max(end, end_already)

                    # update range variable on the fly
                    start = new_start
                    end = new_end

                    # mark the existing range for removal
                    ranges_to_be_removed.append(range_already)
                    merged_something = True # recheck newly created range to all (including previous merged) ranges!

            # remove all ranges that were merged
            for r in ranges_to_be_removed:
                merged.remove(r)

        # add the final merged range
        merged.append((start, end))

    total_elements = sum(end - start + 1 for start, end in merged)
    return total_elements


# print(len(product_ranges)) # 189
print(
    "Count of unique numbers in ranges (correct):",
    part2_buggy(product_ranges),
)
print(
    "Count of unique numbers in ranges (example, correct):",
    part2_buggy(example_ranges),
)
print(
    "Count of unique numbers in ranges (old buggy):",
    part2_old_buggy_fixed(example_ranges),
)
print(
    "Count of unique numbers in ranges (old buggy fixed):",
    part2_old_buggy_fixed(product_ranges),
)


def part2_ai_sorting(product_ranges: List[tuple]) -> int:
    """
    Merge overlapping or touching ranges (inclusive). Then count the total number
    of unique integers covered by the merged ranges.
    """
    if not product_ranges:
        return 0

    # Normalize ranges to ensure start <= end and remove any invalid entries
    normalized = [(min(s, e), max(s, e)) for s, e in product_ranges]

    # Sort by start
    normalized.sort(key=lambda x: x[0]) # INTERESTING

    merged = [] # START WITH EMPTY LIST, NO NEED FOR RECHECKING
    cur_start, cur_end = normalized[0] # WORK WITH TUPLS. INSTEAD OF INDEPENEDENT VARIABLES

    for start, end in normalized[1:]:
        # If ranges overlap or touch (inclusive), extend current
        # Touching means start <= cur_end + 1 to ensure continuity.
        if start <= cur_end + 1:
            cur_end = max(cur_end, end) # ONLY NEED TO CHECK END AS THEY ARE ALL SORTED BY START
        else:
            merged.append((cur_start, cur_end))
            cur_start, cur_end = start, end

    # Append the last active range
    merged.append((cur_start, cur_end))

    # Inclusive count of unique numbers
    total_elements = sum(e - s + 1 for s, e in merged)
    return total_elements

print(
    "Count of unique numbers in ranges (old buggy fixed):",
    part2_ai_sorting(product_ranges),
)

# Based on part2_ai_sorting (captial letters comments) and to part2_buggy compared to part2_old_buggy_fixed write here down in bullets my learnings:
# Learnings from implementing range merging:
# - Sorting the ranges by start simplifies merging logic and avoids repeated re-checking.
# - Always normalize input ranges to ensure start <= end.
# - When merging, only need to compare current range with the last merged one if sorted.
# - Overlapping or touching ranges can be merged by extending the end.
# - Removing and updating ranges on-the-fly (without sorting) is error-prone and requires repeated checks.
# - Using a while loop to recheck merges is less efficient than sorting first.
# - Inclusive counting (end - start + 1) is important for correct range size.
# - Clean code is easier to debug and reason about than complex, on-the-fly modifications.

# Use debugger, while loop 