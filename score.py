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

## Step 0. Test bed
## Scoring function

import sys

## LOGGING
## =======
import logging
logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

## SCORING FUNCTION
## ================

## Stolen from http://hetland.org/coding/python/levenshtein.py
def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n
        
    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
            
    return current[n]

def score(submitted, original):
    scores = []
    count = 0
    fs = open(submitted)
    fo = open(original)

    ## first line contains headers ("id","sentence")
    _, _ = fs.readline(), fo.readline()

    while True:
        try:
            s = fs.readline()
            o = fo.readline()
            count += 1

            try:
                id1, sentence1 = s.split(",", 1)
                id2, sentence2 = o.split(",", 1)
            except ValueError:
                logger.error("Line %d is invalid!" % (count))
                break

            _score = levenshtein(sentence1, sentence2)
            scores.append(_score)

            logger.info("id: %s score: %d" % (id1, _score))

        except IOError:
            break

    fs.close()
    fo.close()

    msg = "Total score %02.4f %d tests" % \
          (float(sum(scores))/len(scores),
           len(scores))
    logger.info(msg)
    print msg

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "USAGE: python score.py <submission-file> <original-file>"

    else:
        score(sys.argv[1], sys.argv[2])
