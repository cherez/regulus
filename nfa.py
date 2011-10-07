# -*- coding: iso-8859-1 -*-
import dfa

class NFA(object):
    nodes = []

    def __init__(self):
        self.nodes = [NFANode(0)] #empty start node
        self.nodes[0].final = True #match the empty string

    #Basic NFA operations
    #These seem like they could be refactored. Hard.

    def concat(self, other):
        #match a string that matches the current NFA, THEN the other
        #so append the two NFAs, and make any final from the first transition into the start of the second
        offset = len(self.nodes)
        for node in self.nodes:
            if node.final:
                if '' in node.transitions:
                    node.transitions[''] += [offset]
                else:
                    node.transitions[''] = [offset]
            node.final = False

        for node in other.nodes:
            self.nodes.append(NFANode(node.id + offset))
            for symbol in node.transitions:
                self.nodes[-1].transitions[symbol] = [i + offset for i in node.transitions[symbol] ]
            self.nodes[-1].final = node.final


        return offset

    def star(self):
        #match a string that contains the current NFA 0 or more times
        #so, make a default node that is final and make it the new start
        #any old final nodes transition to the new one
        for i in self.nodes:
            i.id += 1
            for j in i.transitions:
                i.transitions[j] = [k+1 for k in i.transitions[j] ]

        self.nodes.insert(0, NFANode(0))

        for i in self.nodes:
            if i.final:
                if '' in i.transitions:
                    i.transitions[''] += [0]
                else:
                    i.transitions[''] = [0]

        self.nodes[0].final = True
        self.nodes[0].transitions[''] = [1]

    def cross(self):
        #match a string that contains the current NFA 1 or more times
        #so, this is just like star, but the starting node is not final
        self.star()
        self.nodes[0].final = False

    def opt(self):
        #match a string that matches the current NFA, or the empty string
        #so just add a starting node that is final
        for i in self.nodes:
            i.id += 1
            for j in i.transitions:
                i.transitions[j] = [k+1 for k in i.transitions[j] ]

        self.nodes.insert(0, NFANode(0))
        self.nodes[0].final = True
        self.nodes[0].transitions[''] = [1]

    def union(self, other):
        #match a string that matches either NFA
        #make a starting node that transitions into either NFA
        for node in self.nodes:
            node.id += 1
            for symbol in node.transitions:
                node.transitions[symbol] = [i + i for i in node.transitions[symbol] ]

        self.nodes.insert(0, NFANode(0))

        offset = len(self.nodes)

        for node in other.nodes:
            self.nodes.append(NFANode(node.id + offset))
            for symbol in node.transitions:
                self.nodes[-1].transitions[symbol] = [i + offset for i in node.transitions[symbol] ]
            self.nodes[-1].final = node.final

            self.nodes[0].transitions[''] = [1, offset]

    def __repr__(self):
        return '\n'.join([repr(i) for i in self.nodes])


    def to_dfa(self):
        #creates a DFA from the NFA
        #each node in the result acts as the NFA in a set of nodes
        other = dfa.DFA()
        mapping = {}    #maps a set of symbols in self to a single state is the DFA
                                    #{(nodes): node}
        open_nodes = [] #list of nodes that have yet to be processed

        first = [0]
        for i in first:
            if '' in self.nodes[i].transitions:
                for j in self.nodes[i].transitions['']:
                    if j not in first:
                        first.append(j)

        mapping[frozenset(first)] = 0
        open_nodes.append(frozenset(first))

        while open_nodes:
            current = open_nodes.pop()
            nodes = [self.nodes[i] for i in current]
            index = mapping[current]

            #find the nodes to which this maps
            transitions = set()
            for i in nodes:
                for j in i.transitions:
                    if j:
                        transitions.add(j)
            #set all the node's transitions
            for i in transitions:
                next = []
                #find all the natural transitions
                for j in nodes:
                    if i in j.transitions:
                        next.extend(j.transitions[i])
                #then all the empty transitions
                for j in next:
                    if '' in self.nodes[j].transitions:
                        for k in self.nodes[j].transitions['']:
                            if k not in next:
                                next.append(k)

                key = frozenset(next)
                #if we have no previous node representing this set, make one
                if key not in mapping:
                    mapping[key] = len(other.nodes)
                    open_nodes.append(key)
                    other.nodes.append(dfa.DFANode(len(other.nodes)))
                other.nodes[index].transitions[i] = mapping[key]

            other.nodes[index].final = False
            for i in nodes:
                if i.final:
                    other.nodes[index].final = i.final
                    break

        return other

class NFANode(object):
    id = 0
    transitions = {} #{symbol : [nodes] }
    final = False

    def __init__(self, id):
        self.id = id
        self.transitions = {}
        self.final = False

    def __repr__(self):
        return 'id: ' + repr(self.id) + '\nTransitions:' + repr(self.transitions) + '\nFinal:' + repr(self.final)

def match_symbols(chars):
    n = NFA()
    n.nodes[0].final = False #Do not match the empty string
    for c in chars:
        n.nodes[0].transitions[c] = [1]
    n.nodes.append(NFANode(1))
    n.nodes[1].final = True
    return n
