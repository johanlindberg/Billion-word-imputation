Billion Word Imputation
-----------------------------

_**Find and impute missing words in the billion word corpus**_

For each sentence in the test set, we have removed exactly one word. Participants must create a model capable of inserting back the correct missing word at the correct location in the sentence. Submissions are scored using an edit distance to allow for partial credit.

**NOTE!** This github repo does not contain the data files because they're simply too big. Get them at the [competition webpage](https://www.kaggle.com/c/billion-word-imputation).

1. **Development Platform**<br>
I'm using an [Acer C720P Chromebook](http://www.google.com/chrome/devices/acer-c720p-chromebook/) running [Ubuntu Trusty 14.04](http://releases.ubuntu.com/14.04/) via [Crouton](https://github.com/dnschneid/crouton). I use [Python 2.7](https://docs.python.org/2/) and I edit all code in [Emacs](http://www.gnu.org/software/emacs).

2. _**Implementation notes**_<br>
The overall process for producing a result is to 1) process the training-file and build up an index of [bigrams](http://en.wikipedia.org/wiki/Bigram). 2) process the test-file line by line and matching two words at a time using the bigram index to figure out whether it is more probable that a word should be inserted or not.<br>I'm probably going to have to search the bigram index from both ways in order to _pinch_ the missing words. Not sure how to do that, just yet.<br>Also, using trigrams _could_ perhaps enhance the results.<br><br>**TODO**<br>Processing the training file requires a lot of time, CPU and memory. I can't even run through the whole file as it stands. I'm thinking I should split and pickle the `bigrams` hash table with regular intervals. That'll of course grow and become unwieldy as well. But it just might work well enough since I don't care about run time performance as long it doesn't take days to complete.<br>I need to run some tests though to see how much the constant pickle/unpickle operations affects performance.

3. _**Example session (current)**_

This version of the code saves the bigrams to file every 200 000 lines and it takes about 1 minute to process 1 000 001 lines. Current estimate for processing the whole file is about 35 minutes.<br><br>The previous version was significantly slower. It seems that evaluating `len(dict)` on large dicts take a lot of time.

     (trusty)johan@localhost:~/.../Billion Word Imputation$ python count.py 
     . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
     Total time 0:00:53.323787
     Total number of lines 30301028.

     (trusty)johan@localhost:~/Downloads/Playground/Kaggle/Billion Word Imputation$ python sep14.py train_v2.txt -m 1000001 -c True
     *INFO load progress.pkl
     *INFO load bigrams_0.pkl
     *INFO save bigrams_0.pkl 151252 keys
     *INFO processing took 0:00:06.491715
     *INFO saving 151252 bigrams took 0:00:05.329251
     *INFO load bigrams_1.pkl
     *INFO save bigrams_1.pkl 151696 keys
     *INFO processing took 0:00:18.383728
     *INFO saving 151696 bigrams took 0:00:05.692117
     *INFO load bigrams_2.pkl
     *INFO save bigrams_2.pkl 151347 keys
     *INFO processing took 0:00:30.619849
     *INFO saving 151347 bigrams took 0:00:05.653308
     *INFO load bigrams_3.pkl
     *INFO save bigrams_3.pkl 150866 keys
     *INFO processing took 0:00:42.843143
     *INFO saving 150866 bigrams took 0:00:05.646262
     *INFO load bigrams_4.pkl
     *INFO 1000000/1000000 rows, 25378842 words. time 0:00:55.035687 (0:00:55.035785)
     *INFO save bigrams_4.pkl 151030 keys
     *INFO processing took 0:00:00.000036
     *INFO saving 151030 bigrams took 0:00:05.685437
     Total processing time: 0:01:00.918093
     Total number of processed lines: 1000001
     Total number of processed words: 25378858
     *INFO save progress.pkl

4. _**Example session (previous)**_

This version relied on RAM memory for the bigrams hash table and could not process more than about 10 000 000 lines. Estimate to complete the file (had memory been enough) was about 15 minutes.

     (trusty)johan@localhost:~/.../Billion Word Imputation$ python sep14.py train_v2.txt -m 1000001
     1000000 rows, 362630/25378842 words 1.43% took 0:00:30.611223
     2000000 rows, 532807/50741379 words 1.05% took 0:00:30.000417
     3000000 rows, 666837/76120838 words 0.88% took 0:00:29.779393
     4000000 rows, 781747/101462769 words 0.77% took 0:00:29.793588
     5000000 rows, 884790/126834420 words 0.70% took 0:00:29.860021
     6000000 rows, 978430/152208838 words 0.64% took 0:00:31.698201
     7000000 rows, 1065985/177577919 words 0.60% took 0:00:31.574044
     8000000 rows, 1147314/202951922 words 0.57% took 0:00:31.429389
     9000000 rows, 1223958/228313904 words 0.54% took 0:00:31.595810
     10000000 rows, 1297003/253698997 words 0.51% took 0:00:31.448286
