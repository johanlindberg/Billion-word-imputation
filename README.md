<h3>Billion Word Imputation</h3>

<hr size="1" />

_**Find and impute missing words in the billion word corpus**_

For each sentence in the test set, we have removed exactly one word. Participants must create a model capable of inserting back the correct missing word at the correct location in the sentence. Submissions are scored using an edit distance to allow for partial credit.

Submissions are evaluated on the mean Levenshtein distance between the sentences you submit and the original sentences in the test set.

Your submission file should contain the sentence id and a predicted sentence. To prevent parsing issues, you should use double quotes to escape the sentence text and two double quotes ("") for double quotes within a sentence.

<hr size="1" />

**NOTE!** This github repo does not contain the data files because they're simply too big. Get them at the [competition webpage](https://www.kaggle.com/c/billion-word-imputation).

1. **Development Platform**<br>
I'm using an [Acer C720P Chromebook](http://www.google.com/chrome/devices/acer-c720p-chromebook/) running [Ubuntu Trusty 14.04](http://releases.ubuntu.com/14.04/) via [Crouton](https://github.com/dnschneid/crouton). I use [Python 2.7](https://docs.python.org/2/) and I edit all code in [Emacs](http://www.gnu.org/software/emacs).

2. _**Implementation notes**_<br>
The overall process for producing a result is to<br>1) process the training-file and build up an index of [bigrams](http://en.wikipedia.org/wiki/Bigram) organized alphabetically in separate .pkl files.<br>2) process the test-file line by line, matching two words at a time using the bigram index to decide whether it is more probable that a word should be inserted or not.<br>3) figure out which word is missing by looking at the bigrams and select the most probable.<br><br>I'm probably going to have to search the bigram index from both ways in order to _pinch_ the missing words. I'll probably have to store bigrams from both ends to make that type of search efficient.<br>Also, using trigrams or even higher n-grams _could_ perhaps enhance the results.

3. _**TODO**_<br>
Figure out if there are any improvements that can be made in the replace_missing_word and find_missing_index functions.<br>Add more test sentences from different sources to build a decent test bed base.<br>Also, I'll start working on att2.py which will verify the selected word by making another comparison based on the word after.

4. _**Example session (current)**_<br>

4.1 _solver_ _att1.py_<br>

Running the current test.py and att1.py (with extra logging) produces the following. I've got two versions of this code in att1.py. This is the output from the _2 version which is the best of them.

     $ python test.py test_index.txt
     2014-10-23 22:06:40,875 START
     2014-10-23 22:07:27,948 START
     2014-10-23 22:07:27,950 STOP
     2014-10-23 22:07:27,950 Removing index 1
     2014-10-23 22:07:47,009 Missing index is thought to be: 6
     2014-10-23 22:07:49,938 Returning 'Two studies shed light on whether the video games are good or bad for kids .'
     2014-10-23 22:07:50,090 Removing index 2
     2014-10-23 22:08:09,893 Missing index is thought to be: 2
     2014-10-23 22:08:09,910 Returning 'Two recent years shed light on whether video games are good or bad for kids .'
     2014-10-23 22:08:09,923 Removing index 3
     2014-10-23 22:08:28,067 Missing index is thought to be: 3
     2014-10-23 22:08:28,071 Returning 'Two recent studies have light on whether video games are good or bad for kids .'
     2014-10-23 22:08:28,085 Removing index 4
     2014-10-23 22:08:43,754 Missing index is thought to be: 6
     2014-10-23 22:08:46,803 Returning 'Two recent studies shed on whether the video games are good or bad for kids .'
     2014-10-23 22:08:46,967 Removing index 5
     2014-10-23 22:09:01,338 Missing index is thought to be: 5
     2014-10-23 22:09:03,850 Returning 'Two recent studies shed light of whether video games are good or bad for kids .'
     2014-10-23 22:09:03,991 Removing index 6
     2014-10-23 22:09:18,144 Missing index is thought to be: 3
     2014-10-23 22:09:18,145 Returning 'Two recent studies have shed light on video games are good or bad for kids .'
     2014-10-23 22:09:18,156 Removing index 7
     2014-10-23 22:09:34,497 Missing index is thought to be: 7
     2014-10-23 22:09:37,454 Returning 'Two recent studies shed light on whether the games are good or bad for kids .'
     2014-10-23 22:09:37,620 Removing index 8
     2014-10-23 22:09:52,439 Missing index is thought to be: 7
     2014-10-23 22:09:55,336 Returning 'Two recent studies shed light on whether the video are good or bad for kids .'
     2014-10-23 22:09:55,486 Removing index 9
     2014-10-23 22:10:12,506 Missing index is thought to be: 9
     2014-10-23 22:10:14,450 Returning 'Two recent studies shed light on whether video games . good or bad for kids .'
     2014-10-23 22:10:14,568 Removing index 10
     2014-10-23 22:10:29,347 Missing index is thought to be: 7
     2014-10-23 22:10:32,295 Returning 'Two recent studies shed light on whether the video games are or bad for kids .'
     2014-10-23 22:10:32,447 Removing index 11
     2014-10-23 22:10:46,125 Missing index is thought to be: 11
     2014-10-23 22:10:48,079 Returning 'Two recent studies shed light on whether video games are good . bad for kids .'
     2014-10-23 22:10:48,198 Removing index 12
     2014-10-23 22:11:04,915 Missing index is thought to be: 7
     2014-10-23 22:11:07,896 Returning 'Two recent studies shed light on whether the video games are good or for kids .'
     2014-10-23 22:11:08,044 Removing index 13
     2014-10-23 22:11:24,596 Missing index is thought to be: 7
     2014-10-23 22:11:27,520 Returning 'Two recent studies shed light on whether the video games are good or bad kids .'
     2014-10-23 22:11:27,671 Removing index 14
     2014-10-23 22:11:44,364 Missing index is thought to be: 7
     2014-10-23 22:11:47,267 Returning 'Two recent studies shed light on whether the video games are good or bad for .'
     id: 1 avg score 6.8571 (5.2857) 14 tests
     Total score 6.8571 (5.2857) 14 tests
     2014-10-23 22:11:47,419 STOP

and this is the _1 version.

     $ python test.py test_index.txt
     2014-10-23 22:27:40,783 START
     2014-10-23 22:28:30,716 START
     2014-10-23 22:28:30,717 STOP
     2014-10-23 22:28:30,719 Removing index 1
     2014-10-23 22:28:48,307 Missing index is thought to be: 6 (0.006756)
     2014-10-23 22:28:48,911 Returning 'Two studies shed light on whether video games are good or bad for the kids .'
     2014-10-23 22:28:48,940 Removing index 2
     2014-10-23 22:29:05,962 Missing index is thought to be: 2 (0.000000)
     2014-10-23 22:29:05,963 Returning 'Two recent shed light on whether video games are good or bad for  kids .'
     2014-10-23 22:29:05,976 Removing index 3
     2014-10-23 22:29:22,765 Missing index is thought to be: 3 (0.000000)
     2014-10-23 22:29:22,798 Returning 'Two recent studies light on whether video games are good or bad for  kids .'
     2014-10-23 22:29:22,807 Removing index 4
     2014-10-23 22:29:37,074 Missing index is thought to be: 6 (0.006756)
     2014-10-23 22:29:37,075 Returning 'Two recent studies shed on whether video games are good or bad for the kids .'
     2014-10-23 22:29:37,093 Removing index 5
     2014-10-23 22:29:50,758 Missing index is thought to be: 5 (0.000000)
     2014-10-23 22:29:50,758 Returning 'Two recent studies shed light whether video games are good or bad for  kids .'
     2014-10-23 22:29:50,768 Removing index 6
     2014-10-23 22:30:04,350 Missing index is thought to be: 3 (0.010079)
     2014-10-23 22:30:04,351 Returning 'Two recent studies shed light on video games are good or bad for have kids .'
     2014-10-23 22:30:04,360 Removing index 7
     2014-10-23 22:30:20,400 Missing index is thought to be: 7 (0.004223)
     2014-10-23 22:30:20,400 Returning 'Two recent studies shed light on whether games are good or bad for the kids .'
     2014-10-23 22:30:20,416 Removing index 8
     2014-10-23 22:30:35,309 Missing index is thought to be: 7 (0.006756)
     2014-10-23 22:30:35,309 Returning 'Two recent studies shed light on whether video are good or bad for the kids .'
     2014-10-23 22:30:35,325 Removing index 9
     2014-10-23 22:30:52,029 Missing index is thought to be: 9 (0.002543)
     2014-10-23 22:30:52,030 Returning 'Two recent studies shed light on whether video games good or bad for . kids .'
     2014-10-23 22:30:52,040 Removing index 10
     2014-10-23 22:31:06,593 Missing index is thought to be: 7 (0.006756)
     2014-10-23 22:31:06,593 Returning 'Two recent studies shed light on whether video games are or bad for the kids .'
     2014-10-23 22:31:06,612 Removing index 11
     2014-10-23 22:31:20,202 Missing index is thought to be: 11 (0.001928)
     2014-10-23 22:31:20,203 Returning 'Two recent studies shed light on whether video games are good bad for . kids .'
     2014-10-23 22:31:20,218 Removing index 12
     2014-10-23 22:31:36,998 Missing index is thought to be: 7 (0.006756)
     2014-10-23 22:31:36,998 Returning 'Two recent studies shed light on whether video games are good or for the kids .'
     2014-10-23 22:31:37,015 Removing index 13
     2014-10-23 22:31:53,646 Missing index is thought to be: 7 (0.006756)
     2014-10-23 22:31:53,646 Returning 'Two recent studies shed light on whether video games are good or bad the kids .'
     2014-10-23 22:31:53,661 Removing index 14
     2014-10-23 22:32:10,379 Missing index is thought to be: 7 (0.006756)
     2014-10-23 22:32:10,379 Returning 'Two recent studies shed light on whether video games are good or bad the for .'
     id: 1 avg score 7.7857 (5.2857) 14 tests
     Total score 7.7857 (5.2857) 14 tests
     2014-10-23 22:32:10,432 STOP

4.2 _build_bigrams.py_<br>

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
