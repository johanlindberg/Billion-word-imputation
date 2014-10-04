Billion Word Imputation
-----------------------------

_**Find and impute missing words in the billion word corpus**_

For each sentence in the test set, we have removed exactly one word. Participants must create a model capable of inserting back the correct missing word at the correct location in the sentence. Submissions are scored using an edit distance to allow for partial credit.

**NOTE!** This github repo does not contain the data files because they're simply too big. Get them at the [competition webpage](https://www.kaggle.com/c/billion-word-imputation).

1. **Development Platform**<br>
I'm using an [Acer C720P Chromebook](http://www.google.com/chrome/devices/acer-c720p-chromebook/) running [Ubuntu Trusty 14.04](http://releases.ubuntu.com/14.04/) via [Crouton](https://github.com/dnschneid/crouton). I use [Python 2.7](https://docs.python.org/2/) and I edit all code in [Emacs](http://www.gnu.org/software/emacs).

2. _**Implementation notes**_<br>
The overall process for producing a result is to<br>1) process the training-file and build up an index of [bigrams](http://en.wikipedia.org/wiki/Bigram).<br>2) merge all of the bigrams files to weed out duplicates and get a reasonable efficient data storage.<br>3) process the test-file line by line and matching two words at a time using the bigram index to figure out whether it is more probable that a word should be inserted or not.<br><br>I'm probably going to have to search the bigram index from both ways in order to _pinch_ the missing words. Not sure how to do that, just yet.<br>Also, using trigrams _could_ perhaps enhance the results.

3. _**TODO**_<br>
Processing the training-file produces a lot of bigrams files. Those files are just dumps at regular intervals which means that there are a lot of duplicate words both as keys and values (current estimate is about 50% overlap of keys). Also, I'm going to need to figure out a way of segmenting keys, probably alphabetically, such that I can work the test-file in a time-efficient manner.

4. _**Example session (current)**_

This version of the code processes the whole training-file in about 25-30 minutes and spits out 30 bigrams files. I had to move the training file to an SD-card in order to run this.

     (trusty)johan@localhost:~/.../Billion Word Imputation$ python count.py 
     . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
     Total time 0:00:53.323787
     Total number of lines 30301028.

     (trusty)johan@localhost:~/.../Billion Word Imputation$ python build_bigrams.py /mnt/sdb1/train_v2.txt 
     *INFO load bigrams_0.pkl
     *INFO 1000000 rows, 25378842 words. time 0:00:31.448211 (0:00:31.448287)
     *INFO save bigrams_0.pkl 362630 keys
     *INFO saving 362630 bigrams took 0:00:18.530142
     *INFO load bigrams_1.pkl
     *INFO 2000000 rows, 50741379 words. time 0:00:49.798382 (0:01:21.246760)
     *INFO save bigrams_1.pkl 363896 keys
     *INFO saving 363896 bigrams took 0:00:18.440293
     *INFO load bigrams_2.pkl
     *INFO 3000000 rows, 76120838 words. time 0:00:49.715474 (0:02:10.962312)
     *INFO save bigrams_2.pkl 363337 keys
     *INFO saving 363337 bigrams took 0:00:19.093823
     *INFO load bigrams_3.pkl
     ...
     *INFO 28000000 rows, 710284247 words. time 0:00:55.393994 (0:23:46.943986)
     *INFO save bigrams_27.pkl 362868 keys
     *INFO saving 362868 bigrams took 0:00:19.845263
     *INFO load bigrams_28.pkl
     *INFO 29000000 rows, 735645361 words. time 0:00:51.847141 (0:24:38.791207)
     *INFO save bigrams_28.pkl 363001 keys
     *INFO saving 363001 bigrams took 0:00:20.010363
     *INFO load bigrams_29.pkl
     *INFO 30000000 rows, 761020899 words. time 0:00:51.734306 (0:25:30.525632)
     *INFO save bigrams_29.pkl 363331 keys
     *INFO saving 363331 bigrams took 0:00:18.877618
     *INFO load bigrams_30.pkl
     *INFO save bigrams_30.pkl 188610 keys
     Total processing time: 0:26:07.995869
     Total number of processed lines: 30301028
     Total number of processed words: 768648884

     (trusty)johan@localhost:~/.../Billion Word Imputation$ python clean_bigrams.py
     *INFO load bigrams_0.pkl
     *INFO load bigrams_1.pkl
     *INFO d1 = 362630, d2 = 363896
     *INFO 54155/100000 54.16% 0:00:01.637949
     *INFO 107984/200000 53.99% 0:00:01.506188
     *INFO 160864/300000 53.62% 0:00:01.464472
     *INFO 193719/362630 53.42% 0:00:01.088057
     *INFO save bigrams_0.pkl 362630 keys
     *INFO save bigrams_1.pkl 170177 keys
     *INFO d1 = 362630, d2 = 170177
