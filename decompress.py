from bitarray import bitarray
import time
import sys


inputfile = open(sys.argv[1], "rb")
out = open(sys.argv[2], 'w+')

longest_code_length = int.from_bytes(inputfile.read(1), 'big')

# print(longest_code_length)
amount_for_each_length = [0 for x in range(longest_code_length + 1)]

for x in range(longest_code_length + 1):
    amount_for_each_length[x] = int.from_bytes(inputfile.read(1), 'big')

print(amount_for_each_length)
amount_of_bits = 0
index = 0
for x in amount_for_each_length:
    while x > 0:
        amount_of_bits += index
        amount_of_bits += 8
        x -= 1
    index += 1

while (amount_of_bits % 8) != 0:
    amount_of_bits += 1

amount_of_bytes = amount_of_bits // 8
filetable = inputfile.read(amount_of_bytes)
print(filetable)
bit_array_table = bitarray()
bit_array_table.frombytes(filetable)
table = {}
index = 0
key_list = []
item_list = []
for x in amount_for_each_length:
    while x > 0:
        char = chr(int.from_bytes(bit_array_table[:8].tobytes(), 'big'))
        bit_array_table = bit_array_table[8:]
        code = bit_array_table[:index]
        bit_array_table = bit_array_table[index:]
        # table[code] = char
        key_list.append(code)
        item_list.append(char)
        x -= 1
    index += 1

amount_of_padding = int.from_bytes(inputfile.read(1), 'big')
actual_text = inputfile.read()
bit_array_message = bitarray()
bit_array_message.frombytes(actual_text)
DECODED_TEXT = ""
DECODED_TEXT_ARRAY = []
index = 0
bit_array_compare = bitarray()



#for key, item in table.items():
#    key_list.append(key)
#    item_list.append(item)

start = time.time()

while len(bit_array_message) > amount_of_padding:
    index += 1
    bit_string = bit_array_message[:index]
    if bit_string in key_list:
        # DECODED_TEXT += table[bit_string]
        DECODED_TEXT += item_list[key_list.index(bit_string)]
        bit_array_message = bit_array_message[index:]
        index = 0

    if len(DECODED_TEXT) > 1000:
        DECODED_TEXT_ARRAY.append(DECODED_TEXT)
        DECODED_TEXT = ''
DECODED_TEXT_ARRAY.append(DECODED_TEXT)

print(time.time() - start)

for x in DECODED_TEXT_ARRAY:
    out.write(x)
