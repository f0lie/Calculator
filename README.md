# Calculator
Recursive descent parser writen in Python. Most of the code is from Python Cookbook, I added some more operations. Currently implements power, minus, plus, multiple, divide, parenthesis, functions, and constants. Names are taken from Python's math module so anything implemented there is callable here.
# Usage
Import calculator and create ExpressionEvaluator. Then use parse(text) method to eval strings.
```python
>>> import calculator
>>> e = calculator.ExpressionEvaluator()
>>> e.parse("1+1")
2
>>> e.parse("2^3")
8
>>> e.parse("2**3")
8
>>> e.parse("9 * (1 + 3)")
36
>>> e.parse("pi")
3.141592653589793
>>> e.parse("sin(pi/2)")
1.0
>>> e.parse("sin(pi/2")
Traceback (most recent call last):
  File "<input>", line 1, in <module>
    e.parse("sin(pi/2")
  File "/home/user/proj/calculator/calculator.py", line 50, in parse
    val = self.expr()
  File "/home/user/proj/calculator/calculator.py", line 75, in expr
    exprval = self.term() # Grab left* term
  File "/home/user/proj/calculator/calculator.py", line 90, in term
    termval = self.factor() # Grab left* pow
  File "/home/user/proj/calculator/calculator.py", line 105, in factor
    powval = self.base()
  File "/home/user/proj/calculator/calculator.py", line 122, in base
    return self.name()
  File "/home/user/proj/calculator/calculator.py", line 138, in name
    self._expect('RPAREN')
  File "/home/user/proj/calculator/calculator.py", line 68, in _expect
    raise SyntaxError('Expected ' + tok_type)
  File "<string>", line None
SyntaxError: ExpectedRPAREN
>>> e.parse("lol")
Traceback (most recent call last):
  File "<input>", line 1, in <module>
    e.parse("lol")
  File "/home/user/proj/calculator/calculator.py", line 50, in parse
    val = self.expr()
  File "/home/user/proj/calculator/calculator.py", line 75, in expr
    exprval = self.term() # Grab left* term
  File "/home/user/proj/calculator/calculator.py", line 90, in term
    termval = self.factor() # Grab left* pow
  File "/home/user/proj/calculator/calculator.py", line 105, in factor
    powval = self.base()
  File "/home/user/proj/calculator/calculator.py", line 122, in base
    return self.name()
  File "/home/user/proj/calculator/calculator.py", line 132, in name
    name = getattr(math, self.tok.value)
AttributeError: module 'math' has no attribute 'lol'
>>> e.history
[Query(text='1+1', result=2), Query(text='2^3', result=8), Query(text='2**3', result=8), Query(text='9
 * (1 + 3)', result=36), Query(text='pi', result=3.141592653589793), Query(text='sin(pi/2)', result=1.
0)]

```