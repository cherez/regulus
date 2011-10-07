# -*- coding: iso-8859-1 -*-
class DFA(object):
    Nodes = []

    def __init__(self):
        self.nodes = [DFANode(0)] #empty start node
        self.nodes[0].final = True #match the empty string

    def minimize(self):
        #list of supernodes
        groups = [ [], [] ]

        #utility function for finding the group of a particular node
        #I have way too many inner functions in this project
        def group(id):
            for i, j in enumerate(groups):
                for node in j:
                    if node.id == id:
                        return i
            #oh crap, this suggests we're referencing a non-existant node
            assert False, "DFA references non-existantnode"

        #partition into final and not final
        for i in self.nodes:
            if not i.final:
                groups[0].append(i)
            else:
                groups[1].append(i)

        groups = [i for i in groups if i]


        #partition each supernode if their transitions don't have the same keys
        for i in groups:
            new = []
            for j in i:
                if j.transitions.keys() != i[0].transitions.keys():
                    new.append(j)
            #remove later to not freak out the iterations
            for j in new:
                i.remove(j)
            if new:
                groups.append(new)

        #now each group should have the same transition keys
        #partition groups so that all their members point to the same group for all transitions
        #since earlier groups might point to later ones that later split, we need to repeat until there's no change
        changed = True
        while changed:
            changed = False
            for i in groups:
                new = []
                for j in i:
                    for key in j.transitions:
                        if group(j.transitions[key]) != group(i[0].transitions[key]):
                            new.append(j)
                for j in new:
                    i.remove(j)
                if new:
                    changed = True
                    groups.append(new)

        #finally! Now we just turn our supernodes into regular nodes and call it a night

        #first, move the supernode with node 0 to the front, to keep our starting state
        start = groups[group(0)]
        groups.remove(start)
        groups.insert(0, start)

        self.nodes = []
        for i in groups:
            self.nodes.append(i[0])
            #we'll be referencing this a lot
            node = self.nodes[-1]
            node.id = len(self.nodes)-1
            for j in node.transitions:
                node.transitions[j] = group(node.transitions[j])

        #and we're done!

    def __repr__(self):
        return '\n'.join([repr(i) for i in self.nodes])

class DFANode(object):
    id = 0
    transitions = {} #{symbol : node }
    final = False

    def __init__(self, id):
        self.id = id
        self.transitions = {}
        self.final = False

    def __repr__(self):
        return 'id: ' + repr(self.id) + '\nTransitions:' + repr(self.transitions) + '\nFinal:' + repr(self.final)
