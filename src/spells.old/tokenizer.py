class TokenType:
    EQUALS = "equal"
    COMMA = "comma"
    PLUS = "plus"
    MINUS = "minus"
    MULTIPLY = "multiply"
    DIVIDE = "divide"
    MODULO = "modulo"
    POWER = "power"
    IF = "ifKeyword"
    UNLESS = "unlessKeyword"
    OTHERWISE = "otherwiseKeyword"
    IS = "isKeyword"
    THEN = "thenKeyword"
    END = "endKeyword"
    IN = "inKeyword"
    DO = "doKeyword"
    FOR = "forKeyword"
    WHILE = "whileKeyword"
    NOT = "notKeyword"
    RETURN = "returnKeyword"
    BREAK = "breakKeyword"
    CONTINUE = "continueKeyword"
    AND = "andKeyword"
    OR = "orKeyword"
    LESS = "lessKeyword"
    GREATER = "greaterKeyword"
    TO = "toKeyword"
    FROM = "fromKeyword"
    AT = "atKeyword"
    PIPE = "pipe"
    OPENBRACKET = "openbracket"
    CLOSEBRACKET = "closebracket"
    TRUE = "trueKeyword"
    FALSE = "falseKeyword"
    STRINGLITERAL = "string literal"
    NUMBERLITERAL = "number literal"
    IDENTIFIER = "identifier"

keywords = {
    "if": TokenType.IF,
    "unless": TokenType.UNLESS,
    "otherwise": TokenType.OTHERWISE,
    "is": TokenType.IS,
    "then": TokenType.THEN,
    "end": TokenType.END,
    "in": TokenType.IN,
    "do": TokenType.DO,
    "for": TokenType.FOR,
    "while": TokenType.WHILE,
    "not": TokenType.NOT,
    "return": TokenType.RETURN,
    "break": TokenType.BREAK,
    "continue": TokenType.CONTINUE,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "to": TokenType.TO,
    "from": TokenType.FROM,
    "at": TokenType.AT,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
}

symbols = {
    "=": TokenType.EQUALS,
    ",": TokenType.COMMA,
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.MULTIPLY,
    "/": TokenType.DIVIDE,
    "%": TokenType.MODULO,
    "^": TokenType.POWER,
    "|": TokenType.PIPE,
    "(": TokenType.OPENBRACKET,
    ")": TokenType.CLOSEBRACKET,
    "<": TokenType.LESS,
    ">": TokenType.GREATER,
}

class Token:
    def __init__(self, t: str, v: str = ""):
        self.token_type = t
        self.value = v
    
    def __repr__(self):
        return "{ Type: " + self.token_type + ", Value: '" + self.value + "' }"

class Tokenizer:
    def __init__(self, stream: str):
        self.stream = stream + "\n"
        self.tokens: list[Token] = []
    
    def tokenize(self):
        position = 0
        while position < len(self.stream) - 1:
            char = self.stream[position]
            if char.isalpha():
                # identifiers and keywords
                identifier = char
                position += 1
                next_char = self.stream[position]
                while next_char not in [' ', '\t', '\n'] and position < len(self.stream) - 1:
                    identifier += next_char
                    position += 1
                    next_char = self.stream[position]
                
                if identifier in keywords:
                    self.tokens.append(Token(keywords[identifier]))
                else:
                    self.tokens.append(Token(TokenType.IDENTIFIER, identifier))
            elif char.isnumeric():
                # number literals
                number = char
                position += 1
                next_char = self.stream[position]
                while next_char not in [' ', '\t', '\n'] and position < len(self.stream) - 1:
                    number += next_char
                    position += 1
                    next_char = self.stream[position]
                
                if '.' in number:
                    try:
                        float(number)
                        self.tokens.append(Token(TokenType.NUMBERLITERAL, number))
                    except ValueError:
                        return []
                else:
                    try:
                        int(number)
                        self.tokens.append(Token(TokenType.NUMBERLITERAL, number))
                    except ValueError:
                        return []
            elif char == '"':
                # strings
                string = ""
                position += 1
                next_char = self.stream[position]
                while next_char != '"' and position < len(self.stream) - 1:
                    string += next_char
                    position += 1
                    next_char = self.stream[position]
                
                self.tokens.append(Token(TokenType.STRINGLITERAL, string))
            else:
                if char in symbols:
                    self.tokens.append(Token(symbols[char]))
                elif char not in [' ', '\t', '\n']:
                    return []

            position += 1

        return self.tokens