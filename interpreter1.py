# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis

INTEGER, PLUS, MINUS, SPACE, EOF = 'INTEGER', 'PLUS', 'MINUS', 'SPACE', 'EOF'

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
        return 'Token({type}: {value})'.format(type = self.type, value = repr(self.value))

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

    def error(self):
    	raise Exception('Error parsing input')

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        text = self.text

        # is self.pos index past the end of the self.text ?
        # if so, then return EOF token because there is no more
        # input left to convert into tokens
        if self.pos > len(text)-1:
            return Token(EOF, None)

        # get the char at current token and get the associated
        # token
        current_char = text[self.pos]

        # if the character is a digit then convert it to
        # integer, create an INTEGER token, increment self.pos
        # Similarly for others
        if current_char.isdigit():
            token = Token(INTEGER, current_char)
            self.pos += 1
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        if current_char == '-':
            token = Token(MINUS, current_char)
            self.pos += 1
            return token

        if current_char == ' ':
            token = Token(SPACE, current_char)
            self.pos += 1
            return token

        self.error()

    def check(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()

    def expr(self):
        """
        expr -> INTEGER PLUS INTEGER
        """
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()
        left = []
        right = []
        while(self.current_token.type == INTEGER):
            left.append(self.current_token)
            self.check(INTEGER)

        while(self.current_token.type == SPACE):
        	self.check(SPACE)

        operator = self.current_token
        self.check(PLUS) or self.check(MINUS)

        while(self.current_token.type == SPACE):
        	self.check(SPACE)

        while(self.current_token.type == INTEGER):
            right.append(self.current_token)
            self.check(INTEGER)

        leftstr = ''
        rightstr = ''
        for i in left:
        	leftstr += i.value
        
       	for i in right:
        	rightstr += i.value

        if operator.value == '+':
            result = int(leftstr) + int(rightstr)

        elif operator.value == '-':
        	result = int(leftstr) - int(rightstr)
        
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

			
