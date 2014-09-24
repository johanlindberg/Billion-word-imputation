Billion Word Imputation
-----------------------------

_**Find and impute missing words in the billion word corpus**_

	For each sentence in the test set, we have removed exactly one word. Participants must create a model capable of inserting back the correct missing word at the correct location in the sentence. Submissions are scored using an edit distance to allow for partial credit.

**NOTE!** This github repo does not contain the data files because they're simply too big. Get them at the [competition webpage](https://www.kaggle.com/c/billion-word-imputation).

1. **Development Platform**
I'm using an [Acer C720P Chromebook](http://www.google.com/chrome/devices/acer-c720p-chromebook/) running [Ubuntu Trusty 14.04](http://releases.ubuntu.com/14.04/) via [Crouton](https://github.com/dnschneid/crouton). I use [Python 2.7](https://docs.python.org/2/) and I edit all code in [Emacs](http://www.gnu.org/software/emacs).

2. _**Implementation notes**_
The overall process for producing a result is to 1) process the training-file and build up an index of [bigrams](http://en.wikipedia.org/wiki/Bigram). 2) process the test-file line by line and matching two words at a time using the bigram index to figure out whether it is more probable that a word should be inserted or not.<br>I'm probably going to have to search the bigram index from both ways in order to _pinch_ the missing words. Not sure how to do that, just yet.<br>Also, using trigrams _could_ perhaps enhance the results.<br><br>**TODO**<br>Processing the training file requires a lot of time, CPU and memory. I can't even run through the whole file as it stands. I'm thinking I should split and pickle the `bigrams` hash table with regular intervals. That'll of course grow and become unwieldy as well. But it just might work well enough since I don't care about run time performance as long it doesn't take days to complete.<br>I need to run some tests though to see how much the constant pickle/unpickle operations affects performance.

3. _**Example session**_

		(trusty)johan@localhost:~/Downloads/Playground/Kaggle/Billion Word Imputation$ python sep14.py train_v2.txt -m 10000001
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
