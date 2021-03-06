import sys
import argparse
import logging
import math
import nltk
import random
import search
import lstm.ptb_word_lm as nn
from itertools import chain
from datetime import datetime

############################
# Configuration variables
############################
pos_training_path = "../lib/tagged/english-bidirectional-distsim.tagger"
pos_jar_path = "../lib/jar/stanford-postagger.jar"

# Minimum amount of choices for the next word (otherwise lower gram).
# This configures the focus on the real documents.
# A wide choice gives more freedom to the LSTM -> more general (or financial) English.
# A smaller choice forces more real document content in the story (the n-grams dominate).
min_amount = 10

# How many sentences per story shall we generate?
sentence_count = 10

# Sentence terminators. We want flowing stories, so skipping these for now.
terminator_types = ['.', ':']
terminator_words = ['<eos>']
s_terminator = '<eos>'

# E.g. adjectives can not end sentences (it tends to give bad results).
forbidden_type_sequences = {
    "ADJ": [".", ":"],
    "IN": [".", ":"],
    "JJ": [".", ":", "VB"],
    "RB": [".", ":"],
    "VBZ": [".", ":"],
    "POS": [".", ":"],
    ".": [".", ":"]
}

forbidden_types = ["``", "''", "CD", ":", "(", ")"]
forbidden_tokens = set(["(", ")", "[", "]", ",", "'", "\"", ";", "``","“", "?", "!", ".", "へ", "‿", "_", "''", "&", "gt"])

''' Here we may want parameters for different story datasets.
I'm leaving it as-is for example purposes. The parameters we want to tune will
likely be very different. '''
# Template parameters:
# shortname - >
# dataset
# [max-length, min-length, min-length-before-pref]
# start sequence (Must be at least 2 words, no unigrams.)
# preferred words
# preferred sequence
# exceptions from terminator_types
story_map = {
    "pride": [
        "../lib/datasets/prideandprejudice.txt",
        [1000, 0, 0],
        ["i", "feel"],
        [],
        [],
        [],
        nltk.MLEProbDist
    ],
    "tolkien": [
        "../lib/datasets/tolkien.txt",
        [1000, 0, 0],
        ["frodo", "was"],
        [],
        [],
        [],
        nltk.MLEProbDist
    ],
    "tifu": [
        "../datasets/tifu/storybot.txt",
        [1000, 0, 0],
        [s_terminator],
        [],
        [],
        [],
        nltk.MLEProbDist
    ],
    "retail": [
        "../datasets/talesfromretail/storybot.txt",
        [1000, 0, 0],
        [s_terminator],
        [],
        [],
        [],
        nltk.MLEProbDist
    ],
    "techsupport": [
        "../datasets/talesfromtechsupport/storybot.txt",
        [1000, 0, 0],
        [s_terminator],
        [],
        [],
        [],
        nltk.MLEProbDist
    ],
    "pettyrevenge": [
        "../datasets/pettyrevenge/storybot.txt",
        [1000, 0, 0],
        [s_terminator],
        [],
        [],
        [],
        nltk.MLEProbDist
    ],
    "prorevenge": [
        "../datasets/prorevenge/storybot.txt",
        [1000, 0, 0],
        [s_terminator],
        [],
        [],
        [],
        nltk.MLEProbDist
    ]
}


############################
# Utility functions
############################
def normalize(prob_list):
    prob_sum = sum(prob_list)
    return [math.exp(math.log(p) - math.log(prob_sum)) for p in prob_list]


def parse_args():
    parser = argparse.ArgumentParser(
            description="Generate text based on given corpus.",
            epilog='Example of use: storybot.py -n tifu')
    parser.add_argument("-n", "--name", help="Short name of corpus to load: {tifu}", )
    parser.add_argument("-q", "--query", default = "", help="An intersection query to select a subset of documents.", )
    parser.add_argument("-v", "--verbose", action='store_true', help="Increase output verbosity")
    args = parser.parse_args()

    if args.name not in ["tifu", "retail", "techsupport", "pettyrevenge", "prorevenge"]:
        print("Wrong corpus name given. Must be one of: {tifu, retail, techsupport, pettyrevenge, prorevenge}")
        parser.print_help()
        sys.exit(-2)
    return args


