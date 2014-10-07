## September 2014 attempt at Kaggle's Billion Word Imputation

## Step 1. Build bigrams index

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

class Progress(object):
    def __init__(self):
        self.line_count = 0
        self.word_count = 0

def merge_bigrams(b1, b2):
    """merge_bigrams moves all key/value pairs from <b2> to <b1>.

    >>> b1 = {'a': {'b': 1, 'c': 1}}
    >>> b2 = {'a': {'c': 1, 'd': 1}}
    >>> merge_bigrams(b1, b2)
    >>> b1['a']['b']
    1
    >>> b1['a']['c']
    2
    >>> b1['a']['d']
    1
    """
    for k1 in b1.keys():
        try:
            for v in b2[k1].keys():
                try:
                    b1[k1][v] += b2[k1][v]
                except KeyError:
                    b1[k1][v] = b2[k1][v]

        except KeyError:
            pass            

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

def train(progress, training_file, max_limit):
    f = open(training_file)

    bigrams = None

    tick = datetime.now()
    for line in f:
        progress.line_count += 1

        max_limit -= 1
        if max_limit == 0:
            break

        # heart beat
        if progress.line_count % heart_beat_interval == 0:
            _tick = datetime.now()
            split = _tick - tick
            total = _tick - progress.start
            print "*INFO %d rows, %d words. time %s (%s)" \
                  % (progress.line_count,
                     progress.word_count,
                     split, total)
            tick = datetime.now()

        # load bigrams dict from file unless already loaded
        if bigrams is None:
            bigrams = load_bigrams(progress.bigrams_count)

        words = line.split()
        progress.word_count += len(words)
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

        # save bigrams to file if it contains more than
        # max_bigrams_size keys.
        if progress.line_count % max_bigrams_lines == 0:
            _tick = datetime.now()
            save_bigrams(progress.bigrams_count, bigrams)
            _split = datetime.now() - _tick

            print "*INFO saving %s bigrams took %s" % (len(bigrams), _split)

            progress.bigrams_count += 1
            bigrams = None

    save_bigrams(progress.bigrams_count, bigrams)

    f.close()

if __name__ == "__main__":
    import copy
    argv = copy.copy(sys.argv[1:]) # first arg is filename so
                                   # it can safely be ignored

    ## Match command line arguments against the kwargs spec
    ## ----------------------------------------------------
    kwargs = { "clear": (bool, False),
               "max_limit": (int, -1),
               "test": (bool, False),
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

    # if the test flag is set we should run all doctests and exit
    if kwargs["test"]:
        import doctest
        doctest.testmod()
        sys.exit(0)

    # any argument left over is a value for training_file
    if len(argv) == 1:
        kwargs["training_file"] = argv[0]
    elif len(argv) > 1:
        raise Exception("You can't have more than one default argument.")

    # if no training file is specified we need to raise an exception
    if kwargs["training_file"] is None:
        raise Exception("You need to specify a training-file.")

    # if the clear flag is set we should `rm *.pkl` 
    if kwargs["clear"]:
        for f in os.listdir(os.getcwd()):
            if f.endswith(".pkl"):
                os.remove(f)
    del kwargs["clear"]

    # populate kwargs with default values unless provided as arguments
    for key in kwargs.keys():
        if type(kwargs[key]) == tuple: 
            # if the tuple with type and default value hasn't been
            # replaced already we haven't got a value from the user
            # so we replace it now
            kwargs[key] = kwargs[key][1]

    progress = Progress()
    progress.start = datetime.now()
    kwargs["progress"] = progress
    try:
        train(**kwargs)
    except KeyboardInterrupt:
        pass

    _tick = datetime.now()
    print "Total processing time: %s" % (_tick - progress.start)
    print "Total number of processed lines: %s" % (progress.line_count)
    print "Total number of processed words: %s" % (progress.word_count)

