# tokens = "+- */ >>= = != # This is a comment!\n \"This is a string\" IF+-123 9.8654 foo*THEN/"

import sys
import os

from lex import *
from parse import *
from emit import *


def main():
    if(len(sys.argv) != 2):
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as inputFile:
        input = inputFile.read()

    # Init lexer, parser and emitter.
    lexer = Lexer(input)
    emitter = Emitter("out.c")
    parser = Parser(lexer, emitter)

    parser.program()  # Start the parser
    emitter.writeFile()  # Write c output to file

    print("Compiling Completed!")

    baseName = os.path.basename(sys.argv[1])
    print(f"run: ./build/{os.path.splitext(baseName)[0]}.exe")


main()
