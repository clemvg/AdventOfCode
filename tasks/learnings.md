# Advent of Code - Learnings

## General Notes
- Try a way to fix pythonpath issue
- Use debugger (can also be used in api)

## Day 1 - 4
todo

## Day 5: Cafeteria Ranges Checking (Part 2)

### AI Solution
- Sorting the ranges by start simplifies merging logic and avoids repeated re-checking.
- When merging, only need to compare current range with the last merged one if sorted.

### Personal Solution
- Removing and updating ranges on-the-fly (without sorting) is error-prone and requires repeated checks!
- Using a while loop to recheck merges is less efficient than sorting first.
- Clean code and var names is easier to debug and reason of my first buggy solution especially for on-the-fly modifications.

## Day 6: The Trash Compactor

- Equal padding of lines via line.ljust(max_width)
- While loop of cols might be interesting to spot whitespace columns between number columns
- Not working with while loop suggests using the prior parse_input function for part 1 and adding whitespaces to the left (because right-aligned) to have max equal length of the numbers

## Day 7: Laboratories

### Core Concept
Two fundamentally different problems requiring different approaches:

**Part 1: Event Simulation** - "How many splitting events occur during the simulation?"
- **Strategy**: BFS/while loop with beam tracking
- **Focus**: Simulate the process, count events as they happen
- **Pattern**: Standard left/right beam creation pattern
- **Key**: Track visited splitters to avoid double-counting

**Part 2: Path Combinatorics** - "How many different complete journeys are possible?"
**Strategy 1: Recursive approach with memoization**
- **Focus**: Calculate mathematical combinations of all possible routes
- **Pattern**: Position-based memoization with return counts
- **Key**: Memoization prevents recalculating the same subproblems

**Strategy 2: Bottom-up Dynamic Programming**
- **Focus**: Work backwards from bottom row to eliminate recursion
- **Pattern**: Build timeline counts layer by layer from bottom to top
- **Key**: Each position's count = sum of its children's counts (for splitters)
- **Advantage**: No recursion stack overhead, more intuitive flow

Both approaches are present in the solution file. 

### Algorithm Comparison

| Aspect | Part 1 (Event Counting) | Part 2 (Path Counting) |
|--------|-------------------------|------------------------|
| **Method** | BFS simulation | Recursive DP |
| **Data Structure** | List of active beams | Memo dictionary |
| **Question** | "When do splits happen?" | "How many ways to exit?" |
| **Complexity** | O(splits × beams) | O(rows × cols) |

### Example Walkthrough
```
Part 1 - Event Counting:
Step 1: [Beam at S]
Step 2: [Beam hits first ^] → COUNT +1, create [BeamLeft, BeamRight] 
Step 3: [BeamLeft hits next ^, BeamRight continues] → COUNT +1 for new splitter
Result: Total number of unique split events

Part 2 - Path Counting:
From S: How many ways to reach bottom?
├── If go through splitter: left_ways + right_ways
├── If continue straight: same as next position
└── Recursively calculate for each position
Result: Total number of complete paths
```

**Key Insight**: Part 1 simulates the physical process; Part 2 calculates mathematical possibilities.

- TODO: Reproduce Part 2 independently (required AI assistance)