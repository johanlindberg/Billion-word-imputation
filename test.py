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
## Automatically generated test-cases

import att1
import score
import util

import sys

## LOGGING
## =======
import logging
logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

## TEST-RUNNER
## ===========

def test(original):
    total_scores = []
    total_base_scores = []
    with open(original) as fo:
        line_index = 0
        for line in fo:
            if line_index > 0: # first line contain headers
                id, sentence = line.split(",", 1)
                sentence = util.decode_sentence(sentence)

                logger.info("Testing %s, %s" % (id, sentence))

                ## Test the solver
                ## ---------------

                scores = []
                base_scores = []

                ## generate test sentences
                words = sentence.split()
                for i in range(1, len(words)- 1):
                    test_sentence = " ".join(words[:i] + words[i+1:])

                    ## NOTE! This is a hack to relieve the solver from
                    ## having to figure out the index of which word is
                    ## missing.
                    def f(x):
                        return i
                    att1.find_missing_index = f

                    ## run the solver
                    _sentence = att1.replace_missing_word(test_sentence)
                    logger.info("Scoring '%s'" % (_sentence))

                    ## score the result
                    scores.append(score.levenshtein(sentence, _sentence))
                    base_scores.append(score.levenshtein(sentence,
                                                         test_sentence))

                    logger.info("id: %s score: %d (%d)" % \
                                (id, scores[-1], base_scores[-1]))

                msg = "id: %s avg score %02.4f (%02.4f) %d tests" % \
                      (id, float(sum(scores))/len(scores),
                       float(sum(base_scores))/len(base_scores),
                       len(scores))
                logger.info(msg)
                print msg

                total_scores += scores
                total_base_scores += base_scores

            line_index += 1

    msg = "Total score %02.4f (%02.4f) %d tests" % \
          (float(sum(total_scores))/len(total_scores),
           float(sum(base_scores))/len(base_scores),
           len(total_scores))
    logger.info(msg)
    print msg

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "USAGE: python test.py <file>"

    else:
        test(sys.argv[1])
