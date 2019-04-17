"""
Created by Roman Polishchenko at 2019-04-17
2 course, comp math
Taras Shevchenko National University of Kyiv
email: roma.vinn@gmail.com
"""
from itertools import product


class BinaryTree:
    """
    A recursive implementation of Binary Tree.

    """
    def __init__(self, root_obj):
        self.key = root_obj
        self.left_child = None
        self.right_child = None

    def insert_left(self, new_node):

        if isinstance(new_node, BinaryTree):
            t = new_node
        else:
            t = BinaryTree(new_node)

        if self.left_child is not None:
            t.left = self.left_child

        self.left_child = t

    def insert_right(self, new_node):
        if isinstance(new_node, BinaryTree):
            t = new_node
        else:
            t = BinaryTree(new_node)

        if self.right_child is not None:
            t.right = self.right_child
        self.right_child = t

    def get_right_child(self):
        return self.right_child

    def get_left_child(self):
        return self.left_child

    def set_root_val(self, obj):
        self.key = obj

    def get_root_val(self,):
        return self.key


class Stack:
    """
    Simple stack implementation.

    """
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()


class Operations:
    """
    Class that implements logical operations
    """
    @staticmethod
    def xor(_a: bool, _b: bool) -> bool:
        """
        Logical XOR
        """
        if _a == _b:
            return False
        else:
            return True

    @staticmethod
    def implication(_a, _b) -> bool:
        """
        Logical implication.
        """
        if _a == 1 and _b == 0:
            return False
        else:
            return True


class Formula:
    """
    Class that implements Formula type

    """
    def __init__(self, f: str):
        self.formula = f
        self.variables = self.get_variables()
        self.parse_tree = self.build_parse_tree()

    def get_variables(self) -> dict:
        """
        Parse formula and find all variables symbols with assumption that
        all variables looks like 'xn'
        :return: list
        """
        tmp = self.formula.split()
        var = {}
        for t in tmp:
            if t not in ['!', '->', '(', ')']:
                var[t] = False
        return var

    def set_values(self, values):
        """
        Update mentioned logical values.
        :param values:  dict {'symbol': True/False, ...}
                        list [True, False, ...], where x1 = True, x2 = False, ...
        :return: None
        """
        if type(values) == list and all([type(i) == bool for i in values]) and len(values) == len(self.variables):
            keys = list(self.variables.keys())
            # sort keys in order
            keys.sort(key=lambda x: int(x[1:]))
            values = {keys[i]: values[i] for i in range(len(keys))}
        self.variables.update(values)

    def build_parse_tree(self) -> BinaryTree:

        def remove_denial(_tokens: list):
            for index, token in enumerate(_tokens):
                if token == '!':
                    _tokens[index] = '('
                    _tokens.insert(index + 1, '1')
                    _tokens.insert(index + 2, "+")
                    _tokens.insert(index + 4, ')')

        tokens = self.formula.split()
        remove_denial(tokens)
        stack = Stack()
        tree = BinaryTree('')
        stack.push(tree)
        current_tree = tree
        for i in tokens:
            if i == '(':
                current_tree.insert_left('')
                stack.push(current_tree)
                current_tree = current_tree.get_left_child()
            elif i not in ['+', '->', '!', ')']:
                if i == '1':
                    current_tree.set_root_val(True)
                else:
                    current_tree.set_root_val(i)
                parent = stack.pop()
                current_tree = parent
            elif i in ['+', '->', '!']:
                current_tree.set_root_val(i)
                current_tree.insert_right('')
                stack.push(current_tree)
                current_tree = current_tree.get_right_child()
            elif i == ')':
                current_tree = stack.pop()
            else:
                raise ValueError
        return tree

    def _evaluate(self, parse_tree):
        actions = {'+': Operations.xor, "->": Operations.implication}

        left_child = parse_tree.get_left_child()
        right_child = parse_tree.get_right_child()

        if left_child and right_child:
            fn = actions[parse_tree.get_root_val()]
            return fn(self._evaluate(left_child), self._evaluate(right_child))
        else:
            root_val = parse_tree.get_root_val()
            if type(root_val) == bool:
                return root_val
            else:
                return self.variables[root_val]

    def evaluate(self):
        pt = self.parse_tree
        return self._evaluate(pt)

    def is_tautology(self):
        k = len(self.variables)
        for values in product([True, False], repeat=k):
            self.set_values(list(values))
            if not self.evaluate():
                return False
        return True


if __name__ == '__main__':
    formula = Formula("( x2 -> ( ! x1 -> x2 ) )")
    print(formula.is_tautology())
    formula = Formula("( x1 -> x2 )")
    print(formula.is_tautology())
