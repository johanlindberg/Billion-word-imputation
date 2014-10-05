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
Processing the training-file produces a lot of bigrams files. Those files are just dumps at regular intervals which means that there are a lot of duplicate words both as keys and values (current estimate is about 50% overlap of keys).<br>Also, I'm going to need to figure out a way of segmenting keys, probably alphabetically, such that I can work the test-file in a time-efficient manner.

4. _**Example session (current)**_

This version of the code processes the whole training-file in about 40-45 minutes and spits out 31 bigrams files. I had to move the training file to an SD-card in order to run this.

     $ python count.py 
     . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
     Total time 0:00:53.323787
     Total number of lines 30301028.

     $ python build_bigrams.py /mnt/sdb1/train_v2.txt 
     *INFO load bigrams_0.pkl
     *INFO 1000000 rows, 25378842 words. time 0:01:01.390676 (0:01:01.390771)
     *INFO Letter frequency: [('*', 21741324), ('T', 376586),
     ('A', 297348), ('S', 292751), ('M', 254222), ('C', 252188),
     ('I', 245944), ('B', 217857), ('P', 158762), ('H', 151721),
     ('W', 151024), ('D', 130108), ('R', 126218), ('F', 123651),
     ('N', 118978), ('G', 110445), ('L', 108021), ('O', 96007),
     ('J', 92174), ('E', 92031), ('U', 90318), ('K', 58570),
     ('Y', 37255), ('V', 32889), ('Z', 10048), ('Q', 9096),
     ('X', 3294)]
     *INFO save bigrams_0.pkl 362630 keys
     *INFO saving 362630 bigrams took 0:00:18.571240
     *INFO load bigrams_1.pkl
     *INFO 2000000 rows, 50741379 words. time 0:01:20.788715 (0:02:22.179680)
     *INFO Letter frequency: [('*', 43472419), ('T', 752253),
     ('A', 594093), ('S', 584641), ('M', 507544), ('C', 504964),
     ('I', 492035), ('B', 435683), ('P', 317991), ('H', 302153),
     ('W', 301366), ('D', 259416), ('R', 251590), ('F', 247297),
     ('N', 238433), ('G', 220469), ('L', 216406), ('O', 192123),
     ('J', 184316), ('E', 183548), ('U', 180515), ('K', 117134),
     ('Y', 74382), ('V', 65376), ('Z', 20270), ('Q', 18411),
     ('X', 6528)]
     *INFO save bigrams_1.pkl 363896 keys
     *INFO saving 363896 bigrams took 0:00:18.451696
     *INFO load bigrams_2.pkl
     *INFO 3000000 rows, 76120838 words. time 0:01:20.568723 (0:03:42.748590)
     *INFO Letter frequency: [('*', 65216801), ('T', 1128490),
     ('A', 890873), ('S', 877012), ('M', 761248), ('C', 757203),
     ('I', 737821), ('B', 653779), ('P', 476770), ('H', 453346),
     ('W', 452240), ('D', 389565), ('R', 377366), ('F', 371018),
     ('N', 357442), ('G', 330550), ('L', 325498), ('O', 287748),
     ('J', 276920), ('E', 275312), ('U', 270975), ('K', 175501),
     ('Y', 111510), ('V', 98127), ('Z', 30365), ('Q', 27675),
     ('X', 9657)]
     *INFO save bigrams_2.pkl 363337 keys
     *INFO saving 363337 bigrams took 0:00:19.052001
     *INFO load bigrams_3.pkl
     ...
     *INFO 28000000 rows, 710284247 words. time 0:01:22.038258 (0:37:37.789443)
     *INFO Letter frequency: [('*', 608541491), ('T', 10523626),
     ('A', 8314422), ('S', 8175553), ('M', 7096529), ('C', 7069549),
     ('I', 6885726), ('B', 6109500), ('P', 4437771), ('H', 4236263),
     ('W', 4228065), ('D', 3633352), ('R', 3525971), ('F', 3460043),
     ('N', 3333607), ('G', 3075780), ('L', 3035570), ('O', 2690126),
     ('J', 2582391), ('E', 2571490), ('U', 2533105), ('K', 1639012),
     ('Y', 1043007), ('V', 914718), ('Z', 282505), ('Q', 254104),
     ('X', 90797)]
     *INFO save bigrams_27.pkl 362868 keys
     *INFO saving 362868 bigrams took 0:00:19.277433
     *INFO load bigrams_28.pkl
     *INFO 29000000 rows, 735645361 words. time 0:01:21.296400 (0:38:59.086025)
     *INFO Letter frequency: [('*', 630270680), ('T', 10899101),
     ('A', 8611924), ('S', 8467432), ('M', 7349670), ('C', 7321940),
     ('I', 7131848), ('B', 6327224), ('P', 4595849), ('H', 4387861),
     ('W', 4378687), ('D', 3763039), ('R', 3652172), ('F', 3583305),
     ('N', 3452457), ('G', 3185397), ('L', 3144561), ('O', 2786457),
     ('J', 2674097), ('E', 2663001), ('U', 2623834), ('K', 1696815),
     ('Y', 1080457), ('V', 947556), ('Z', 292525), ('Q', 263303),
     ('X', 93992)]
     *INFO save bigrams_28.pkl 363001 keys
     *INFO saving 363001 bigrams took 0:00:19.101743
     *INFO load bigrams_29.pkl
     *INFO 30000000 rows, 761020899 words. time 0:01:21.268897 (0:40:20.355107)
     *INFO Letter frequency: [('*', 652013805), ('T', 11275635),
     ('A', 8907408), ('S', 8759297), ('M', 7603307), ('C', 7574266),
     ('I', 7376606), ('B', 6545251), ('P', 4754274), ('H', 4538645),
     ('W', 4529857), ('D', 3893367), ('R', 3778205), ('F', 3707199),
     ('N', 3571055), ('G', 3295243), ('L', 3252846), ('O', 2882153),
     ('J', 2766727), ('E', 2754984), ('U', 2714680), ('K', 1755852),
     ('Y', 1117464), ('V', 980309), ('Z', 302651), ('Q', 272300),
     ('X', 97332)]
     *INFO save bigrams_29.pkl 363331 keys
     *INFO saving 363331 bigrams took 0:00:18.402693
     *INFO load bigrams_30.pkl
     *INFO save bigrams_30.pkl 188610 keys
     Total processing time: 0:41:06.522228
     Total number of processed lines: 30301028
     Total number of processed words: 768648884

     $ python clean_bigrams.py
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
