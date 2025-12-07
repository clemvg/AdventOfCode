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