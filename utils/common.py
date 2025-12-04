"""Common utility functions for file reading and parsing."""
from typing import List, Tuple

# text can be in one line or multiple lines, so strip by default
# Strip removes leading and trailing whitespace characters (including newlines) from each line.

def read_text_to_list_of_strings(path: str , strip: bool = True) -> List[str]:
    """Read a text file line by line and return a list of lines."""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines() if strip else f.readlines()
    return lines

# TODO: merge with prev def by adding output_var_type arg
def read_text_to_list_of_ints(path: str, strip: bool = True) -> List[int]:
    """Read a text file line by line and return a list of integers."""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines() if strip else f.readlines()
    return [int(line) for line in lines if line.strip()]

def read_text_to_list_of_tuples(path: str, delimiter: str = "-") -> List[Tuple[int, ...]]:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    parts = [p.strip() for p in text.split(",") if p.strip()]
    return [tuple(map(int, p.split(delimiter))) for p in parts]

# TODO: add helpers to transform into other structures (e.g., dict, tuples, parsed objects).
