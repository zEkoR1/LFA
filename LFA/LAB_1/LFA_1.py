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
                terminal_leading_expansions = [rule for rule in self.rules[symbol] if
                                               all(sym in self.terminals for sym in rule)]
                if terminal_leading_expansions:
                    expansion = random.choice(terminal_leading_expansions)
                else:
                    expansion = random.choice(self.rules[symbol])
            else:
                expansion = random.choice(self.rules[symbol])
            return ''.join(self._generate_string_from_symbol(sym, depth + 1) for sym in expansion)
        return ''
    def generate_valid_strings(self, n=5):
        valid_strings = []
        for _ in range(n):
            valid_string = self._generate_string_from_symbol(self.start_symbol)
            valid_strings.append(valid_string)
        return valid_strings
terminals = ['a', 'b', 'c', 'd']
non_terminals = ['S', 'D', 'E', 'F', 'L']
rules = {
    'S': ['aD '],
    'D': ['bE'],
    'E': ['cF', 'dL'],
    'F': ['dD'],
    'L': ['aL', 'bL', 'c']
}
start_symbol = 'S'
grammar = Grammar(terminals, non_terminals, rules, start_symbol)
valid_strings = grammar.generate_valid_strings()
print(valid_strings)
