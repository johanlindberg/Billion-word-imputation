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

## Step 2. Solver
## [Attempt 1] Select most frequently occuring word in bigrams.

import util
import test

import string
import sys

## LOGGING
## =======
import logging
logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

## SOLVER
## ======

def replace_missing_word(sentence):
    words = sentence.split()
    i = find_missing_index(words)
    missing_word = None

    previous_word = words[i-1]
    logger.info("Searching for words following '%s'" % \
                (previous_word))

    ch = previous_word[0].upper()
    if ch in string.uppercase:
        bigrams = util.load_bigrams(ch)
    else:
        bigrams = util.load_bigrams('.')

    try:
        previous_bigrams = bigrams[previous_word]
        
        ## sort words by frequency descending
        pb = sorted(previous_bigrams,
                    key = previous_bigrams.get,
                    reverse = True)
        total_occurences = sum(previous_bigrams.values())
        logger.info("%s words to choose from, %d total occurences." % \
                     (len(previous_bigrams), total_occurences))

        ## choose the most frequently used word as missing_word 
        missing_word = pb[0]
        word_occurence = previous_bigrams[missing_word]
        
        ## calculate the percentage of occurence frequency
        logger.info("Selected '%s' (occurs %d times %02.4f%%)" % \
                    (missing_word, word_occurence,
                     float(word_occurence)/total_occurences*100))
    except KeyError:
        ## if the word doesn't exist in the bigrams index
        ## we don't guess.
        logger.warn("'%s' does not exist in bigrams index!" % \
                    (previous_word))
        missing_word = None

    if missing_word:
        result = " ".join(words[:i] + [missing_word] + words[i:])
        _sentence = " ".join(words[:i] + ["<", missing_word, ">"] + words[i:])
    else:
        result = " ".join(words)
        _sentence = " ".join(words[:i] + ["<>"] + words[i:])

    logger.warn("%s" % (_sentence))
    return result

def find_missing_index(words):
    index, index_occurences = -1, 100.0
    for i in range(1, len(words)-1):
        previous_word = words[i-1]
        index_word = words[i]
        logger.info("Searching for word pair '%s-%s'" % \
                    (previous_word, index_word))
 
        ch = previous_word[0].upper()
        if ch in string.uppercase:
            bigrams = util.load_bigrams(ch)
        else:
            bigrams = util.load_bigrams('.')
 
        try:
            previous_bigrams = bigrams[previous_word]
            
            word_occurence = previous_bigrams[index_word]
            total_occurences = sum(previous_bigrams.values())
         
            occurences = float(word_occurence) / total_occurences * 100
            ## calculate the percentage of occurence frequency
            logger.info("'%s-%s' (occurs %d times %02.4f%%)" % \
                        (previous_word, index_word,
                         word_occurence,
                         occurences))
 
            if occurences < index_occurences:
                index = i
                index_occurences = occurences
 
        except KeyError:
            logger.info("'%s-%s' does not exist in bigrams index!" % \
                        (previous_word, index_word))
            index = i
            index_occurences = 0
 
    logger.warn("Missing index is thought to be: %d (%02.4f%%)" % \
                (index, index_occurences))

    return index

def replace_words(test_file, submission_file):
    ## load test_file and replace words in each line
    submission = ['"id","sentence"', ]
    with open(test_file) as f:
        f.readline() # get rid of headers
        for line in f:
            id, sentence = line.split(",")

            s = replace_missing_word(util.decode_sentence(sentence))
            submission.append('%s,"%s"' % (id, util.encode_sentence(s)))

    ## write submission_file
    with open(submission_file, "w") as f:
        for line in submission:
            f.write(line+ "\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "USAGE: python att1.py <test-file> <submission-file>"
        print "  where <submission-file> will be created."

    else:
        test_file, submission_file = sys.argv[1:]
        replace_words(test_file, submission_file)

