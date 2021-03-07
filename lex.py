import enum
import sys

# To contain the original text and type of token


class Token:
    def __init__(self, tokenText, tokenKind):
        # The token's actual text. Used for Identfiers, Strings, and numbers
        self.text = tokenText
        self.kind = tokenKind  # The Token type the token is classified as

    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            # All keyword enums must be 1XX
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        return None


# TokenType is our enum for all the types of tokens.
class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Keywords.
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    # Operators.
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211


class Lexer:
    def __init__(self, input):
        # Append a \n to the input to simplify lexing/parsing the last token/statement
        self.source = input + '\n'
        self.curChar = ''  # the current char in the string
        self.curPos = -1  # current position in the string
        self.nextChar()

    # Process the next character
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0'  # EOF
        else:
            self.curChar = self.source[self.curPos]

    # Return the lookahead character
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos+1]

    # Handle Invalid Token
    def abort(self, message):
        sys.exit("Lexing Error. " + message)

    # Skip whitespace (except newlines). \n = end of a statement
    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()

    # Skip Comments
    def skipComment(self):
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()

    # Return the next token
    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = None

        # Check the first char of the token to decide what it is.
        # Check if its a multi char token (eg. !=, <= >=)
        if self.curChar == "+":
            token = Token(self.curChar, TokenType.PLUS)  # Plus Token
        elif self.curChar == "-":
            token = Token(self.curChar, TokenType.MINUS)  # Minus Token
        elif self.curChar == "*":
            token = Token(self.curChar, TokenType.ASTERISK)  # Asterisk token
        elif self.curChar == "/":
            token = Token(self.curChar, TokenType.SLASH)  # Slash token
        elif self.curChar == '=':
            # Check Whether this token is = or ==
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)
        elif self.curChar == '>':
            # Check whether this token is > or >=
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)
        elif self.curChar == '<':
            # Check whether this token is < or <=
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LT)
        elif self.curChar == '!':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())
        elif self.curChar == '\"':
            # Get characters between quotations
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '\"':
                # Dont allow special chars in the string, ie. no escape chars, newlines, tabs or %
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Illegal character in string.")
                self.nextChar()

            tokText = self.source[startPos: self.curPos]
            token = Token(tokText, TokenType.STRING)
        elif self.curChar.isdigit():
            # Leading char is digit, to this must be a digit
            # Get all consecutive digits and decimal if there is one
            startPos = self.curPos

            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == '.':  # Decimal!
                self.nextChar()

                # Must have atleast one digit after decimal
                if not self.peek().isdigit():
                    # Error!
                    self.abort("Must have a number after decimal.")
                while self.peek().isdigit():
                    self.nextChar()
            # Get the substring
            tokText = self.source[startPos: self.curPos + 1]
            token = Token(tokText, TokenType.NUMBER)
        elif self.curChar.isalpha():
            # Leading char is a letter, so this must be an indentifier or a keyword.
            # Get all consecutive alpha mumeric chars
            startPos = self.curPos

            while self.peek().isalpha():
                self.nextChar()

            # Check if the token is in the list of keywords.
            tokText = self.source[startPos: self.curPos + 1]
            keyword = Token.checkIfKeyword(tokText)

            if keyword == None:  # Identifier
                token = Token(tokText, TokenType.IDENT)
            else:  # Keyword
                token = Token(tokText, keyword)
        elif self.curChar == "\n":
            token = Token(self.curChar, TokenType.NEWLINE)  # Newline token
        elif self.curChar == "\0":
            token = Token(self.curChar, TokenType.EOF)  # EOF Token
        else:
            # Unknown Token!
            self.abort("Unknown Token: " + self.curChar)
        self.nextChar()
        return token
