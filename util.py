## September 2014 attempt at Kaggle's Billion Word Imputation

## For each sentence in the test set, we have removed exactly one word.
## Participants must create a model capable of inserting back the
## correct missing word at the correct location in the sentence.
## Submissions are scored using an edit distance to allow for partial
## credit.

## Utilities

import cPickle
import sys

def load_bigrams(bigram_index):
    print "*INFO bigrams_%s.pkl" % (bigram_index),
    try:
        with open("/media/removable/SD Card/bigrams_%s.pkl" % (bigram_index), "rb") as f_in:
            bigrams = cPickle.load(f_in)
    except IOError:
        bigrams = {}

    print len(bigrams)
    return bigrams

def save_bigrams(bigrams):
    print "*INFO save all bigrams"
    for ch in string.uppercase + '*':
        b1 = merge_bigrams(bigrams[ch], load_bigrams(ch))
        print "%s keys" % (len(b1))
        with open("bigrams_%s.pkl" % (ch), "wb") as f_out:
            cPickle.dump(b1, f_out)
        bigrams[ch] = None


def decode_sentence(sentence):
    """Strip newlines and quotes from first and last position."""
    sentence = sentence.strip("\n")
    if sentence[0] == '"':
        sentence = sentence[1:]
    if sentence[-1] == '"':
        sentence = sentence[:-1]

    return sentence

def encode_sentence(sentence):
    """Change all " to "" in sentence.
    NOTE! This is a stub. It just returns sentence as-is."""
    return sentence

if __name__ == "__main__":
    import doctest
    doctest.testmod()

