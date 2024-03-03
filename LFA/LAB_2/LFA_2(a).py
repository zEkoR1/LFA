import random

class Grammar:
    def __init__(self, terminals, non_terminals, rules, start_symbol):
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.rules = rules
        self.start_symbol = start_symbol

    def _generate_string_from_symbol(self, symbol, depth=0):
        if symbol in self.terminals:
            return symbol
        elif symbol in self.non_terminals:
            if depth > 10:
                return ''
            expansion = random.choice(self.rules[symbol])
            return ''.join(self._generate_string_from_symbol(sym, depth + 1) for sym in expansion)
        return ''

    def generate_valid_strings(self, n=5):
        valid_strings = []
        for _ in range(n):
            valid_string = self._generate_string_from_symbol(self.start_symbol)
            valid_strings.append(valid_string)
        return valid_strings

    def classify_grammar(self):
        is_regular = True

        for lhs, rhs_list in self.rules.items():
            for rhs in rhs_list:

                if not ((len(rhs) == 1 and rhs in self.terminals) or
                        (len(rhs) == 2 and rhs[0] in self.terminals and rhs[1] in self.non_terminals) or
                        (len(rhs) == 2 and rhs[1] in self.terminals and rhs[0] in self.non_terminals)):
                    is_regular = False  # This rule does not fit Type 3 grammar

        if is_regular:
            return "Type 3 (Regular)"
        else:
            return "Type 2 (Context-Free)"


terminals = ['a', 'b', 'c', 'd']
non_terminals = ['S', 'D', 'E', 'F', 'L']
rules = {
    'S': ['aD'],
    'D': ['bE'],
    'E': ['cF', 'dL'],
    'F': ['dD'],
    'L': ['aL', 'bL', 'c']
}
start_symbol = 'S'

grammar = Grammar(terminals, non_terminals, rules, start_symbol)
valid_strings = grammar.generate_valid_strings()
print(valid_strings)

classification = grammar.classify_grammar()
print(f"Grammar Classification: {classification}")
