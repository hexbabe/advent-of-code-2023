"""
--- Day 3: Gear Ratios ---
You and the Elf eventually reach a gondola lift station; he says the gondola
lift will take you up to the water source, but this is as far as he can bring
you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem:
they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of
surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working
right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine,
but nobody can figure out which one. If you can add up all the part numbers
in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation
of the engine. There are lots of numbers and symbols you don't really
understand, but apparently any number adjacent to a symbol, even diagonally,
is a "part number" and should be included in your sum.
(Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not
adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number
is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all
of the part numbers in the engine schematic?

Your puzzle answer was 533784.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
The engineer finds the missing part and installs it in the engine! As the engine
springs to life, you jump in the closest gondola, finally ready to ascend to the
water source.

You don't seem to be going very fast, though. Maybe something is still wrong?
Fortunately, the gondola has a phone labeled "help", so you pick it up and the
engineer answers.

Before you can explain the situation, she suggests that you look out the window.
There stands the engineer, holding a phone in one hand and waving with the other.
You're going so slowly that you haven't even left the station. You exit the
gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong.
A gear is any * symbol that is adjacent to exactly two part numbers. Its gear
ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so
that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, there are two gears. The first is in the top left; it has part
numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower
right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it
is only adjacent to one part number.) Adding up all of the gear ratios produces
467835.

What is the sum of all of the gear ratios in your engine schematic?
"""
# kinda spaghetti code today bc i wasn't feeling well

NON_ENGINE_PARTS = {".", "\n"}
LINES = open('./dec_3/input.txt', 'r').readlines()  # run script from outer dir

def is_engine_part(char: str):
    return not char.isnumeric() and char not in NON_ENGINE_PARTS

def is_row_inbounds(row):
    min_row, max_row = 0, len(LINES) - 1
    return row >= min_row and row <= max_row

def is_col_inbounds(col):
    min_col, max_col = 0, len(LINES[0]) -  1
    return col >= min_col and col <= max_col

def find_num_left(row: int, col: int):
    acc = ""
    char = LINES[row][col]
    while is_col_inbounds(col) and char.isnumeric():
        acc = char + acc
        col -= 1
        char = LINES[row][col]
    start_col = col + 1
    return acc, start_col

def find_num_right(row: int, col: int):
    if not is_col_inbounds(col):
        return ""
    acc = ""
    char = LINES[row][col]
    while is_col_inbounds(col) and char.isnumeric():
        acc += char
        col += 1
        char = LINES[row][col]
    return acc
        
def find_number(row: int, col: int):
    char = LINES[row][col]
    if char.isnumeric():
        num_left, start_col = find_num_left(row, col)
        num_right = find_num_right(row, col + 1)
        return int(num_left + num_right), start_col
    return None, None

def get_all_adjacent_nums(row: int, col: int):
    nums = []
    for i in range(row - 1, row + 2):
        seen_start_cols = set()
        for j in range(col - 1, col + 2):
            if is_row_inbounds(i) and is_col_inbounds(j):
                num_or_none, start_col = find_number(i, j)
                if num_or_none is not None and start_col not in seen_start_cols:
                    num = num_or_none
                    seen_start_cols.add(start_col)
                    nums.append((num, start_col))
    return nums

def get_gear_ratio(row: int, col: int):
    nums = []
    for i in range(row - 1, row + 2):
        seen_start_cols = set()
        for j in range(col - 1, col + 2):
            if is_row_inbounds(i) and is_col_inbounds(j):
                num_or_none, start_col = find_number(i, j)
                if num_or_none is not None and start_col not in seen_start_cols:
                    num = num_or_none
                    seen_start_cols.add(start_col)
                    nums.append((num, start_col))
    if len(nums) == 2:
        return nums[0][0] * nums[1][0]
    return 0

if __name__ == "__main__":
    total_sum = 0
    gear_ratios_sum = 0
    for row, line in enumerate(LINES):
        for col, char in enumerate(line):
            if is_engine_part(char):
                # Part 1
                nums = get_all_adjacent_nums(row, col)
                for num, _ in nums:
                    total_sum += num
                # Part 2
                gear_ratio = get_gear_ratio(row, col)
                gear_ratios_sum += gear_ratio

    print(f"Dec 3 part 1: {total_sum}")
    print(f"Dec 3 part 2: {gear_ratios_sum}. :>")
