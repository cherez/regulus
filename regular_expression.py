# -*- coding: iso-8859-1 -*-

import cStringIO

from nfa import NFA, match_symbols
class RegularExpression(NFA):
    def __init__(self):
        NFA.__init__(self)

def make_re(stream, sub = False):
    if isinstance(stream, str):
        stream = cStringIO.StringIO(stream)
    re = RegularExpression()
    next = []

    #some utility functions
    #These are relatively complex actions that get invoked below.
    def read_character():
        character = stream.read(1)
        if character == '\\':
            character += stream.read(1)
            if character == '\\n':
                return '\n'
            if character == '\\r':
                return '\r'
            if character == '\\t':
                return '\t'
        return character

    def peek():
        start = stream.tell() #We need this because at EOF read(1) will not move forward.
        character = stream.read(1)
        stream.seek(start)
        return character

    def merge():
        #combine all the current ors, then
        while len(next) > 1:
            next[0].union(next[1])
            del next[1]

        if len(next) == 1:
            re.concat(next[0])
            del next[0] #can't do next = [] because of name binding issues

    #read the contents of a bracket expression
    #I feel awful having this long of a subfunction, but this would be even worse inlined.
    def read_bracket():
        characters = []
        inverse = False
        last = read_character()
        if last == '^':
            inverse = True
            last = read_character()

        next = read_character()
        while next:
            if next == '-':
                end = read_character()
                for i in xrange(ord(last[-1]), ord(end[-1])+1 ): #last[-1] to deal with \ escapes
                    characters.append(chr(i))
                last = read_character()
                if last == ']':
                    break
                next = read_character()
            else:
                characters.append(last[-1])
                if next == ']':
                    break
                last = next
                next = read_character()

        if not next:
            #if we get down here, then we hit eof without a ]
            raise ValueError('Unterminated bracket expression in regular expression.')

        if not inverse:
            return characters
        else:
            characters = [chr(i) for i in xrange(0, 256) if chr(i) not in characters]
            return characters


    while peek():
        c = read_character()
        if c == '(':
            next.append(make_re(stream, True))
        elif c == ')':
            if sub:
                merge()
                return re
            else:
                raise ValueError('Unbalanced parentheses in regular expression.')
        elif c == '[':
            next.append(match_symbols(read_bracket()))
        else:
            next.append(match_symbols(c[-1])) #c[-1] to deal with \ escapes

        if peek() == '*':
            read_character()
            next[-1].star()

        if peek() == '+':
            read_character()
            next[-1].cross()

        if peek() == '?':
            read_character()
            next[-1].opt()

        if peek() == '|':
            #this is an or, so go
            read_character()
            continue

        merge()
    if sub:
        raise ValueError('Unbalanced parentheses in regular expression.')
    return re
