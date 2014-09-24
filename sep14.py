## September 2014 attempt at Kaggle's Billion Word Imputation
##

## For each sentence in the test set, we have removed exactly one word.
## Participants must create a model capable of inserting back the correct
## missing word at the correct location in the sentence. Submissions are
## scored using an edit distance to allow for partial credit.

import sys
from datetime import datetime

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
    f = open(training_file)
    line_count = 0
    word_count = 0

    start = datetime.now()
    for line in f:
        line_count += 1

        max_limit -= 1
        if max_limit == 0:
            break

        # heart beat
        if line_count % 1000000 == 0:
            delta = datetime.now() - start
            print "%d rows, %d/%d words %02.2f%% took %s" \
                  % (line_count,
                     len(bigrams),
                     word_count,
                     (float(len(bigrams))/word_count) * 100,
                     delta)
            start = datetime.now()

        words = line.split()
        word_count += len(words)
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

if __name__ == "__main__":
    import copy
    argv = copy.copy(sys.argv[1:]) # first arg is filename so
                                   # it can safely be ignored

    ## Match command line arguments against the kwargs spec
    ## ----------------------------------------------------
    kwargs = { "max_limit": (int, -1),
               "training_file": (str, None), }
    for key in kwargs.keys():
        for prefix, end_of_slice in [("--", None), ("-", 1)]:
            # keyword becomes, for example --max-limit and -m
            keyword = "%s%s" % (prefix, key[0:end_of_slice].replace("_", "-"))
            if keyword in argv:
                try:
                    position = argv.index(keyword)
                    # to make sure the value is of the correct type we
                    # run it through a type converter function
                    kwargs[key] = kwargs[key][0](argv[position+1])

                    # remove this keyword and value from argv
                    argv = argv[0:position] + argv[position+2:]

                except ValueError:
                    raise Exception("The flag %s requires a %s"
                                    % (keyword, str(kwargs[key])))
                except IndexError:
                    raise Exception("The flag %s requires a value."
                                    % (keyword))

    # any argument left over is a value for training_file
    if len(argv) == 1:
        kwargs["training_file"] = argv[0]
    elif len(argv) > 1:
        raise Exception("You can't have more than one default argument.")

    # populate kwargs with default values unless provided as arguments
    for key in kwargs.keys():
        if type(kwargs[key]) == tuple: 
            # if the tuple with type and default value hasn't been
            # replaced already we haven't got a value from the user
            # so we replace it now
            kwargs[key] = kwargs[key][1]

    train(**kwargs)
    
