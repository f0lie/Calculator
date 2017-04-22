# Calculator
Recursive descent parser writen in Python. Most of the code is from Python Cookbook, I added some more operations. Currently implements power, minus, plus, multiple, divide, and parathesises.
# Usage
Import calculator and create ExpressionEvaluator. Then use parse(text) method to eval strings.
```python
>>> import calculator
>>> e = calculator.ExpressionEvaluator()
>>> e.parse("4 + 2**2")
8
>>> e.parse("2**2 * 2")
8
>>> e.parse("2**2 * 6")
24
>>> e.parse("2**6 * 6")
384
>>> e.parse("4+2**2")
8
>>> e.parse("(4+2)**2")
36
>>> exit()
```