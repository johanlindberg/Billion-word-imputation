## September 2014 attempt at Kaggle's Billion Word Imputation

## Step 2. Clean up bigrams index

## For each sentence in the test set, we have removed exactly one word.
## Participants must create a model capable of inserting back the correct
## missing word at the correct location in the sentence. Submissions are
## scored using an edit distance to allow for partial credit.

import cPickle
import os
import string
import sys

from datetime import datetime

heart_beat_interval = 1000000
max_bigrams_lines = 1000000

# bigrams are a number of hash-tables storing the bigrams found in the
# training-file. They are structured such that each word (key) holds
# another hash-table with another word (key) which holds the number of
# occurances (value).
#
# for example: bigrams["to"]["fly"] = 1 and bigrams["to"]["sleep"] = 3
# means that, so far, the only words found after "to" has been "fly" and
# "sleep" and that they have been found one and three times respectively.
#

def save_bigrams(bigram_index, bigrams):
    if bigrams is None:
        return

    print "*INFO save bigrams_%s.pkl %s keys" % (bigram_index, len(bigrams))
    with open("bigrams_%s.pkl" % (bigram_index), "wb") as f_out:
        cPickle.dump(bigrams, f_out)

def load_bigrams(bigram_index):
    print "*INFO load bigrams_%s.pkl" % (bigram_index)
    try:
        with open("bigrams_%s.pkl" % (bigram_index), "rb") as f_in:
            bigrams = cPickle.load(f_in)
    except IOError:
        bigrams = {}

    return bigrams

def merge(d1, d2):
    duplicates = 0
    keys = 0
    start = datetime.now()
    for k1 in d1.keys():
        keys += 1
        try:
            for v in d2[k1].keys():
                try:
                    d1[k1][v] += d2[k1][v]
                except KeyError:
                    d1[k1][v] = d2[k1][v]

            duplicates += 1
            del d2[k1]

        except KeyError:
            pass

        if keys % 100000 == 0:
            tick = datetime.now() - start
            print "*INFO %s/%s %0.2f%% %s" % (duplicates,
                                              keys,
                                              float(duplicates)/keys*100,
                                              tick)
            start = datetime.now()

    tick = datetime.now() - start
    print "*INFO %s/%s 0.2%f %s" % (duplicates,
                                    keys,
                                    float(duplicates)/keys*100,
                                    tick)

if __name__ == "__main__":
    d1 = load_bigrams(0)
    d2 = load_bigrams(1)
    print "*INFO d1 = %s, d2 = %s" % (len(d1), len(d2)) # 218.5 MB
    merge(d1, d2)
    save_bigrams(0, d1)
    save_bigrams(1, d2)
    print "*INFO d1 = %s, d2 = %s" % (len(d1), len(d2)) # 178.0 MB
