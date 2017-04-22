import re
import collections

# Token specification
NUM    = r'(?P<NUM>\d+)'
PLUS   = r'(?P<PLUS>\+)'
MINUS  = r'(?P<MINUS>-)'
TIMES  = r'(?P<TIMES>\*)'
DIVIDE = r'(?P<DIVIDE>/)'
LPAREN = r'(?P<LPAREN>\()'
RPAREN = r'(?P<RPAREN>\))'
WS     = r'(?P<WS>\s+)'

MASTER_PAT = re.compile('|'.join([NUM, PLUS, MINUS, TIMES,
                                  DIVIDE, LPAREN, RPAREN, WS]))

# Tokenizer
Token = collections.namedtuple('Token', ['type','value'])

def gen_tokens(text):
    scanner = MASTER_PAT.scanner(text)
    for m in iter(scanner.match, None):
        tok = Token(m.lastgroup, m.group())
        if tok.type != 'WS':
            yield tok

class ExpressionEvaluator:
    "Recursive descent parser"

    def parse(self, text):
        'Main func to process expressions and return values'
        self.tokens = gen_tokens(text) # Feeds tokens
        self.tok = None # Last token consumed
        self.next_tok = None # Next token
        self._advance() # Load first token
        return self.expr()

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
            op = self.tok.type
            right = self.term()
            if op == 'PLUS':
                exprval += right
            elif op == 'MINUS':
                exprval -= right

        return exprval

    def term(self):
        "term ::= factor { ('*'|'/') factor }*"

        termval = self.factor() # Grab left* factor

        while self._accept('TIMES') or self._accept('DIVIDE'): # Process repeating operations
            op = self.tok.type
            right = self.term()
            if op == 'TIMES':
                termval *= right
            elif op == 'DIVIDE':
                termval /= right

        return termval

    def factor(self):
        "factor ::= NUM | ( expr )"

        if self._accept('NUM'):
            return int(self.tok.value)
        elif self._accept('LPAREN'):
            exprval = self.expr() # Began at the "top"
            self._expect('RPAREN')
            return exprval
        else:
            raise SyntaxError('Expected NUMBER or PAREN')