def setup_logging(verbose):
    import os
    if not os.path.isdir("../logs/"):
        os.makedirs("../logs/")
    today = datetime.now().strftime("%Y-%m-%d")
    # Log DEBUG and INFO to file
    logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s: %(levelname)-8s %(message)s',
            datefmt='%Y-%m-%d %H:%M',
            filename='../logs/%s_storybot.log' % today,
            filemode='a'
    )

    # Log to console based on specified verbosity
    console = logging.StreamHandler()
    level = logging.DEBUG if verbose else logging.INFO
    console.setLevel(level)
    formatter = logging.Formatter('%(asctime)s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def embellish(tokens):
    """
    :param tokens: a 2D list of token and POS tag for the entire text generated up until now.
    :return: Capitalized most recent sentence generated.
    """
    ret = []
    for token in tokens[-2::-1]:
        if token[0] == '<eos>':
            break
        ret.insert(0, token[0])
    ret[0] = ret[0].capitalize()

    # concatentate tokens starting with apostrophe
    # and capitalize i:s
    start_chars = ("'", "n'")
    for i, t in enumerate(ret):
        if t == 'i':
            ret.pop(i)
            ret.insert(i, 'I')
        if t.startswith(start_chars):
            t2 = ret.pop(i)
            t1 = ret.pop(i-1)
            ret.insert(i-1, t1+t2)

    ret = " ".join(ret)
    return ret + "."


# PosTagger class - make POS tagger changes easier.
class PosTagger:
    def __init__(self, tagger_type):
        if(tagger_type == 'stanford'):
            self.tagger = nltk.StanfordPOSTagger(pos_training_path, pos_jar_path)
            self.tag = self.tagger.tag
        elif(tagger_type == 'nltk'):
            self.tag = nltk.pos_tag
        else:
            raise ValueError('Required POS tagger \"' + tagger_type + '\" is unknown.')


def vocabulary_stats(words):
    print("Wait for the stats...")
    text_size = len(words)
    vocabulary = set(words)
    vocab_size = len(vocabulary)
    print("Vocabulary size is {} words.".format(vocab_size))
    words_stat = dict()
    for w in words:
        if w in words_stat:
            words_stat[w] += 1
        else:
            words_stat[w] = 1
    word_counts = sorted(words_stat.values())
    # Invert sorting order.
    word_counts[:] = word_counts[::-1]
    assert(vocab_size == len(word_counts))
    top_n = [1000, 2000, 3000, 4000, 5000, 10000, 20000]
    cum_sum = 0
    idx = 0
    for top in top_n:
        while(idx < min(vocab_size, top)):
            cum_sum += word_counts[idx]
            idx += 1
        print("{} top vocabulary words cover {:.2f}% of the text.".format(idx, 100.0*cum_sum/text_size))


def text2words(text):
    words = []
    tokenized_sentences = nltk.sent_tokenize(text)
    for i, sentence in enumerate(tokenized_sentences):
        tokenized_sentence = nltk.tokenize.word_tokenize(sentence)

        while tokenized_sentence[-1] in forbidden_tokens:
            tokenized_sentence = tokenized_sentence[:-1]
            if len(tokenized_sentence) == 0:
                break

        if len(tokenized_sentence) == 0:
            continue

        tokenized_sentence.append(s_terminator)
        for tok in tokenized_sentence:
            if not tok in forbidden_tokens:
                words.append(tok)
    return words


############################
# Main body of code
############################
class StoryGen:
    # Enable/disable the POS tagger. Maybe not needed to have it enabled when using LSTM.
    pos_tagger_enabled = False
    # LSTM enable/disable configuration.
    lstm_enabled = True
    # The longest sequence of words being sent to the LSTM.
    max_lstm_steps = 30
    # When the n-grams fail to find anything, generate at most max_random_words instead.
    max_random_words = 400
    # When the LSTM says "terminate the sentence", we "toss a coin" and terminate with
    # probability sure_terminate_prob.
    sure_terminate_prob = 0.5

    ngrams_terminator_probability = 0.02

    # How many times is n-gram score larger than (n-1)-gram score? 10 - a lot, 1.2 - much less
    # This should be always larger than 1.
    ngrams_decay_base = 3.0

    def __init__(self, shortname, min_grams=2, max_grams=5, text=""):
        self.posTagger = PosTagger('nltk')
        if self.lstm_enabled:
            #self.lstm = nn.Lstm("../models/lstm/ptb/model5.ckpt","../datasets/ptb/ptb.train.txt", self.max_lstm_steps)
            #self.lstm = nn.Lstm("../models/lstm/tailsfromretail/model4.ckpt","../datasets/talesfromretail_lstm/ptb.train.txt", self.max_lstm_steps)
            self.lstm = nn.Lstm("../models/lstm/tifu/model4.ckpt","../datasets/tifu_lstm/ptb.train.txt", self.max_lstm_steps)
        self.sentence_count = 0
        self.shortname = shortname
        self.min_grams = min_grams
        self.max_grams = max_grams

        (filepath, limits, self.startSeq, self.preferred, self.preferred_seq,
         self.term_except, smoothing_factory) = story_map[shortname]
        self.max_length, self.min_length, self.min_preferred = limits
        self.out = ""  # self.out contains all the text we have generated.

        # Either load the full corpus or just use the provided text string
        # for story generation.
        if(text == ""):
            raw = open(filepath, 'r', encoding="utf8").read().lower()
        else:
            raw = text.lower()
        self.text = "".join(raw.split())

        words = text2words(raw)

        self.vocabulary = set(words)
        vocabulary_stats(words)

        logging.debug("Creating corpus...")
        self.models = [None] * (max_grams + 1)
        self.estimates = [None] * (max_grams + 1)

         # create n-grams on unbroken sequences of text.
        logging.debug("Creating {0}-{1} grams models...".format(min_grams, max_grams))
        for n in range(min_grams, max_grams + 1):
            ngrams = nltk.ngrams(words, n)
            formatted = []
            for grams in ngrams:
                prev = grams[:-1]
                res = grams[-1]
                formatted.append((prev, res))
            dist = nltk.ConditionalFreqDist(formatted)
            self.models[n] = dist
            self.estimates[n] = nltk.ConditionalProbDist(dist, smoothing_factory, bins=len(self.vocabulary))

        self.startPhrase = [[w, t] for (w, t) in self.posTagger.tag(self.startSeq)]  # TODO: Change anything here?


    def is_terminator(self, out):
        next_word, next_type = out[-1][0], out[-1][1]
        if next_word == s_terminator:
            logging.debug("Found terminator: %s " % out[-1][0][0])
            return True
        return False

    def key_for_gram_count(self, out, gram_count):
        """
        :param out: List of [[word, tag], ...]
        :param gram_count: Size of n-gram
        :return: the key to use for finding next token
        For a 5-gram the key should be 4 tokens
        For a 4-gram the key should be 3 tokens
        etc.
        """
        words_in_key = gram_count - 1
        key = [x[0] for x in out[-words_in_key:]]
        # If the current key is shorter than the gram count then pad with <s> # TODO: Remove this code path
        if len(out) < words_in_key:
            for _ in range(0, words_in_key - len(out)):
                key.insert(0, "<s>")

        return tuple(key)


    # Check if a word is allowed, depending on word, type, previous word,
    # and the full sequence.
    def isAllowed(self, next_word, next_type, word, out):
        # Do not put preferred word too early, decided by min_preferred.
        if len(out) < self.min_preferred and next_word in self.preferred:
            return False

        # # Only use preferred word once.
        # if next_word in self.preferred and next_word in [x[0] for x in out]:
        #     return False

        # # Do not terminate sentence before preferred word.
        # if self.isTerminator(next_word, next_type):
        #     for pref in self.preferred:
        #         if pref not in [x[0] for x in out]:
        #             return False

        # Do not terminate too early.
        if (len(out) < self.min_length) and (self.isTerminator(next_word, next_type)):
            return False

        # Check if the sequence is forbidden, e.g. terminator after adjective.
        if (word[1] in forbidden_type_sequences) and (next_type in forbidden_type_sequences[word[1]]):
            return False

        # Check if type is forbidden.
        if next_type in forbidden_types:
            return False

        # Check if word has been used in the past 4 words, avoid repetition.
        if next_word in [x[0] for x in out[-4:]]:
            return False

        # Check if sequence has been used in past 10 words, avoid repetition
        if [word, next_word] in [x[0] for x in out[-10:]]:
            return False

        return True

    def generate_tagged_choice(self, prob_dist, num_choices):
        """
        :param key: the n-gram input
        :param gram_count: how large the n-gram is
        :param num_choices: how many candidate tokens should be returned
        :return: a list of randomly chosen candidate tokens, sorted by probability in descending order
        This method picks num_choices random tokens from the probability distribution and returns a list of
        distinct tagged tokens.
        """

        choices = []
        for i in range(0, num_choices):
            token = prob_dist.generate()
            if token not in choices:
                choices.append(token)
        tagged_choices = self.posTagger.tag(choices)
        return tagged_choices

    def random_word_dict(self):
        k = min(len(self.vocabulary), self.max_random_words)
        words = random.sample(self.vocabulary, k)
        wd = dict()
        for w in words:
            wd[w] = 1.0/len(words)
        return wd

    def filter_lstm_input(self, current_seq, choice_seq):
        # Substitute '<s>' for '<eos>' (end of sentence).
        #word_choice = [wt if not wt == '<s>' else '<eos>' for wt in choice_seq ]
        # Remove '.' from any possible word of choice. TODO: This is only a hotfix!
        #word_choice = [w if not w[-1] == '.' else w[:-1] for w in word_choice ]
        # Extract up to the last self.max_lstm_steps words from the output
        # sequence. This sequence will be sent to the LSTM as input.
        word_choice = choice_seq
        roll_begin = max(0, len(current_seq)-self.max_lstm_steps)
        word_seq = [current_seq[i][0] for i in range(roll_begin, len(current_seq))]
        #word_seq = [w if not w=='<s>' else '<eos>' for w in word_seq]
        return [word_seq, word_choice]


    # Return the union of dict1 and dict2, adding only non-present values to dict1 from dict2.
    # Values of dict2 are pre-multiplied by c before adding to dict1.
    def merge_dicts(self, dict1, dict2, c):
        for k, v in dict2.items():
            if k not in dict1:
                dict1[k] = v * c
        return dict1

    # Multiply probabilities of words in wpdict dictionary by LSTM predictions.
    def lstm_prob(self, word_seq, wpdict):
        in_words = list(wpdict.keys())
        word_seq, word_choice = self.filter_lstm_input(word_seq, in_words)
        wscore = self.lstm.predict_choice(word_seq, word_choice, 0.0)
        top_word = word_choice[wscore.index(max(wscore))]
        wprob = self.lstm.score2prob(wscore)
        ndict = dict()
        for i in range(0, len(in_words)):
            wpdict[in_words[i]] *= wprob[i]
        return [wpdict, top_word]


    # Build a dictionary from the specified probability distribution.
    def prob_dict(self, key, gram_count):
        samples = list(self.estimates[gram_count][key].samples())
        d = dict()
        for s in samples:
            d[s] = self.estimates[gram_count][key].prob(s)
        return d

    def normalize_pdict(self, pdict):
        psum = sum(pdict.values())
        for k, v in pdict.items():
            pdict[k] = pdict[k]/psum
        return pdict

    def first_good_choice(self, tagged_choices, seq):
        for i in range(0, len(tagged_choices)):
            next_word, next_type = tagged_choices[i]
            logging.debug("Candidate word: %s" % next_word)
            if not self.isAllowed(next_word, next_type, seq[-1], seq):
                continue
            else:
                return [next_word, next_type]
        return None

    # Add one word to the sequence seq, using between min_ and max_grams ngrams model.
    # Return [succeeded = False/True, (extended) sequence].
    def extend_sequence(self, min_grams, max_grams, seq):
        gram_count = max_grams
        num_choices = 0

        # Decide the range of ngram models required for obtaining enough choices.
        while gram_count >= min_grams and num_choices < min_amount:
            dist = self.models[gram_count]
            key = self.key_for_gram_count(seq, gram_count)
            num_choices += len(dist[key])
            if num_choices < min_amount:
                gram_count -= 1

        logging.debug("Available choices: %i" % num_choices)

        assert(self.ngrams_decay_base > 1)
        pdict = dict()
        # Use random words from the input documents or the n-grams if there is enough of them.
        if(num_choices < min_amount):
           pdict = self.random_word_dict()
        else:
            # Merge all required probability distributions into one.
            for ng in range(max_grams, gram_count-1, -1):
                c = self.ngrams_decay_base ** (ng - gram_count)
                key = self.key_for_gram_count(seq, ng)
                pd = self.prob_dict(key, ng)
                pd = self.normalize_pdict(pd)
                pdict = self.merge_dicts(pdict, pd, c)

        # Add the end of sentence as a choice.
        pdict[s_terminator] = max(pdict.values()) * self.ngrams_terminator_probability
        pdict = self.normalize_pdict(pdict)

        # Update the distribution by LSTM. May terminate the sentence when LSTM thinks it is good to do so.
        if(self.lstm_enabled):
            pdict, top_word = self.lstm_prob(seq, pdict)
            if(top_word == s_terminator and random.uniform(0.0,1.0) < self.sure_terminate_prob):
                logging.debug('<eos> is the top word.')
                seq.append([s_terminator,'.'])
                return [True, seq]
        probs = nltk.DictionaryProbDist(pdict, normalize = True)

        # Choose the next word. Filter by POS or not.
        if(self.pos_tagger_enabled):
            tagged_choices = self.generate_tagged_choice(probs, min(num_choices, 20))
            c = self.first_good_choice(tagged_choices, seq)
            if c is None:
                return [False, seq]
            seq.append(c)
        else:
            c = probs.generate()
            if(c == s_terminator):
                tc = [[c,'.']]
            else:
                tc = self.posTagger.tag([c])
            seq.append(tc[0])
        return [True, seq]


    def next_instance(self):
        logging.info("Generating story, please wait...")

        if self.sentence_count == 0:
            self.out = self.startPhrase

        # Keep building a sentence until we hit a terminator
        while True:
            num_tokens = len(self.out)  # Number of tokens in current sentence
            logging.debug("Length: %s" % len(self.out))

            max_grams = min(self.max_grams, num_tokens + 1)
            min_grams = min(self.min_grams, num_tokens + 1)
            assert min_grams <= max_grams, "min grams > max grams !"

            [succeeded, self.out] = self.extend_sequence(min_grams, max_grams, self.out)

            # If we have no choices and have reached 2-gram, then end.
            if not succeeded:
                logging.debug("No valid choice found. Ending sentence with an ERROR.")
                logging.info
                self.out.append([".ERROR-no_choice", "."])
                break
            if self.is_terminator(self.out):
                break

        self.sentence_count += 1
        logging.debug("Sentence completed.")
        return embellish(self.out)


def run(num, shortname, text=""):
    today = datetime.now().strftime("%Y-%m-%d")
    with open("../output/tifu_%s.txt" % today, "a") as o:
        o.write("\n\n\n\n")
        o.flush()
        x = StoryGen(shortname, min_grams=2, max_grams=5, text=text)

        for i in range(0, num):
            logging.debug("Starting to generate sentence %i" % i)
            res = x.next_instance()
            if "".join(res.lower().split()) in x.text:
                # Alerts non-original sentences, we may not need this.
                logging.debug("NON-ORIGINAL sentence generated")
                logging.info(res + "    (NOT ORIGINAL)")
            else:
                logging.info(res)
            o.write(res + " ")
            o.flush()


def main(argv):
    #random.seed(123456789)
    args = parse_args()
    short_name = args.name
    verbose = args.verbose
    query = args.query
    setup_logging(verbose)
    # Generate a story from everything.
    if(query == ""):
        run(sentence_count, short_name)
        return
    # Retrieve documents by a user query and tell a story.
    docs = search.testLoading(query)
    if len(docs) < 1:
        print("No documents match your query.")
        return
    print("Writing a story based on {} documents.".format(len(docs)))
    text = ""
    # Merge all retrieved documents.
    for fn in docs:
        text += search.file_content(fn)
    run(sentence_count, short_name, text)





if __name__ == "__main__":
    main(sys.argv[1:])
