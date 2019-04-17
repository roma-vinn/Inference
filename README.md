# "Forward reasoning" project

File ```'main.py'``` consist class ```Formula```, which
represents corresponding mathematical object – Propositional
calculus formula. 

Initialization is strict. It's needed to:
- use spaces between each symbol of variable, logical connectivity
or scope;
- use only implication (```->```) and negation (```!```);
- remove all redundant parentheses, but external.

Example:
```python
from main import Formula

formula = Formula('( x1 -> ( ! x2 -> x1 ) )')
```

## Tautology checking

For now, you can just check whether your formula is tautology or not.
For this, there is a method ```is_tautology```.

Example:
```python
from main import Formula

formula_1 = Formula('( x1 -> ( ! x2 -> x1 ) )')
print(formula_1.is_tautology())  # True

formula_2 = Formula('( x1 -> x2 )')
print(formula_2.is_tautology())  # False
```
