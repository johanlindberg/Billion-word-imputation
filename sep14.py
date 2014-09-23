## September 2014 attempt at Kaggle's Billion Word Imputation
##

## For each sentence in the test set, we have removed exactly one word.
## Participants must create a model capable of inserting back the correct
## missing word at the correct location in the sentence. Submissions are
## scored using an edit distance to allow for partial credit.

import sys

N = 1000

# bigrams is a hash-table storing the bigrams found in the training-file.
# It's structured such that each word (key) holds another hash-table with
# another word (key) which holds the number of occurances (value).
#
# for example: bigrams["to"]["fly"] = 1 and bigrams["to"]["sleep"] = 3
# means that, so far, the only words found after "to" has been "fly" and
# "sleep" and that they have been found one and three times respectively.
#

bigrams = {}

def train(training_file):
    n = 0
    f = open(training_file)
    for line in f:
        n += 1
        if n > N:
            break

        words = line.split()
        for i in xrange(len(words) - 1):
            a, b = words[i], words[i+1]

            try:
                _b = bigrams[a]
            except KeyError:
                bigrams[a] = { b : 0, }
                _b = bigrams[a]

            try:
                _b[b] += 1
            except KeyError:
                _b[b] = 1

    f.close()

    # stats
    print len(bigrams.keys())

if __name__ == "__main__":
    if len(sys.argv) == 2:
        train(sys.argv[1])
    else:
        raise Exception("You need to specify a training-file.")
