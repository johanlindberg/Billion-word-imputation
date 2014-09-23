## September 2014 attempt at Kaggles Billion Word Imputation
##

## For each sentence in the test set, we have removed exactly one word.
## Participants must create a model capable of inserting back the correct
## missing word at the correct location in the sentence. Submissions are
## scored using an edit distance to allow for partial credit.

import sys

N = 10

def train(training_file):
    n = 0
    f = open(training_file)
    for line in f:
        n += 1
        if n > N:
            break

        print line

    f.close()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        train(sys.argv[1])
    else:
        raise Exception("You need to specify a training-file.")
