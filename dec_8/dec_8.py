"""
--- Day 8: Haunted Wasteland ---
You're still riding a camel across Desert Island when you spot a sandstorm quickly approaching. When
you turn to warn the Elf, she disappears before your eyes! To be fair, she had just finished warning
you about ghosts a few minutes ago.

One of the camel's pouches is labeled "maps" - sure enough, it's full of documents (your puzzle input)
about how to navigate the desert. At least, you're pretty sure that's what they are; one of the
documents contains a list of left/right instructions, and the rest of the documents seem to describe
some kind of network of labeled nodes.

It seems like you're meant to use the left/right instructions to navigate the network. Perhaps if you
have the camel follow the same instructions, you can escape the haunted wasteland!

After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where you
are now, and you have to follow the left/right instructions until you reach ZZZ.

This format defines each node of the network individually. For example:

RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
Starting with AAA, you need to look up the next element based on the next left/right instruction in
your input. In this example, start with AAA and go right (R) by choosing the right element of AAA, CCC.
Then, L means to choose the left element of CCC, ZZZ. By following the left/right instructions, you
reach ZZZ in 2 steps.

Of course, you might not find ZZZ right away. If you run out of left/right instructions, repeat the
whole sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL... and so on. For example,
here is a situation that takes 6 steps to reach ZZZ:

LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?

--- Part Two ---
The sandstorm is upon you and you aren't any closer to escaping the wasteland. You had the camel follow
the instructions, but you've barely left your starting position. It's going to take significantly more
steps to escape!

What if the map isn't for people - what if the map is for ghosts? Are ghosts even bound by the laws of
spacetime? Only one way to find out.

After examining the maps a bit longer, your attention is drawn to a curious fact: the number of nodes with
names ending in A is equal to the number ending in Z! If you were a ghost, you'd probably just start at
every node that ends with A and follow all of the paths at the same time until they all simultaneously end
up at nodes that end with Z.

For example:

LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
Here, there are two starting nodes, 11A and 22A (because they both end with A). As you follow each left/right
instruction, use that instruction to simultaneously navigate away from both nodes you're currently on. Repeat
this process until all of the nodes you're currently on end with Z. (If only some of the nodes you're on end
with Z, they act like any other node and you continue as normal.) In this example, you would proceed as follows:

Step 0: You are at 11A and 22A.
Step 1: You choose all of the left paths, leading you to 11B and 22B.
Step 2: You choose all of the right paths, leading you to 11Z and 22C.
Step 3: You choose all of the left paths, leading you to 11B and 22Z.
Step 4: You choose all of the right paths, leading you to 11Z and 22B.
Step 5: You choose all of the left paths, leading you to 11B and 22C.
Step 6: You choose all of the right paths, leading you to 11Z and 22Z.
So, in this example, you end up entirely on nodes that end in Z after 6 steps.

Simultaneously start on every node that ends with A. How many steps does it take before you're only on nodes
that end with Z?
"""
from typing import Callable, Dict, List


LINES = open('./dec_8/input.txt', 'r').readlines()

class Node:
    name: str
    left_name: str
    right_name: str

    def __init__(self, name: str, left_name: str, right_name: str):
        self.name = name
        self.left_name = left_name
        self.right_name = right_name

    def __repr__(self) -> str:
        return str({
            "name": self.name,
            "left": self.left_name,
            "right": self.right_name
        })

def get_num_steps_part_1(
        directions: str,
        nodes: Dict[str, Node],
        start_node_name: str,
        is_end_node_name: Callable
    ):
    cur_node = nodes[start_node_name]
    steps = 0
    while True:
        for direction in directions:
            if direction == "L":
                cur_node = nodes[cur_node.left_name]
            if direction == "R":
                cur_node = nodes[cur_node.right_name]
            steps += 1
            if is_end_node_name(cur_node.name):
                return steps

def print_answer_part_1():
    directions: str = ""
    nodes: Dict[str, Node] = dict()
    for i, line in enumerate(LINES):
        # pre-process line
        line = line.replace("\n", "")
        line = line.replace(" ", "")
        line = line.replace("(", "")
        line = line.replace(")", "")

        # special cases
        if i == 0:
            directions = line
            continue
        if i == 1:
            continue

        node_name, l_r_str = line.split("=")
        left_name, right_name = l_r_str.split(",")
        node = Node(node_name, left_name, right_name)
        nodes[node_name] = node

    num_steps = str(get_num_steps_part_1(
                directions,
                nodes,
                start_node_name="AAA",
                is_end_node_name=lambda s: s == "ZZZ"
            )
        )
    print("Dec 8 part 1: " + num_steps)

def lcm(numbers):
    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a

    lcm = 1
    for number in numbers:
        lcm *= number // gcd(lcm, number)
    return lcm

def get_num_steps_part_2(directions: str, nodes: Dict[str, Node], starting_nodes: Dict[str, Node]):
    cur_node_names = starting_nodes
    steps_for_each_starting_node: List[int] = []
    for node_name in cur_node_names:
        steps = get_num_steps_part_1(
            directions,
            nodes,
            node_name,
            lambda s: s[-1] == "Z"
        )
        steps_for_each_starting_node.append(steps)
    return lcm(steps_for_each_starting_node)

def print_answer_part_2():
    directions: str = ""
    nodes: Dict[str, Node] = dict()
    starting_nodes: Dict[str, Node] = dict()
    for i, line in enumerate(LINES):
        # pre-process line
        line = line.replace("\n", "")
        line = line.replace(" ", "")
        line = line.replace("(", "")
        line = line.replace(")", "")

        # special cases
        if i == 0:
            directions = line
            continue
        if i == 1:
            continue

        node_name, l_r_str = line.split("=")
        left_name, right_name = l_r_str.split(",")
        node = Node(node_name, left_name, right_name)
        nodes[node_name] = node
        if node_name[-1] == "A":
            starting_nodes[node_name] = node

    print("Dec 8 part 2: " + str(get_num_steps_part_2(directions, nodes, starting_nodes)))


if __name__ == "__main__":
    print_answer_part_1()
    print_answer_part_2()
