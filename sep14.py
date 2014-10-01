## September 2014 attempt at Kaggle's Billion Word Imputation
##

## For each sentence in the test set, we have removed exactly one word.
## Participants must create a model capable of inserting back the correct
## missing word at the correct location in the sentence. Submissions are
## scored using an edit distance to allow for partial credit.

import cPickle
import string
import sys

from datetime import datetime

heart_beat_interval = 1000000
max_bigrams_size = 30000

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
        self.bigrams_count = 0
        self.line_count = 0
        self.word_count = 0

def save_bigrams(bigram_index, bigrams):
    print ">save_bigrams(%s) %s" % (bigram_index, len(bigrams))
    f_out = open("bigrams_%s.pkl" % (bigram_index), "wb")
    cPickle.dump(bigrams, f_out)
    f_out.close()

def load_bigrams(bigram_index):
    print ">load_bigrams"
    try:
        f_in = open("bigrams_%s.pkl" % (bigram_index), "rb")
        bigrams = cPickle.load(f_in)
        f_in.close()
    except IOError:
        bigrams = {}

    return bigrams

def save_progress(progress):
    print ">save_progress"
    f_out = open("progress.pkl", "wb")
    cPickle.dump(progress, f_out)
    f_out.close()

def load_progress():
    print ">load_progress"
    try:
        f_in = open("progress_state.pkl", "rb")
        progress = cPickle.load(f_in)
        f_in.close()
    except IOError:
        progress = Progress()

    return progress

def train(progress, training_file, max_limit):
    f = open(training_file)
    line_count = 0

    bigrams = None

    tick = datetime.now()
    for line in f:
        progress.line_count += 1
        line_count += 1

        max_limit -= 1
        if max_limit == 0:
            break

        # heart beat
        if line_count % heart_beat_interval == 0:
            _tick = datetime.now()
            split = _tick - tick
            total = _tick - progress.start
            print "%d/%d rows, %d/%d words %02.2f%% time %s (%s)" \
                  % (line_count, progress.line_count,
                     len(bigrams), progress.word_count,
                     (float(len(bigrams))/progress.word_count) * 100,
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
        if len(bigrams.keys()) > max_bigrams_size:
            split = datetime.now() - tick

            _tick = datetime.now()
            save_bigrams(progress.bigrams_count, bigrams)
            _split = datetime.now() - _tick

            print "*INFO processing took %s" % (split)
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

    # if no training file is specified we need to raise an exception
    if kwargs["training_file"] is None:
        raise Exception("You need to specify a training-file.")

    # clear flag
    del kwargs["clear"]

    # populate kwargs with default values unless provided as arguments
    for key in kwargs.keys():
        if type(kwargs[key]) == tuple: 
            # if the tuple with type and default value hasn't been
            # replaced already we haven't got a value from the user
            # so we replace it now
            kwargs[key] = kwargs[key][1]

    progress = load_progress()
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

    save_progress(progress)

