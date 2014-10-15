## September 2014 attempt at Kaggle's Billion Word Imputation

## For each sentence in the test set, we have removed exactly one word.
## Participants must create a model capable of inserting back the
## correct missing word at the correct location in the sentence.
## Submissions are scored using an edit distance to allow for partial
## credit.

## Attempt 1

import test

import sys

def replace_missing_word(sentence):
    s = sentence.split()
    i = find_missing_word(sentence)

    return " ".join(s[:i] + ["HELLO"] + s[i+1:])

def find_missing_word(sentence):
    """NOTE! This method is a stub.
    It is coupled with the contents of test.txt where I've removed the
    word 'light' at index 4"""

    return 4

def replace_words(test_file, submission_file):
    ## load test_file and replace words in each line
    submission = ['"id","sentence"', ]
    with open(test_file) as f:
        f.readline() # get rid of headers
        for line in f:
            id, sentence = line.split(",")
            s = replace_missing_word(sentence)
            submission.append('%s,"%s"' % (id, s))

    ## write submission_file
    with open(submission_file, "w") as f:
        for line in submission:
            f.write(line+ "\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "USAGE: You must specify a test file and a submission file"

    else:
        test_file, submission_file = sys.argv[1:]
        replace_words(test_file, submission_file)
        test.score(submission_file, "orig.txt")
