"""Modulo explanation below"""

from utils import common

# -------- Constants --------
INPUT_PATH = "input/input_day_1.txt"
INPUT_DATA = common.read_text_to_list_of_strings(INPUT_PATH)
EXAMPLE_ROTATIONS = [
    "L68",
    "L30",
    "R48",
    "L5",
    "R60",
    "L55",
    "L1",
    "L99",
    "R14",
    "L82",
]

# -------- Modulo Explanation --------
# Modulo operator (%) gives the remainder of a division
# Example: 7 % 3 = 1 because 7 = 2*3
# Example: -7 % 3 = 2 because -7 = -3*3 + 2
# In Python, the result of a % n has the same sign as n
# So for positive n, a % n is always between 0 and n-1

# In puzzle,
# modulo 100 always a number between 0 and 100
# Negative numbers --> floor down
# Definition: a % n = a - n × ⌊a/n⌋
# Starting at -17, if we keep adding 5 until we get positive
# -5 % 100 = 95   # -5 + 100 = 95
# a % positive → always gives 0 to positive-1

# -------- Approach --------
# Start at position 50 on a dial of length 100 (0 to 99)
# For each rotation:
#   - If 'L', move left (decrease position)
#   - If 'R', move right (increase position)
#   - Use modulo 100 to wrap around the dial
# Count how many times we land on 0 after each rotation (Part 1)
# For Part 2, count how many times we pass through 0 during each rotation

# Initial variables needed
# postion, password_count

# Note if you are neding at 0, extra count

# bijvoorbeeld als je op 0 stopt en dan draai je 100 keer in eender welke richting, dan ga je nog altijd geen 0 passeren, terwijl als je op eender welke ander getal eindigt en dan 100 keer draait, passeer je wel sws 0


# -------- Solutions --------
def solve_safe_password(rotations):
    """
    Calculate the password by counting how many times the dial points to 0
    after any rotation in the sequence.

    Args:
        rotations: List of strings like ['R46', 'L12', 'R1', ...]

    Returns:
        Number of times the dial lands on 0
    """
    position = 50
    password_count = 0

    for rotation in rotations:
        direction = rotation[0]  # 'L' or 'R'
        distance = int(rotation[1:])

        if direction == "L":
            # Left means toward lower numbers
            position = (position - distance) % 100
        else:  # direction == 'R'
            # Right means toward higher numbers
            position = (position + distance) % 100

        # Count if we land on 0
        if position == 0:
            password_count += 1

    return password_count


# optional: merge with previous function for efficiency with extra parameter
def solve_click_password(rotations):
    """
    Calculate the password by counting how many times the dial points to 0
    during any click of the dial (including when the rotation ends).
    """
    position = 50
    password_count = 0

    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])

        if direction == "R":
            # First time we can reach 0 when moving right; treat 0 as 100 if we start at 0
            first_hit = (
                100 - position
            ) % 100 or 100  # to know how many clicks to reach 0, when pos is zero, first_hit should be 100
            if distance >= first_hit:
                password_count += (
                    1 + (distance - first_hit) // 100
                )  # one for first hit, rest for every 100 clicks
            position = (position + distance) % 100  # update position
        else:
            # Moving left; first time we can reach 0 is after `position` clicks (or 100 if already on 0)
            first_hit = position or 100
            if distance >= first_hit:
                password_count += 1 + (distance - first_hit) // 100
            position = (position - distance) % 100

    return password_count


# -------- Ruben's Dial Implementation (Bruteforce) --------
# dus als je 10.000 keer roteert, doe je dat in een loop van 10.000 iteraties
class Dial:
    def __init__(self, length):
        self.length = length
        self.possible_choises = [i for i in range(length)]
        self.current_pos = length // 2
        self.zero_count = 0

    def get(self):
        return self.possible_choises[self.current_pos]

    def rotate_left(self):
        new_pos = self.current_pos - 1
        if new_pos == -1:
            new_pos = self.length - 1
        self.current_pos = new_pos
        if self.current_pos == 0:
            self.zero_count += 1

    def rotate_x_left(self, x):
        for _ in range(x):
            self.rotate_left()

    def rotate_right(self):
        new_pos = self.current_pos + 1
        if new_pos == self.length:
            new_pos = 0
        self.current_pos = new_pos
        if self.current_pos == 0:
            self.zero_count += 1

    def rotate_x_right(self, x):
        for _ in range(x):
            self.rotate_right()


# -------- Main --------
def main():
    # --------- PERSONAL SOLUTION --------
    # Example checks
    test_result = solve_safe_password(EXAMPLE_ROTATIONS)
    print(f"Example result: {test_result} (expected: 3)")
    test_result_part2 = solve_click_password(EXAMPLE_ROTATIONS)
    print(
        f"Example result (method 0x434C49434B): {test_result_part2} (expected: 6)"
    )
    print()

    # Part 1
    my_list = INPUT_DATA
    result = solve_safe_password(my_list)
    print(f"Final result: {result}")

    # Part 2
    result_part2 = solve_click_password(my_list)
    print(f"Final result (method 0x434C49434B): {result_part2}")

    # -------- RUBEN'S SOLUTION --------
    # Ruben's solution part 1
    dial_part1 = Dial(100)
    zero_landings_part1 = 0
    for rotation in INPUT_DATA:
        direction = rotation[0]
        distance = int(rotation[1:])
        if direction == "L":
            dial_part1.rotate_x_left(distance)
        else:
            dial_part1.rotate_x_right(distance)
        if dial_part1.get() == 0:
            zero_landings_part1 += 1
    print(f"Ruben's solution part 1: {zero_landings_part1}")
    # Ruben's solution part 2
    dial = Dial(100)
    for rotation in INPUT_DATA:
        direction = rotation[0]
        distance = int(rotation[1:])
        if direction == "L":
            dial.rotate_x_left(distance)
        else:
            dial.rotate_x_right(distance)
    print(f"Ruben's solution part 1: {dial.zero_count}")


if __name__ == "__main__":
    main()
