"""
--- Day 1: Trebuchet?! ---
Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given you a map; on it,
they've used stars to mark the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked
when you complete the first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you ("the sky") and 
why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the sky ("of course, where do you 
think snow comes from") when you realize that the Elves are already loading you into a trebuchet ("please hold still, we need to strap
you in").

As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very
young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values
on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that
the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit
(in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?

--- Part Two ---
Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters:
one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?
"""

DIGITS_AS_LETTERS = {str(num) for num in range(1, 10)}  # input doesn't contain 0s
DIGIT_WORD_TO_NUM = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}
FULL_INPUT = open("./dec_1/input.txt").read()  # run script from outer directory
LINES = FULL_INPUT.split("\n")

def get_value_from_line_1(line):
    """The way to process each line in part 1

    Args:
        line (str)

    Returns:
        int: calibration value from one line that the inept elf wrote
    """
    tens_digit, ones_digit = None, None
    for char in line:
        if char in DIGITS_AS_LETTERS:
            if tens_digit is None:
                tens_digit = int(char)
            ones_digit = int(char)
    return tens_digit * 10 + ones_digit

def get_value_from_line_2(line):
    """The way to process each line in part 2

    Args:
        line (str)

    Returns:
        int: calibration value from one line that the inept elf wrote
    """
    def get_digit_word_in_string(s):
        for digit_word in DIGIT_WORD_TO_NUM:
            if digit_word in s:
                return digit_word
        return None
    
    def get_next_digit_and_next_index(index):
        acc = ""
        while index < len(line):
            char = line[index]
            # Check if numeric digit letter came first
            if char in DIGITS_AS_LETTERS:
                return int(char), index + 1
            # Now check if acc has a word in it
            acc += char
            either_a_word_or_none = get_digit_word_in_string(acc)
            if either_a_word_or_none is not None:
                word = either_a_word_or_none
                return DIGIT_WORD_TO_NUM[word], index  # no increment on index due to possible overlap
            index += 1
        return None, None

    tens_digit, ones_digit, index = None, None, 0

    while True:
        digit, index = get_next_digit_and_next_index(index)
        if index is None:  # reached end of line
            break
        
        if tens_digit is None:
            tens_digit = digit
        ones_digit = digit

    return tens_digit * 10 + ones_digit

def get_answer(get_value_from_line):    
    values_sum = 0
    for line in LINES:
        values_sum += get_value_from_line(line)
    return values_sum

if __name__ == "__main__":
    print(get_answer(get_value_from_line_1))
    print(get_answer(get_value_from_line_2))
