from tokenizer import Tokenizer, Token, TokenType

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens

    def parse(self):
        position = 0

        while position < len(self.tokens) - 1:
            tok = self.tokens[position]
            match tok.token_type:
                case TokenType.FOR:
                    position += 1

                    if self.tokens[position].token_type == TokenType.IDENTIFIER:
                        identifier = self.tokens[position].value
                        position += 1
                        if self.tokens[position].token_type == TokenType.FROM:
                            position += 1
                            identifier_value = int(self.tokens[position].value)
                            position += 1
                            if self.tokens[position].token_type == TokenType.TO:
                                position += 1
                                end = int(self.tokens[position].value)

                                for identifier_value in range(identifier_value + 1, end + 1):
                                    print(identifier_value)
            position += 1

    def parse_block(self, position, tokens):
        pass

    def parse_expression(self, position, tokens):
        pass

if __name__ == "__main__":
    tokenizer = Tokenizer(open('data/scripts/simple.sci').read())

    parser = Parser(tokenizer.tokenize())
    parser.parse()
