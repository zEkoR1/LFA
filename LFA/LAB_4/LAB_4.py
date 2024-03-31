import random
def createPatternString(pattern):
    pattern_string = ""
    i = 0
    while i < len(pattern):
        # Handle single occurrence from choices
        if (pattern[i] == "(" and pattern.index(")", i) == len(pattern) - 1) or (
                pattern[i] == "(" and pattern[pattern.index(")", i) + 1] not in ["*", "+", "?", "{"]):
            option = select(randomChoice(pattern[i + 1:pattern.index(")", i)]))
            pattern_string += option
            i = pattern.index(")", i)
            print(f"Single occurrence from choices: Appended {option} => {pattern_string}")
        # Handle one or more occurrences from choices
        elif pattern[i] == "(" and pattern[pattern.index(")", i) + 1] == "+":
            repetitions = random.randint(1, 5)
            for _ in range(repetitions):
                option = select(randomChoice(pattern[i + 1:pattern.index(")", i)]))
                pattern_string += option
                print(f"One or more from choices: Appended {option} => {pattern_string}")
            i = pattern.index(")", i) + 1
        # Handle zero or more occurrences from choices
        elif pattern[i] == "(" and pattern[pattern.index(")", i) + 1] == "*":
            for _ in range(random.randint(0, 5)):
                option = select(randomChoice(pattern[i + 1:pattern.index(")", i)]))
                pattern_string += option
                print(f"Zero or more from choices: Appended {option} => {pattern_string}")
            i = pattern.index(")", i) + 1
        # Handle fixed occurrences from choices
        elif pattern[i] == "(" and pattern[pattern.index(")", i) + 1] == "{":
            for _ in range(int(pattern[pattern.index("{", i) + 1])):
                option = select(randomChoice(pattern[i + 1:pattern.index(")", i)]))
                pattern_string += option
                print(f"Fixed occurrences from choices: Appended {option} => {pattern_string}")
            i = pattern.index("}", i) + 1
        # Handle zero or one occurrence from choices
        elif pattern[i] == "(" and pattern[pattern.index(")", i) + 1] == "?":
            if random.randint(0, 1):
                option = select(randomChoice(pattern[i + 1:pattern.index(")", i)]))
                pattern_string += option
                print(f"Zero or one from choices: Appended {option} => {pattern_string}")
            i = pattern.index(")", i) + 1
        elif i < len(pattern) - 2 and pattern[i + 1] == "?":
            if random.randint(0, 1):
                pattern_string += pattern[i]
                print(f"Zero or one occurrence: Appended {pattern[i]} => {pattern_string}")
            i += 2
        elif pattern[i] in '(){|+*?}' + '^':
            i += 1
            continue
        else:
            pattern_string += pattern[i]
            print(f"Direct addition: Appended {pattern[i]} => {pattern_string}")
            i += 1
    return pattern_string

def select(option):
    return random.choice(option)
def randomChoice(sequence):
    return sequence.split("|")

# Here are given the rules
rule_1 = "(a|b)(c|d)(E)+(G)?"
print('Resulting string for rule 1: ', createPatternString(rule_1))
print('-' * 70)
rule_2 = "P(Q|R|S)T(UV|W|X)*(Z)+"
print('Resulting string for rule 2: ', createPatternString(rule_2))
print('-' * 70)
rule_3 = "1(0|1)*2(3|4){" + "5}" + "36"
print('Resulting string for rule 3: ', createPatternString(rule_3))
