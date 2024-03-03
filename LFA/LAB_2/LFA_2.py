states = ['q0', 'q1', 'q2', 'q3']
alphabet = ['a', 'b']
final_states = ['q3']
transitions = {
    ('q0', 'a'): ['q1'],
    ('q1', 'b'): ['q2'],
    ('q2', 'b'): ['q3', 'q2'],
    ('q3', 'a'): ['q1'],
    ('q1', 'a'): ['q1'],
}

def is_deterministic(transitions):
    for dests in transitions.values():
        if len(dests) > 1:
            return False
    return True

def fa_to_regular_grammar(states, transitions, final_states):
    grammar = {}
    for state in states:
        grammar[state] = []
        for (src, symbol), dests in transitions.items():
            if src == state:
                for dest in dests:
                    grammar[state].append((symbol, dest))
        if state in final_states:
            grammar[state].append(('', 'ε'))
    return grammar

def ndfa_to_dfa(states, alphabet, transitions, final_states):
    new_states = [set(['q0'])]  # Start with the initial state
    dfa_transitions = {}
    dfa_states = []
    dfa_final_states = []

    while len(new_states) > 0:
        current = new_states.pop(0)
        current_name = ''.join(sorted(current))
        if current_name not in dfa_states:
            dfa_states.append(current_name)
            if current & set(final_states):
                dfa_final_states.append(current_name)
            for symbol in alphabet:
                next_state = set()
                for state in current:
                    if (state, symbol) in transitions:
                        next_state.update(transitions[(state, symbol)])
                next_state_name = ''.join(sorted(next_state))
                dfa_transitions[(current_name, symbol)] = next_state_name
                if next_state not in new_states and next_state_name not in dfa_states:
                    new_states.append(next_state)
    return dfa_states, dfa_transitions, dfa_final_states

is_dfa = is_deterministic(transitions)
regular_grammar = fa_to_regular_grammar(states, transitions, final_states)
dfa_states, dfa_transitions, dfa_final_states = ndfa_to_dfa(states, alphabet, transitions, final_states)

(is_dfa, regular_grammar, (dfa_states, dfa_transitions, dfa_final_states))
print(f"Is the FA deterministic? {'Yes' if is_dfa else 'No'}")

print("\nConverted Regular Grammar:")
for state, productions in regular_grammar.items():
    for production in productions:
        print(f"{state} -> {production[0]}{production[1]}")

print("\nConverted DFA:")
print("States:", dfa_states)
print("Final States:", dfa_final_states)
print("Transitions:")
for (state, symbol), dest in dfa_transitions.items():
    print(f"δ({state}, {symbol}) = {dest}")