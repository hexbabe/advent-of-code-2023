"""
--- Day 2: Cube Conundrum ---
You're launched high into the atmosphere! The apex of your trajectory just barely
reaches the surface of a large island floating in the sky. You gently land in a
fluffy pile of leaves. It's quite cold, but you don't see much snow. An Elf runs
over to greet you.

The Elf explains that you've arrived at Snow Island and apologizes for the lack
of snow. He'll be happy to explain the situation, but it's a bit of a walk, so you
have some time. They don't get many visitors up here; would you like to play a game
in the meantime?

As you walk, the Elf shows you a small bag and some cubes which are either red,
green, or blue. Each time you play this game, he will hide a secret number of cubes
of each color in the bag, and your goal is to figure out information about the number
of cubes.

To get information, once a bag has been loaded with cubes, the Elf will reach into
the bag, grab a handful of random cubes, show them to you, and then put them back
in the bag. He'll do this a few times per game.

You play several games and record the information from each game (your puzzle input).
Each game is listed with its ID number (like the 11 in Game 11: ...) followed by a
semicolon-separated list of subsets of cubes that were revealed from the bag (like
3 red, 5 green, 4 blue).

For example, the record of a few games might look like this:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
In game 1, three sets of cubes are revealed from the bag (and then put back again).
The first set is 3 blue cubes and 4 red cubes; the second set is 1 red cube, 2 green
cubes, and 6 blue cubes; the third set is only 2 green cubes.

The Elf would first like to know which games would have been possible if the bag
contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

In the example above, games 1, 2, and 5 would have been possible if the bag had been
loaded with that configuration. However, game 3 would have been impossible because at
one point the Elf showed you 20 red cubes at once; similarly, game 4 would also have
been impossible because the Elf showed you 15 blue cubes at once. If you add up the IDs
of the games that would have been possible, you get 8.

Determine which games would have been possible if the bag had been loaded with only 12
red cubes, 13 green cubes, and 14 blue cubes. What is the sum of the IDs of those games?
"""
from typing import List, Tuple


MAX_REDS = 12
MAX_GREENS = 13
MAX_BLUES = 14


### Pre-processing (parsing input into objects; i looove objects)
class Round:
    def __init__(self, round_number: int, reds = 0, greens = 0, blues = 0):
        self.round_number = round_number
        self.reds = reds
        self.greens = greens
        self.blues = blues

    def _get_only_numeric_from_str(self, s: str):
        acc = ""
        for char in s:
            if char.isnumeric():
                acc += char
        return acc
    
    def set_count(self, count_str: str):
        count = int(self._get_only_numeric_from_str(count_str))
        if "red" in count_str:
            self.reds = count
        elif "green" in count_str:
            self.greens = count
        elif "blue" in count_str:
            self.blues = count
        else:
            Exception("wtf input")
    
    def __repr__(self) -> str:
        return f"\nRound {self.round_number}: Red: {self.reds}, Green: {self.greens}, Blue: {self.blues}"


class Game:
    def __init__(self, game_str: str):
        # Parse id
        game_id_str, rounds_str = game_str.split(":")
        self.id = int(game_id_str.split(" ")[1])

        # Parse rounds
        round_str_list = rounds_str.split(";")
        self.rounds: List[Round] = []
        for index, round_str in enumerate(round_str_list):
            round = Round(index)
            count_str_list = round_str.split(",")
            for count_str in count_str_list:
                round.set_count(count_str)
            self.rounds.append(round)

    def get_min_number_cubes_needed(self) -> Tuple[int, int, int]:
        red_counts = [round.reds for round in self.rounds]
        green_counts = [round.greens for round in self.rounds]
        blue_counts = [round.blues for round in self.rounds]
        return max(red_counts), max(green_counts), max(blue_counts)  # max calculates min needed

    def __repr__(self) -> str:
        return f"\nGame: {self.id} {self.rounds}"
      

### Solve
def get_answer_part_1(games: List[Game]):
    id_sum = 0
    for game in games:
        impossible = False
        for round in game.rounds:
            impossible = impossible or round.reds > MAX_REDS or round.greens > MAX_GREENS or round.blues > MAX_BLUES
        if not impossible:
            id_sum += game.id

    print(f"Dec 2 part 1: {id_sum}")
    return id_sum

def get_answer_part_2(games: List[Game]):
    powers_sum = 0
    for game in games:
        min_reds, min_greens, min_blues = game.get_min_number_cubes_needed()
        powers_sum += min_reds * min_greens * min_blues
    print(f"Dec 2 part 2: {powers_sum}. ez clap ggs")
    return powers_sum

if __name__ == "__main__":
    games_str_list = open('./dec_2/input.txt', 'r').readlines()  # run script from outer dir
    games = []
    for game_str in games_str_list:
        game = Game(game_str)
        games.append(game)

    get_answer_part_1(games)
    get_answer_part_2(games)
