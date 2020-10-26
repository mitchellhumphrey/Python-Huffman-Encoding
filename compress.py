from collections import defaultdict
from bitarray import bitarray
from pathlib import Path
import sys


# sys1 is file to be compressed, sys2 is name of compressed file output

class Node:
    def __init__(self, character=None, node=None):
        # print(type(node))
        self.character = character
        self.left = None
        self.right = None
        if type(node) == 'Node':
            self.left = node.left
            self.right = node.right
            self.character = node.character


# pre:
# post:
# description:
def make_table(tree, table, prefix):
    if tree.character:
        # print("character is " + tree.character)
        table[tree.character] = prefix

    if not tree.left and not tree.right:
        return

    if not tree.left:
        # print("left is None")
        make_table(tree.right, table, prefix + '1')
        return
    if not tree.right:
        print("right is None")
        make_table(tree.left, table, prefix + '0')
        return
    make_table(tree.left, table, prefix + '0')
    make_table(tree.right, table, prefix + '1')


# pre:
# post:
# description: Don't need anymore
def print_tree(tree):
    if not tree.character:
        # print("hi im printing the character " + tree.character)
        pass
    if not tree.right:
        print_tree(tree.right)
    if not tree.left:
        print_tree(tree.left)


file = open(Path("./" + sys.argv[1]), 'r')
out = open(Path("./" + sys.argv[2] + ".p8a"), "wb+")

dictionary = defaultdict(lambda: 0)

# goes through the input file 
for line in file:
    for char in line:
        dictionary[char] += 1

list2 = []

for key, value in dictionary.items():
    # print("(", key, ',', value, ')')
    list2.append((value, Node(character=key)))

while len(list2) > 1:
    list2.sort(key=lambda x: x[0])
    # print(list)
    left = list2.pop(0)
    if len(list2) > 0:
        right = list2.pop(0)
    else:
        right = (0, Node())
    temp = Node()
    temp.right = right[1]
    temp.left = left[1]
    list2.append((left[0] + right[0], temp))

table = {}
tree = list2[0][1]
make_table(tree, table, '')

print(table)
max_length = 0
code_item_table = []
for key, item in table.items():
    if len(item) > max_length:
        max_length = len(item)
    code_item_table.append((item, key))
print(max_length)

out.write(max_length.to_bytes(1, 'big'))
code_item_table.sort(key=lambda x: len(x[0]))
print(code_item_table)

amount_of_lengths = [0 for x in range(max_length + 1)]
for x in code_item_table:
    amount_of_lengths[len(x[0])] += 1

print(amount_of_lengths)

for x in amount_of_lengths:
    out.write(x.to_bytes(1, 'big'))

bit_array = bitarray()

temp = code_item_table[0]
print(temp)
temp_array = bitarray()
print(temp_array.frombytes(ord(temp[1]).to_bytes(1, 'big')))
print(temp_array)
print("hi")

while len(code_item_table) > 0:
    temp = code_item_table.pop(0)
    temp_array = bitarray()
    temp_array.frombytes(ord(temp[1]).to_bytes(1, 'big'))
    bit_array += temp_array
    bit_array += temp[0]

# print(bit_array)
out.write(bit_array.tobytes())

file.seek(0)

char = None
bigstring = bitarray()
while True:
    char = file.read(1)
    if char == "":
        break
    bigstring += table[char]

amount_of_padding = (-len(bigstring)) % 8

out.write(amount_of_padding.to_bytes(1, 'big'))

out.write(bigstring.tobytes())
