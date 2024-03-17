# Define token types including FLOAT to handle floating point numbers along with other mathematical and structural tokens
INTEGER, FLOAT, PLUS, MINUS, MULTIPLY, DIVIDE, LPAREN, RPAREN, EOF = (
    'INTEGER', 'FLOAT', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', '(', ')', 'EOF'
)

class Token:
    def __init__(self, type, value):
        # Token class constructor with type and value. Type is the category of the token, and value is its actual value in the input string.
        self.type = type
        self.value = value

    def __str__(self):
        # Returns a string representation of the token, useful for debugging and logging.
        return f'Token({self.type}, {repr(self.value)})'

    def __repr__(self):
        # Representation of the token object, calling the __str__ method for a friendly output.
        return self.__str__()

class Lexer:
    def __init__(self, text):
        # Lexer class constructor initializes with the text to tokenize, starting position, and current character.
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        # Handles lexical errors by printing an error message. Returns None to indicate an error has occurred.
        print(f'Error: Invalid character at position {self.pos}')
        return None

    def advance(self):
        # Advances the 'pos' pointer and updates 'current_char' with the new character at the new position.
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        # Skips over any whitespace characters in the input string.
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        # Parses a multi-digit integer or float from the input string and returns its token.
        result = ''
        dot_count = 0
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if dot_count == 1:  # Ensures only one decimal point is counted for float numbers
                    break
                dot_count += 1
                result += '.'
            else:
                result += self.current_char
            self.advance()
        return Token(FLOAT, float(result)) if dot_count else Token(INTEGER, int(result))

    def get_next_token(self):
        # Tokenizer function that breaks the input text into tokens, one at a time.
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit() or self.current_char == '.':
                return self.number()

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MULTIPLY, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIVIDE, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            return self.error()

        return Token(EOF, None)  # Returns an EOF token to signify the end of input

def main():
    # Main function to continuously prompt the user for input expressions to tokenize until "exit" is entered.
    while True:
        text = input('Enter your expression (or type "exit" to quit): ')
        if text == "exit":
            break
        lexer = Lexer(text)
        token = lexer.get_next_token()
        while token is not None and token.type != EOF:
            if token.type is None:  # Error detected, break the loop
                break
            print(token)
            token = lexer.get_next_token()

if __name__ == '__main__':
    main()
