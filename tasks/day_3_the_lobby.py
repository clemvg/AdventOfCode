"""Day 3: The Lobby."""
from utils import common


EXAMPLE = [
    987654321111111,
    811111111111119,
    234234234234278,
    818181911112111,
]

# -------- Constants --------
INPUT_PATH = "input/input_day_3.txt"
INPUT_DATA = common.read_text_to_list_of_ints(INPUT_PATH)


# -------- Approach --------
# Problem: Find, for each digit string (battery bank), the maximum two-digit number formed by selecting two digits in their original order, then sum these maxima across all banks.

# Bruteforce: for each integer check seauentially the digits, keep always track of the maximum found so far, remember the place (index) and the number itself
# Second_number pass same logic but skipping the index found in first pass. 
# Put the two digits after each other to get a number
# Loop over all ints with previous logic and each time add the two foudn digit new numbere for the sum 

# Part two probably many batteries... find a general way to do it
# -------- Solutions --------

def max_bank_joltage(bank: int) -> int:
    """
    Given a bank represented as an integer (digits 1-9), find the maximum two-digit
    number formed by selecting two digits in their original order.
    """
    # TODO: make more generalizable to n-digit numbers, recursive ? 
    s = str(bank)
    if len(s) < 2:
        raise ValueError("Bank must have at least two digits.")

    # keep track the maximum first digit seen so far (from the left), then for each position j
    # form a two-digit number with that max-first-digit and s[j]
    # better approach than just keeping track of the max digit betwen 1 and 9, as this logic can be generalized: multiple for loops and 10^n multipliers
    # nevertheless more a brute force approach, more co,binatiosn are tested 
    best_tens_so_far = int(s[0])
    best_two_digit_so_far = 0

    for j in range(1, len(s)):
        second_number = int(s[j])
        candidate = 10 * best_tens_so_far + second_number
        if candidate > best_two_digit_so_far:
            best_two_digit_so_far = candidate
        # Update best_tens_so_far with the best prefix digit seen so far
        if second_number > best_tens_so_far:
            # second_number is at position j, but it can't pair with itself for this j;
            # still, it becomes the prefix max for future positions.
            best_tens_so_far = second_number

    return best_two_digit_so_far

def part_2_generalized_max_bank_joltage(bank: int, k: int) -> int: 
    # OTHER APPROACH: stack and push number to stack, pop when needed to form n-digit number
    """
    Greedy idea paritally got via AI: remove up to n-k smaller leading digits to favor larger digits earlier.
    """
    digits = list(str(bank))
    n = len(digits)
    if k <= 0 or k > n:
        raise ValueError("k must be between 1 and the number of digits in the bank")

    # nmber digits to remove to get k digits
    removals = n - k
    result_stack: list[str] = []

    for digit in digits:
        # while we can remove digits and the current digit is greater than the last in stack,
        # pop from stack to favor larger digits earlier
        while removals > 0 and result_stack and digit > result_stack[-1]:
            result_stack.pop()
            # you can safely pop because the first encountered digit cannot be placed after the current digit (order preserved)
            removals = removals - 1
        result_stack.append(digit)

    # if no pops happen eg 987654321, trim from the end to get exactly k digits
    best_k_digits = result_stack[:k]
    return int("".join(best_k_digits)) # convert back strings to integer

def total_output_joltage(banks: list[int], k: int) -> int:
    # warpper for simple summation
    return sum(part_2_generalized_max_bank_joltage(bank, k) for bank in banks)


def solve_day_3() -> tuple[int, int]:
    """
    Returns (example_total, input_total)
    """
    example_total = total_output_joltage(EXAMPLE, 2)
    input_total = total_output_joltage(INPUT_DATA, 2)
    input_total_k12 = total_output_joltage(INPUT_DATA, 12)
    return example_total, input_total, input_total_k12


if __name__ == "__main__":
    example_total, input_total, input_total_k12 = solve_day_3()
    print(f"Day 3 - Example total output joltage: {example_total}")
    print(f"Day 3 - Input total output joltage: {input_total}")
    print(f"Day 3 - Input total output joltage (k=12): {input_total_k12}")

