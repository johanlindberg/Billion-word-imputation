## September 2014 attempt at Kaggle's Billion Word Imputation

## For each sentence in the test set, we have removed exactly one word.
## Participants must create a model capable of inserting back the
## correct missing word at the correct location in the sentence.
## Submissions are scored using an edit distance to allow for partial
## credit.

## Step 0. Test bed
## Automatically generated test-cases

import att1
import score
import util

import sys

def test(original):
    total_scores = []
    total_base_scores = []
    with open(original) as fo:
        line_index = 0
        for line in fo:
            if line_index > 0: # first line contain headers
                id, sentence = line.split(",")
                sentence = util.decode_sentence(sentence)

                print "*INFO testing %s, %s" % (id, sentence)

                ## Test the solver
                ## --------------------------------------------------

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

                    ## score the result
                    scores.append(score.levenshtein(sentence, _sentence))
                    base_scores.append(score.levenshtein(sentence,
                                                         test_sentence))

                    print "*INFO score: %d base score: %d" % \
                        (scores[-1], base_scores[-1])

                print "*INFO score %02.4f (%02.4f) based on %d tests" % \
                    (float(sum(scores))/len(scores),
                     float(sum(base_scores))/len(base_scores),
                     len(scores))
                total_scores += scores
                total_base_scores += base_scores

            line_index += 1

    print "*INFO total score %02.4f based on %d tests" % \
        (float(sum(total_scores))/len(total_scores),
         len(total_scores))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "USAGE: You must specify an original file."

    else:
        test(sys.argv[1])
