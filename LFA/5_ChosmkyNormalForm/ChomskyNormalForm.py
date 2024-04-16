class Grammar:
    def __init__(self, VN, VT, P, start):
        self.VN = VN
        self.VT = VT
        self.P = P
        self.start = start


class ChomskyForm:
    def __init__(self, VN, VT, P, start):
        self.VN = VN
        self.VT = VT
        self.P = P
        self.start = start

    def remove_duplicates(self, array):
        return list(set(array))

    def generate_strings_with_letter_removed(self, s, letter):
        strings = []
        for i in range(len(s)):
            if s[i] == letter:
                new_string = s[:i] + s[i + 1:]
                strings.append(new_string)
                strings.extend(self.generate_strings_with_letter_removed(new_string, letter))
        return list(set(strings))

    def removeEmptyString(self):
        list_symbol_empty = []
        for symbol in list(self.P.keys()):
            for transition in self.P[symbol]:
                if transition == "":
                    if symbol not in list_symbol_empty:
                        list_symbol_empty.append(symbol)
            self.P[symbol] = [trans for trans in self.P[symbol] if trans]

        for empty_symbol in list_symbol_empty:
            for symbol in list(self.P.keys()):
                new_transitions = []
                for transition in self.P[symbol]:
                    if empty_symbol in transition:
                        new_transitions.extend(self.generate_strings_with_letter_removed(transition, empty_symbol))
                self.P[symbol].extend(new_transitions)
                self.P[symbol] = self.remove_duplicates(self.P[symbol])
        print("After removing empty strings:", self.P)

    def removeInaccessible(self):
        reachable_symbols = [self.start]
        i = 0
        while i < len(reachable_symbols):
            current_symbol = reachable_symbols[i]
            for transition in self.P[current_symbol]:
                for char in transition:
                    if char in self.VN and char not in reachable_symbols:
                        reachable_symbols.append(char)
            i += 1

        self.P = {sym: self.P[sym] for sym in reachable_symbols if sym in self.P}
        self.VN = set(reachable_symbols)
        print("After removing inaccessible symbols:", self.P)

    def unitProduction(self):
        changes = True
        while changes:
            changes = False
            for symbol in list(self.P.keys()):
                for transition in self.P[symbol][:]:
                    if len(transition) == 1 and transition in self.VN:
                        self.P[symbol].remove(transition)
                        self.P[symbol].extend(self.P[transition])
                        changes = True
        self.P = {sym: self.remove_duplicates(self.P[sym]) for sym in self.P}
        print("After removing unit productions:", self.P)

    def chomsky(self):
        spec = "λ"
        k = 1
        new_nonterm = {}
        for symbol in self.P:
            for idx in range(0, len(self.P[symbol])):
                trns = self.P[symbol][idx]
                if len(trns) >= 2:
                    if len(trns) == 2:
                        cnt_nonterm = 0
                        for i in trns:
                            if i in VN:
                                cnt_nonterm += 1
                        if cnt_nonterm == 2:
                            continue

                    rest = self.P[symbol][idx][1:]
                    nonterm_found = ""
                    for i in new_nonterm:
                        if rest == new_nonterm[i]:
                            nonterm_found = i
                            break
                    if nonterm_found == "":
                        new_nonterm[spec + str(k)] = rest
                        nonterm_found = spec + str(k)
                        k += 1
                    self.P[symbol][idx] = self.P[symbol][idx].replace(rest, nonterm_found)

                    if self.P[symbol][idx][0] in VT:
                        term = self.P[symbol][idx][0]
                        nonterm_found = ""
                        for i in new_nonterm:
                            if term == new_nonterm[i]:
                                nonterm_found = i
                                break
                        if nonterm_found == "":
                            new_nonterm[spec + str(k)] = term
                            nonterm_found = spec + str(k)
                            k += 1
                        # print(new_nonterm)
                        self.P[symbol][idx] = self.P[symbol][idx].replace(term, nonterm_found)

        self.P.update(new_nonterm)

        print("After converting to Chomsky Normal Form:", self.P)

    def transformInChomsky(self):
        self.removeEmptyString()
        self.removeInaccessible()
        self.unitProduction()
        self.removeInaccessible()
        self.chomsky()


# Grammar definition
VN = {"S", "A", "B", "C", "E"}
VT = {"a", "b"}
start = "S"

P = {
    "S": ["bA", "B"],
    "A": ["a", "aS", "bAaAb"],
    "B": ["AC", "bS", "aAa"],
    "C": ["", "AB"], #Epsilon is presented as ' '
    "E": ["BA"]
}

grammar = Grammar(VN, VT, P, start)
print("Initial grammar: ", P)
chomsky = ChomskyForm(grammar.VN, grammar.VT, grammar.P, grammar.start)
chomsky.transformInChomsky()
