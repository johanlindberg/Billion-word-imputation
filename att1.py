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

## Attempt 1

import util
import test

import sys

def replace_missing_word(sentence):
    words = sentence.split()
    i = find_missing_index(words)
    missing_word = None

    previous_word = words[i-1]
    print "*INFO searching for words following '%s'" % (previous_word)

    bigrams = util.load_bigrams(previous_word[0])
    try:
        previous_bigrams = bigrams[previous_word]
        
        ## sort words by frequency descending
        pb = sorted(previous_bigrams, key = previous_bigrams.get, reverse = True)
        total_occurences = sum(previous_bigrams.values())
        print "*INFO %s words to choose from. %d occurences in total." % \
            (len(previous_bigrams), total_occurences)

        ## choose the most frequently used word as missing_word 
        missing_word = pb[0]
        word_occurence = previous_bigrams[missing_word]
        
        ## calculate the percentage of occurence frequency
        print "*INFO selected '%s' (%d %02.4f%%)" % \
            (missing_word, word_occurence,
             float(word_occurence)/total_occurences*100)
    except KeyError:
        ## if the word doesn't exist in the bigrams index
        ## we don't guess
        missing_word = ""

    return " ".join(words[:i] + [missing_word] + words[i:])

def find_missing_index(words):
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

            s = replace_missing_word(util.decode_sentence(sentence))
            submission.append('%s,"%s"' % (id, util.encode_sentence(s)))

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
