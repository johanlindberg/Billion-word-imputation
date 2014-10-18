## September 2014 attempt at Kaggle's Billion Word Imputation

## For each sentence in the test set, we have removed exactly one word.
## Participants must create a model capable of inserting back the
## correct missing word at the correct location in the sentence.
## Submissions are scored using an edit distance to allow for partial
## credit.

## Your submission file should contain the sentence id and a predicted
## sentence. To prevent parsing issues, you should use double quotes to
## escape the sentence text and two double quotes ("") for double
## quotes within a sentence. Note that test.csv is a valid submission
## file itself.
##
## The file should contain a header and have the following format:
##
##   id,"sentence"
##   1,"Former Dodgers ... story after another ."
##   2,"8 parliamentary ... ally against Islamic ."
##   3,"Sales of drink ... from a small base ."
##   etc...

import cPickle
import string
import sys

## LOGGING
## =======
import logging
logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

## UTILITIES
## =========

def load_bigrams(bigram_index):
    logger.info("Loading bigrams_%s.pkl" % (bigram_index))
    try:
        with open("/media/removable/SD Card/bigrams_%s.pkl" % \
                  (bigram_index), "rb") as f_in:
            bigrams = cPickle.load(f_in)
    except IOError:
        logger.warn("bigrams_%s.pkl doesn't exist!" % (bigram_index))
        bigrams = {}

    logger.info("bigrams_%s.pkl contains %d bigrams." % \
                (bigram_index, len(bigrams)))

    return bigrams

def save_bigrams(bigrams):
    logger.info("Saving all bigrams to file.")
    for ch in string.uppercase + '.':
        b1 = merge_bigrams(bigrams[ch], load_bigrams(ch))
        logger.info("Saving %d keys in bigrams_%s.pkl" % \
                    (len(b1), ch))
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
