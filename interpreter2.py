#!/usr/bin/python
# -*- coding: utf-8 -*-
# Token types
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis

(INTEGER, PLUS, MINUS, MULTIPLY, DIVIDE, EOF) = ('INTEGER', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'EOF')


class Token(object):

    def __init__(self, type, value):

        # type: INTEGER, PLUS, or EOF
        self.type = type
        # value: 1...9
        self.value = value

    def __str__(self):
        """String representation of the class instance.
        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}: {value})'.format(type=self.type,
                value=repr(self.value))

    def __repr__(self):
        return self.__str__()


class Interpreter(object):

    def __init__(self, text):

        # client string input, e.g. "3+5"

        self.text = text

        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def go_ahead(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.go_ahead()

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.go_ahead()

        return int(result)

    def check(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """

        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.go_ahead()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.go_ahead()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.go_ahead()
                return Token(MULTIPLY, '*')

            if self.current_char == '/':
                self.go_ahead()
                return Token(DIVIDE, '/')

            self.error()

        return Token(EOF, None)

    def expr(self):
        """
        expr -> INTEGER PLUS INTEGER
        """
        # set current token to the first token taken from the input

        self.current_token = self.get_next_token()
        result = self.current_token.value

        left = Token(INTEGER, result)
        self.check(INTEGER)

        while self.current_token is not None and self.current_token.type != EOF:
            left = Token(INTEGER, result)

            operator = self.current_token
            if operator.type == PLUS:
                self.check(PLUS)
            elif operator.type == MINUS:
                self.check(MINUS)
            elif operator.type == MULTIPLY:
                self.check(MULTIPLY)
            elif operator.type == DIVIDE:
                self.check(DIVIDE)

            right = self.current_token
            self.check(INTEGER)

            if operator.type == PLUS:
                result = left.value + right.value
            elif operator.type == MINUS:
                result = left.value - right.value
            elif operator.type == MULTIPLY:
                result = left.value * right.value
            elif operator.type == DIVIDE:
                result = float(left.value / right.value)

        return result


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break

        if not text:
            continue

        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
