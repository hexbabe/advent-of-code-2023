"""
--- Day 4: Scratchcards ---
The gondola takes you up. Strangely, though, the ground doesn't seem to be coming with you;
you're not climbing a mountain. As the circle of Snow Island recedes below you, an entire
new landmass suddenly appears above you! The gondola carries you to the surface of the new
island and lurches into the station.

As you exit the gondola, the first thing you notice is that the air here is much warmer than
it was on Snow Island. It's also quite humid. Is this where the water source is?

The next thing you notice is an Elf sitting on the floor across the station in what seems to
be a pile of colorful square cards.

"Oh! Hello!" The Elf excitedly runs over to you. "How may I be of service?" You ask about water
sources.

"I'm not sure; I just operate the gondola lift. That does sound like something we'd have, though
- this is Island Island, after all! I bet the gardener would know. He's on a different island,
though - er, the small kind surrounded by water, not the floating kind. We really need to come
up with a better naming scheme. Tell you what: if you can help me with something quick, I'll let
you borrow my boat and you can go visit the gardener. I got all these scratchcards as a gift,
but I can't figure out what I've won."

The Elf leads you over to the pile of colorful cards. There, you discover dozens of scratchcards,
all with their opaque covering already scratched off. Picking one up, it looks like each card has
two lists of numbers separated by a vertical bar (|): a list of winning numbers and then a list
of numbers you have. You organize the information into a table (your puzzle input).

As far as the Elf has been able to figure out, you have to figure out which of the numbers you
have appear in the list of winning numbers. The first match makes the card worth one point and each
match after the first doubles the point value of that card.

For example:

Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
In the above example, card 1 has five winning numbers (41, 48, 83, 86, and 17) and eight numbers you
have (83, 86, 6, 31, 17, 9, 48, and 53). Of the numbers you have, four of them (48, 83, 17, and 86)
are winning numbers! That means card 1 is worth 8 points (1 for the first match, then doubled three
times for each of the three matches after the first).

Card 2 has two winning numbers (32 and 61), so it is worth 2 points.
Card 3 has two winning numbers (1 and 21), so it is worth 2 points.
Card 4 has one winning number (84), so it is worth 1 point.
Card 5 has no winning numbers, so it is worth no points.
Card 6 has no winning numbers, so it is worth no points.
So, in this example, the Elf's pile of scratchcards is worth 13 points.

Take a seat in the large pile of colorful cards. How many points are they worth in total?
"""
from collections import deque
from typing import List, Mapping
CARDS = open('./dec_4/input.txt', 'r').readlines()  # run script from outer dir

def get_answer_part_1(cards: List[str]):
    assert len(cards) == 205
    total_pay = 0
    for card in cards:
        winning_nums_str, my_nums_str = card.split(":")[-1].split("|")
        winning_nums_uncleaned = winning_nums_str.split(" ")
        my_nums_uncleaned = my_nums_str.split(" ")

        winning_nums = [int(num) for num in winning_nums_uncleaned if num != ""]
        assert len(winning_nums) == 10
        my_nums = [int(num) for num in my_nums_uncleaned if num != ""]
        assert len(my_nums) == 25
        card_num = int(card.split(":")[0].split(" ")[-1])
        pay = 0
        for my_num in my_nums:
            if my_num in winning_nums:
                if pay == 0:
                    pay = 1
                else:
                    pay *= 2
        total_pay += pay
    return total_pay

class Card:
    winning_nums = set()
    my_nums = []
    num = None
    matches = 0
    def __init__(self, winning_nums: set, my_nums: List[int], num: int):
        self.winning_nums = winning_nums
        self.my_nums = my_nums
        self.num = num
        self.matches = self.get_num_matches()

    def get_num_matches(self) -> int:
        matches = 0
        for my_num in self.my_nums:
            if my_num in self.winning_nums:
                matches += 1
        return matches

def get_answer_part_2(cards_str: List[str]):
    def parse_cards() -> Mapping[int, Card]:
        cards = dict()
        for card_str in cards_str:
            winning_nums_str, my_nums_str = card_str.split(":")[-1].split("|")
            winning_nums_uncleaned = winning_nums_str.split(" ")
            my_nums_uncleaned = my_nums_str.split(" ")

            winning_nums = [int(num) for num in winning_nums_uncleaned if num != ""]
            my_nums = [int(num) for num in my_nums_uncleaned if num != ""]
            card_num = int(card_str.split(":")[0].split(" ")[-1])
            cards[card_num] = Card(winning_nums, my_nums, card_num)
        return cards

    cards = parse_cards()
    q = deque()
    q.extend(cards.values())
    acc = 0
    while len(q) != 0:
        card: Card = q.pop()
        acc += 1
        for card_num in range(card.num + 1, card.num + card.matches + 1):
            q.append(cards[card_num])  # can probably memo-ize this or something
    return acc


if __name__ == "__main__":
    print(f"Dec 4 part 1: {get_answer_part_1(CARDS)}")
    print(f"Dec 4 part 2: {get_answer_part_2(CARDS)}")

