# -*- coding: iso-8859-1 -*-

import nfa
import dfa

def run(automata, string):
    #this just runs DFAs, because they're simpler
    if isinstance(automata, nfa.NFA):
        d = automata.to_dfa()
    elif isinstance(automata, dfa.DFA):
        d = automata
    else:
        raise ValueError('run() only accepts NFAs or DFAs.')

    state = 0
    for char in string:
        if char not in d.nodes[state].transitions:
            return False
        else:
            state = d.nodes[state].transitions[char]

    return d.nodes[state].final
