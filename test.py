## September 2014 attempt at Kaggle's Billion Word Imputation

## For each sentence in the test set, we have removed exactly one word.
## Participants must create a model capable of inserting back the
## correct missing word at the correct location in the sentence.
## Submissions are scored using an edit distance to allow for partial
## credit.

## Step 0. Test bed

import sys

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
    score = 0
    count = 0
    fs = open(submitted)
    fo = open(original)

    ## first line contains headers ("id","sentence")
    _, _ = fs.readline(), fo.readline()

    while True:
        s = fs.readline()
        o = fo.readline()
        count += 1

        try:
            id1, sentence1 = s.split(",")
            id2, sentence2 = o.split(",")
        except ValueError:
            print "*ERROR %s is an invalid line" % (count)
            break

        _score = levenshtein(sentence1, sentence2)
        score += _score
        print "*SCORE %02d %s %s" % (_score, id1, sentence1.strip())
        if _score > 0:
            print "*ORIGINAL %s %s" % (id2, sentence2.strip())

    fs.close()
    fo.close()

    print "*TOTAL SCORE %s" % (score)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "USAGE: You must specify a submission file and an original"

    else:
        score(sys.argv[1], sys.argv[2])
