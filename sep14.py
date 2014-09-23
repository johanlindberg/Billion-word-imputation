## September 2014 attempt at Kaggles Billion Word Imputation
##

import sys

def train(training_file):
    pass

if __name__ == "__main__":
    if len(sys.argv) == 2:
        train(sys.argv[1])
    else:
        raise Exception("You need to specify a training-file.")
