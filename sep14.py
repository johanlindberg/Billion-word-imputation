## September 2014 attempt at Kaggle's Billion Word Imputation
##

## For each sentence in the test set, we have removed exactly one word.
## Participants must create a model capable of inserting back the correct
## missing word at the correct location in the sentence. Submissions are
## scored using an edit distance to allow for partial credit.

import sys

# bigrams is a hash-table storing the bigrams found in the training-file.
# It's structured such that each word (key) holds another hash-table with
# another word (key) which holds the number of occurances (value).
#
# for example: bigrams["to"]["fly"] = 1 and bigrams["to"]["sleep"] = 3
# means that, so far, the only words found after "to" has been "fly" and
# "sleep" and that they have been found one and three times respectively.
#

bigrams = {}

def train(training_file, max_limit):
    n = 0
    f = open(training_file)
    for line in f:
        n += 1
        if n > max_limit:
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
    import copy
    argv = copy.copy(sys.argv)

    kwargs = { "max_limit": int,
               "training_file": str, }
    for key in kwargs.keys():
        for prefix, end_of_slice in [("--", None), ("-", 1)]:
            keyword = "%s%s" % (prefix, key[0:end_of_slice].replace("_", "-"))
            if keyword in argv:
                try:
                    position = argv.index(keyword)
                    kwargs[key] = kwargs[key](argv[position+1])

                    # remove from argv
                    argv = argv[0:position] + argv[position+2:]

                except IndexError:
                    raise Exception("The flag %s requires a value." % (keyword))

    if len(argv) == 2:
        kwargs["training_file"] = argv[1]
    else:
        raise Exception("You can't have more than one default argument.")

    train(**kwargs)
    
