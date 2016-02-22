#!/usr/bin/env python2
from Crypto.Random import random
import argparse
import sys
import math
from collections import Counter
def range_type(min, max):
    def res(x):
        x = int(x);
        if not (min <= x <= max):
            raise argparse.ArgumentTypeError('{} is not in range [{}; {}]'.format(x, min, max))
        return x
    return res

def positive(x):
    x = int(x)
    if x < 0:
        raise argparse.ArgumentTypeError('{} is negative!'.format(x))
    return x

def generate(words, count):
    return ''.join(random.choice(words) for i in xrange(count))

def num_passwords(words, count, max_length):
    # complexity: O(count * max_word_len * max_length)
    start = {0:1.0} # to force more efficient float computations
    word_lens = Counter(map(len, words))
    for i in xrange(count):
        new = {}
        for p in start:
            for l in word_lens:
                x = p + l
                if x > max_length:
                    break
                if x not in new:
                    new[x] = 0
                new[x] += start[p] * word_lens[l]
        start = new
    return sum(start.values())

def main():
    parser = argparse.ArgumentParser(description='Creates password using most common US English words')
    parser.add_argument('-w', '--words', default=4, type=range_type(1, 16))
    parser.add_argument('-n', '--list_size', default=1000, type=range_type(10, 10**4))
    parser.add_argument('-L', '--max_length', type=range_type(1, 1000))
    parser.add_argument('-l', '--min_length', default=0, type=range_type(0, 10000))
    parser.add_argument('-a', '--max_attempts', default=1000, type=positive)
    parser.add_argument('-q', '--quote', action='store_true')
    parser.add_argument('-e', '--entropy', action='store_true')
    args = parser.parse_args()
    import en_us
    if args.list_size > len(en_us.top_words):
        print >> sys.stderr, "Cannot use more than {} words from list!".format(len(en_us.top_words))
        exit(1)
    words = en_us.top_words[:args.list_size]
    for i in xrange(args.max_attempts):
        password = generate(words, args.words)
        if args.min_length <= len(password) and (args.max_length is None or len(password) <= args.max_length):
            break
    else:
        print >> sys.stderr, "{} attempts to generate passwords failed!".format(args.max_attempts)
        exit(1)
    if not args.quote:
        print password
    else:
        print repr(password)
    if args.entropy:
        if args.max_length is None:
            max_limit = float(len(words)) ** args.words
        else:
            max_limit = num_passwords(words, args.words, args.max_length)
        min_limit = num_passwords(words, args.words, args.min_length - 1)
        print round(math.log(max_limit - min_limit, 2), 2)
if __name__ == '__main__':
    main()
    
