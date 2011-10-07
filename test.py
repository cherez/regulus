#!/bin/env python
# -*- coding: iso-8859-1 -*-
def test_regular_expression():
    from regular_expression import make_re
    from run import run

    def test(pattern, accept, reject):
        re = make_re(pattern)
        for i in accept:
            if not run(re, i):
                print "Error: '%s' rejected '%s'" % (pattern, i)
        for i in reject:
            if run(re, i):
                print "Error: '%s' accepted '%s'" % (pattern, i)

    test('a', ['a'], ['', 'aa', 'b'])

    test('a*', ['', 'a', 'aaa'], ['ab', 'b'])

    test('aa', ['aa'], ['ab', 'b', '', 'a'])

    test('a|b', ['a', 'b'], ['ab', '|', '', 'a|b'])

    test('(a|b)*', ['a', 'b', '', 'abaab'], ['c', 'bc'])

    test('[ab]', ['a', 'b'], ['c', 'ab'])

    test('[0-9]', ['0', '9', '5'], ['c', 'ab', ''])

    test('[^ab]', ['\0', '9', '5', 'A'], ['', 'a', 'b', '00'])

    test('\\"', ['"'], ['', 'a', 'b', '00'])

    test('\\\\', ['\\'], ['\'', 'c', '"'])

    test('[^\\\\"]*', ['a', '\'', 'c'], ['\\', '"'])

if __name__ == '__main__':
    test_regular_expression()

