<h3>Billion Word Imputation</h3>

<hr height="1" />

_**Find and impute missing words in the billion word corpus**_

For each sentence in the test set, we have removed exactly one word. Participants must create a model capable of inserting back the correct missing word at the correct location in the sentence. Submissions are scored using an edit distance to allow for partial credit.

Submissions are evaluated on the mean Levenshtein distance between the sentences you submit and the original sentences in the test set.

Your submission file should contain the sentence id and a predicted sentence. To prevent parsing issues, you should use double quotes to escape the sentence text and two double quotes ("") for double quotes within a sentence.

<hr height="1" />

**NOTE!** This github repo does not contain the data files because they're simply too big. Get them at the [competition webpage](https://www.kaggle.com/c/billion-word-imputation).

1. **Development Platform**<br>
I'm using an [Acer C720P Chromebook](http://www.google.com/chrome/devices/acer-c720p-chromebook/) running [Ubuntu Trusty 14.04](http://releases.ubuntu.com/14.04/) via [Crouton](https://github.com/dnschneid/crouton). I use [Python 2.7](https://docs.python.org/2/) and I edit all code in [Emacs](http://www.gnu.org/software/emacs).

2. _**Implementation notes**_<br>
The overall idea for producing a result is to<br>1) process the training-file and build up an index of n-grams (currently [bigrams](http://en.wikipedia.org/wiki/Bigram)) organized alphabetically in separate .pkl files.<br>2) process the test-file line by line, matching two words at a time using the bigram index to decide whether it is more probable that a word should be inserted or not.<br>3) figure out which word is missing by looking at the bigrams and select the most probable.<br><br>

3. _**TODO**_<br>
First and foremost the process of finding the missing word is too slow. There are 306 681 sentences (of varying length) in the test_v2.txt file. Currently we can deal with about 4-5 sentences per minute (optimistic guesstimate) so I'd only have to wait about 1,5-2 months before I can send in a submission to Kaggle. I don't know what would be an acceptable run-time and how far I can improve but it needs to count in hours.

4. _**Example session (current)**_<br>

4.1 _solver (step 2 and 3)_ _att1.py_<br>

Below is some selected output from running on orig.txt (I Ctrl-C'd after 1h43m). It's slightly faster than yesterday (emphasis on slightly). I hope switching to something like [DAWG-dicts](http://dawg.readthedocs.org/en/latest/) will speed it up.

     $ python test.py orig.txt
     id: 1 avg score 4.9286 (5.2857) 14 tests
     id: 2 avg score 6.0526 (6.4737) 19 tests
     id: 3 avg score 5.3200 (5.2400) 50 tests
     id: 4 avg score 8.8824 (5.3529) 17 tests
     id: 5 avg score 9.6087 (5.6087) 23 tests
     id: 6 avg score 11.6857 (5.1143) 35 tests
     id: 7 avg score 4.9091 (5.0000) 11 tests
     id: 8 avg score 5.3750 (5.7500) 8 tests
     ^C

4.2 _preparation (step 1)_ _build_bigrams.py_<br>

This version of the build bigrams code processes the whole training-file in about 80-90 minutes and spits out 27 bigrams files. I had to move the training file to an SD-card in order to run this.

     $ python build_bigrams.py /mnt/sdb1/train_v2.txt 
     *INFO 1000000 rows, 25378842 words. time 0:00:43.715244 (0:00:43.715622)
     *INFO save all bigrams
     *INFO bigrams_A.pkl 0 -> 24879 keys
     *INFO bigrams_B.pkl 0 -> 25130 keys
     *INFO bigrams_C.pkl 0 -> 31650 keys
     ...
     *INFO bigrams_Y.pkl 0 -> 2986 keys
     *INFO bigrams_Z.pkl 0 -> 2432 keys
     *INFO bigrams_*.pkl 0 -> 57855 keys
     *INFO saving 27 bigrams took 0:00:24.483303
     *INFO 2000000 rows, 50741379 words. time 0:01:07.021405 (0:01:50.737135)
     *INFO 3000000 rows, 76120838 words. time 0:00:42.238138 (0:02:32.975356)
     *INFO save all bigrams
     *INFO bigrams_A.pkl 24879 -> 36217 keys
     *INFO bigrams_B.pkl 25130 -> 36145 keys
     *INFO bigrams_C.pkl 31650 -> 45387 keys
     ...
     *INFO bigrams_Y.pkl 16762 -> 17294 keys
     *INFO bigrams_Z.pkl 11609 -> 11889 keys
     *INFO bigrams_*.pkl 365393 -> 377625 keys
     *INFO saving 27 bigrams took 0:05:23.360760
     *INFO 29000000 rows, 735645361 words. time 0:06:06.587985 (1:24:12.863322)
     *INFO 30000000 rows, 761020899 words. time 0:00:41.981535 (1:24:54.844939)
     *INFO save all bigrams
     *INFO bigrams_A.pkl 122690 -> 126081 keys
     *INFO bigrams_B.pkl 116233 -> 119384 keys
     *INFO bigrams_C.pkl 150583 -> 154803 keys
     ...
     *INFO bigrams_Y.pkl 17294 -> 17807 keys
     *INFO bigrams_Z.pkl 11889 -> 12157 keys
     *INFO bigrams_*.pkl 377625 -> 389532 keys
     *INFO saving 27 bigrams took 0:05:38.637519
     *INFO save all bigrams
     *INFO bigrams_A.pkl 126081 -> 126769 keys
     *INFO bigrams_B.pkl 119384 -> 119990 keys
     *INFO bigrams_C.pkl 154803 -> 155611 keys
     ...
     *INFO bigrams_Y.pkl 17807 -> 17904 keys
     *INFO bigrams_Z.pkl 12157 -> 12212 keys
     *INFO bigrams_*.pkl 389532 -> 391904 keys
     Total processing time: 1:36:13.743612
     Total number of processed lines: 30301028
     Total number of processed words: 768648884
