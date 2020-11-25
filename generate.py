import argparse
from collections import defaultdict
import random
import argparse
import re


class PCFG:
    def __init__(self):
        self._rules = defaultdict(list)
        self._sums = defaultdict(float)

    def add_rule(self, lhs, rhs, weight):
        assert(isinstance(lhs, str))
        assert(isinstance(rhs, list))
        self._rules[lhs].append((rhs, weight))
        self._sums[lhs] += weight

    @classmethod
    def from_file(cls, filename):
        grammar = PCFG()
        with open(filename) as fh:
            for line in fh:
                line = line.split("#")[0].strip()
                if not line: continue
                w,l,r = line.split(None, 2)
                r = r.split()
                w = float(w)
                grammar.add_rule(l,r,w)
        return grammar

    def is_terminal(self, symbol): return symbol not in self._rules

    def gen(self, symbol):
        if self.is_terminal(symbol): return symbol
        else:
            expansion = self.random_expansion(symbol)
            return " ".join(self.gen(s) for s in expansion)

    def gen_with_tree(self, symbol):
        if self.is_terminal(symbol):
            return symbol
        else:
            expansion = self.random_expansion(symbol)
            tree = "(" + symbol
            for s in expansion:
                tree += " " + self.gen_with_tree(s)
            tree += ")"

            return tree

    def random_sent(self, sent_num, t):
        sentences = []
        for i in range(sent_num):
            if t:
                sentences.append(self.gen_with_tree("ROOT"))
            else:
                sentences.append(self.gen("ROOT"))
        return sentences

    def random_expansion(self, symbol):
        """
        Generates a random RHS for symbol, in proportion to the weights.
        """
        p = random.random() * self._sums[symbol]
        for r, w in self._rules[symbol]:
            p = p - w
            if p < 0:
                return r
        return r



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PCFG program')
    parser.add_argument('file')
    parser.add_argument('-n', default=1, type=int, help='The number of sentences to create')
    parser.add_argument('-t', action='store_true', help='Generating the sentence tree structure')
    args = parser.parse_args()

    pcfg = PCFG.from_file(args.file)

    # print all sentences line by line
    sentences = pcfg.random_sent(args.n, args.t)
    for sentence in sentences:
        print(sentence)
