import re
import collections

# Stolen from Python Cookbook 2.18 and 2.19
NAME = r'(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'
NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
TIMES = r'(?P<TIMES>\*)'
EQ = r'(?P<EQ>=)'
WS = r'(?P<WS>\s+)'

MASTER_PAT = re.compile('|'.join([NAME, NUM, PLUS, TIMES, EQ, WS]))

Token = collections.namedtuple('Token', ['type', 'value'])

def gen_tokens(text):
    "Generates tokens of a string"
    scanner = MASTER_PAT.scanner(text)
    for match in iter(scanner.match, None):
        tok = Token(match.lastgroup, match.group())
        if tok.type != 'WS':
            yield tok
