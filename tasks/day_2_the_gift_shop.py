"""Day 2: Gift Shop."""
from typing import List, Tuple
from utils import common

[ # product ID RANGES(!)
    (11, 22), (95, 115), (998, 1012), (1188511880, 1188511890), (222220, 222224),
    (1698522, 1698528), (446443, 446449), (38593856, 38593862), (565653, 565659),
    (824824821, 824824827), (2121212118, 2121212124)
]
INPUT_DATA = common.read_text_to_list_of_tuples("input/input_day_2.txt", delimiter="-")
# Digits: single characters 0–9.

# 11-22 has two invalid IDs, 11 and 22.
# 95-115 has one invalid ID, 99. 
# 998-1012 has one invalid ID, 1010. 
# 1188511880-1188511890 has one invalid ID, 1188511885.
# 222220-222224 has one invalid ID, 222222.
# 1698522-1698528 contains no invalid IDs.
# 446443-446449 has one invalid ID, 446446.
# 38593856-38593862 has one invalid ID, 38593859.
# The rest of the ranges contain no invalid IDs.

# -------- Approach --------
# Identify the invalid product IDs (getting first and last ids)
# Invalid ID = which is made only of some sequence of digits repeated twice
# No leading zeros allowed in IDs. So “0101” isn’t an ID at all, even though it looks like “01” + “01”.
# Only numbers that are exactly two equal-length digit blocks concatenated are “invalid.” “101” has three digits, so it can’t be split into two equal halves; you ignore it in the invalid-check logic.
# Adding up all the invalid IDs at the end = solution

def solve_invalid_product_ids(ranges: List[Tuple[int, int]]):
    """"""
    invalid_ids = []
    # loop over all numbers
    for start, end in ranges:
        current_number = start
        end_number = end

        # iterate until we pass the end
        while current_number <= end_number:
            # if current number > end
            # break / or while

            s = str(current_number)

            # if current number start with zero as fist number
            if s.startswith("0"):
                pass
            else:
                # if not even pass
                if len(s) % 2 != 0:
                    pass
                else:
                    # else: check if two ghalves are the same
                    mid = len(s) // 2
                    left = s[:mid]
                    right = s[mid:]

                    # if two halves are the same append to invalid invalid_ids
                    if left == right:
                        invalid_ids.append(current_number)

            # current_number = current_number + 1
            current_number = current_number + 1

    # calculate the sume
    return sum(invalid_ids), invalid_ids

if __name__ == "__main__":
    total, ids = solve_invalid_product_ids(INPUT_DATA)
    print(f"Sum of invalid IDs: {total}")
    print(f"Invalid IDs count: {len(ids)}")
        
        
        