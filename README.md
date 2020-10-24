# Python-Huffman-Encoding

## compress.py

How to use:

python compress.py "name of input file(including extension)" "name of output file(excluding extension)"

##decompress.py

How to use:

python decompress.py "name of input file(including extension)" "name of output file(including extension)"


##P8A file spec

file is in Big Endian

first byte, longest code length

next byte, amount of items at code length 1

next byte, amount of items at code length 2

repeat until all values from 1 to first byte inclusive are stored

add zeros till first part to hear is full bytes

character, then code, looped from smallest to largest

amount of filler bits at end of compressed message

compressed message