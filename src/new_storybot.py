import sys
import argparse
import logging
import math
import nltk
from itertools import chain
from datetime import datetime

############################
# Configuration variables
############################
pos_training_path = "../lib/tagged/english-bidirectional-distsim.tagger"
pos_jar_path = "../lib/jar/stanford-postagger.jar"

# Minimum amount of choices for next word (otherwise lower gram).
min_amount = 3

# Sentence terminators. We want flowing stories, so skipping these for now.
terminator_types = ['.', ':']

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
        ["<s>", "today"],
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
    parser.add_argument("-v", "--verbose", action='store_true', help="Increase output verbosity")
    args = parser.parse_args()

    if args.name not in ["tifu"]:
        print("Wrong corpus name given. Must be one of: {tifu}")
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
    if tokens[0][0] == "<s>":
        tokens.pop(0)
    first = tokens[0][0].capitalize()
    middle = " ".join([x[0] for x in tokens[1:-1]])
    end = tokens[-1][0]
    return first + " " + middle + end
    
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
    


############################
# Main body of code
############################
class StoryGen:
    def __init__(self, shortname, min_grams=2, max_grams=5):
        self.posTagger = PosTagger('nltk')
        self.sentence_count = 0
        self.shortname = shortname
        self.min_grams = min_grams
        self.max_grams = max_grams

        (filepath, limits, startSeq, self.preferred, self.preferred_seq,
         self.term_except, smoothing_factory) = story_map[shortname]
        self.max_length, self.min_length, self.min_preferred = limits

        raw = open(filepath, 'r', encoding="utf8").read().lower()
        self.text = "".join(raw.split())

        # Split into sentences and tokenize
        tokenized_sentences = nltk.sent_tokenize(raw)
        for i, sentence in enumerate(tokenized_sentences):
            tokenized_sentences[i] = nltk.tokenize.word_tokenize(sentence)

        # Vocabulary
        words = [word for sentence in tokenized_sentences for word in sentence]
        self.vocabulary = set(words)

        logging.debug("Creating corpus...")
        self.models = [None] * (max_grams + 1)
        self.estimates = [None] * (max_grams + 1)

        logging.debug("Creating {0}-{1} grams models...".format(min_grams, max_grams))
        for n in range(min_grams, max_grams + 1):
            ngrams = [nltk.ngrams(sentence, n, pad_left=True, left_pad_symbol="<s>")
                      for sentence in tokenized_sentences]
            ngrams = list(chain.from_iterable(ngrams))
            formatted = []
            for grams in ngrams:
                prev = grams[:-1]
                res = grams[-1]
                formatted.append((prev, res))
            dist = nltk.ConditionalFreqDist(formatted)
            self.models[n] = dist
            self.estimates[n] = nltk.ConditionalProbDist(dist, smoothing_factory, bins=len(self.vocabulary))

        self.startPhrase = [[w, t] for (w, t) in self.posTagger.tag(startSeq)]
        

    def is_terminator(self, out):
        next_word, next_type = out[-1][0], out[-1][1]
        if next_type in terminator_types and next_word not in self.term_except:
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
        # If the current key is shorter than the gram count then pad with <s>
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

    def generate_tagged_choice(self, key, gram_count, num_choices):
        """
        :param key: the n-gram input
        :param gram_count: how large the n-gram is
        :param num_choices: how many candidate tokens should be returned
        :return: a list of randomly chosen candidate tokens, sorted by probability in descending order
        This method picks num_choices random tokens from the probability distribution and returns a list of
        distinct tagged tokens.
        """
        prob_dist = self.estimates[gram_count][key]
        choices = []
        for i in range(0, num_choices):
            token = prob_dist.generate()
            if token not in choices:
                choices.append(token)
        tagged_choices = self.posTagger.tag(choices)
        return tagged_choices
    
    # Add one word to the sequence seq, using gram_count ngrams model.
    def extend_sequence(self, gram_count, seq):
        succeeded = False
        dist = self.models[gram_count]
        key = self.key_for_gram_count(seq, gram_count)
        
        print(key)
        logging.debug("Key: %s" % (key,))

        num_choices = len(dist[key])
        logging.debug("Available choices: %i" % num_choices)
        if num_choices < min_amount and not gram_count == 2:
            logging.debug("Too few choices, retrying with smaller gram")
            return [succeeded, seq]
            
        # Try 10 or num_choices tokens. If none are OK, try smaller gram
        for i in range(0, 10):
            tagged_choice = self.generate_tagged_choice(key, gram_count, 1)
            next_word, next_type = tagged_choice[0]
            logging.debug("Candidate word: %s" % next_word)

            if not self.isAllowed(next_word, next_type, seq[-1], seq):
                continue
            else:
                succeeded = True
                seq.append([next_word, next_type])
                break
        return [succeeded, seq]

    def next_instance(self):
        logging.info("Generating story, please wait...")
        out = self.startPhrase if self.sentence_count == 0 else [["<s>", "NN"]]

        logging.info(" ".join([o[0] for o in out]))

        # Keep building a sentence until we hit a terminator
        while not self.is_terminator(out):
            succeeded = False
            num_tokens = len(out)  # Number of tokens in current sentence
            logging.debug("Length: %s" % len(out))

            max_grams = min(self.max_grams, num_tokens + 1)
            min_grams = min(self.min_grams, num_tokens + 1)
            assert min_grams <= max_grams, "min grams > max grams !"

            # Go backwards through the number of grams
            for gram_count in range(max_grams, min_grams - 1, -1):
                if succeeded:
                    break

                logging.debug("Trying %i-grams" % gram_count)
                [succeeded, out] = self.extend_sequence(gram_count, out)

                # If we have no choices and have reached 2-gram, then end.
                if not succeeded:
                    if gram_count > 2:
                        logging.debug("No valid choice found for %i-gram. Continuing" % gram_count)
                        continue
                    else:
                        logging.debug("No valid choice found for 2-gram. Ending sentence.")
                        logging.info
                        out.append([".", "."])
                        break  # breaks out of the 'for gram_count' loop above

                if succeeded:
                    break

        self.sentence_count += 1
        logging.debug("Sentence completed.")
        return embellish(out)


def run(num, shortname):
    today = datetime.now().strftime("%Y-%m-%d")
    with open("../output/tifu_%s.txt" % today, "a") as o:
        o.write("\n\n\n\n")
        o.flush()
        x = StoryGen(shortname, min_grams=2, max_grams=4)

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
    args = parse_args()
    short_name = args.name
    verbose = args.verbose

    setup_logging(verbose)
    run(5, short_name)


if __name__ == "__main__":
    main(sys.argv[1:])


