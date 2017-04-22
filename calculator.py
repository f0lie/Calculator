'Doing stuff with parsing expressions. Takes mainly from Python Cookbook'

import re
import collections
import math

# Token specification
NUM    = r'(?P<NUM>\d+)'
PLUS   = r'(?P<PLUS>\+)'
MINUS  = r'(?P<MINUS>-)'
TIMES  = r'(?P<TIMES>\*)'
DIVIDE = r'(?P<DIVIDE>/)'
LPAREN = r'(?P<LPAREN>\()'
RPAREN = r'(?P<RPAREN>\))'
WS     = r'(?P<WS>\s+)'
FACT   = r'(?P<FACT>!)'
POW    = r'(?P<POW>\*\*|\^)'

MASTER_PAT = re.compile('|'.join([NUM, PLUS, MINUS, POW, TIMES,
                                  DIVIDE, LPAREN, RPAREN, WS, FACT]))

# Tokenizer
Token = collections.namedtuple('Token', ['type', 'value'])

# Query
Query = collections.namedtuple('Query', 'text result')

def gen_tokens(text):
    'Yields tokens within given string'
    scanner = MASTER_PAT.scanner(text)
    for match in iter(scanner.match, None):
        tok = Token(match.lastgroup, match.group())
        if tok.type != 'WS':
            yield tok

class ExpressionEvaluator:
    'Recursive descent parser'

    def __init__(self):
        self.history = []

    def parse(self, text):
        'Main func to process expressions and return values'
        self.tokens = gen_tokens(text) # Feeds tokens
        self.tok = None # Last token consumed
        self.next_tok = None # Next token
        self._advance() # Load first token
        val = self.expr()
        self.history.append(Query(text, val))
        return val

    def _advance(self):
        'Advance one token ahead'
        self.tok, self.next_tok = self.next_tok, next(self.tokens, None)

    def _accept(self, tok_type):
        'Test and consume the token if accepted'
        if self.next_tok and self.next_tok.type == tok_type:
            self._advance()
            return True
        return False

    def _expect(self, tok_type):
        'Consume token and raise SyntaxError if tok_type does not match'
        if not self._accept(tok_type):
            raise SyntaxError('Expected' + tok_type)

    # Grammar Rules

    def expr(self):
        "expr ::= term { ('+'|'-') term }* "

        exprval = self.term() # Grab left* term

        while self._accept('PLUS') or self._accept('MINUS'): # Process repeating operations
            oper = self.tok.type
            right = self.term()
            if oper == 'PLUS':
                exprval += right
            elif oper == 'MINUS':
                exprval -= right

        return exprval

    def term(self):
        "term ::= pow { ('*'|'/') pow }*"

        termval = self.pow() # Grab left* pow

        while self._accept('TIMES') or self._accept('DIVIDE'): # Process repeating operations
            oper = self.tok.type
            right = self.pow()
            if oper == 'TIMES':
                termval *= right
            elif oper == 'DIVIDE':
                termval /= right

        return termval

    def pow(self):
        "pow ::= factor '**' factor"

        powval = self.factor()

        while self._accept('POW'):
            right = self.factor()
            powval = int(math.pow(powval, right))

        return powval

    def factor(self):
        "factor ::= NUM | ( expr )"

        if self._accept('FACT'):
            factval = self.factor()
            return math.factorial(factval)
        elif self._accept('NUM'):
            return int(self.tok.value)
        elif self._accept('LPAREN'):
            exprval = self.expr() # Began at the "top"
            self._expect('RPAREN')
            return exprval
        else:
            raise SyntaxError('Expected NUMBER or PAREN. Received: ' + repr(self.tok))
