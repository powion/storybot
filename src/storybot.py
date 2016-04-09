import getopt
import math
import nltk
import os
import random
import sys

pos_training_path = "../lib/tagged/english-bidirectional-distsim.tagger"
pos_jar_path = "../lib/jar/stanford-postagger.jar"

VERBOSE = False

# Max amount of choices for next word.
top_amount = 20
# Minimum amount of choices for next word (otherwise lower gram).
min_amount = 1
# Max value of n for n-gram.
grams_top = 5

# Sentence terminators. We want flowing stories, so skipping these for now.
# terminator_types = ['.', ':']
terminator_types = []

# E.g. adjectives can not end sentences (it tends to give bad results).
forbidden_type_sequences = {
    "ADJ" : [".", ":"],
    "IN" : [".", ":"],
    "JJ" : [".", ":", "VB"],
    "RB" : [".", ":"],
    "VBZ" : [".", ":"],
    "POS" : [".", ":"],
    "." : [".", ":"]
}

forbidden_types = ["``", "''", "CD", ":"]

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
    "pride" : ["../lib/datasets/prideandprejudice.txt",
               [1000, 0, 0],
               ["i", "feel"],
               [],
               [],
               [],
               nltk.MLEProbDist],
    "tolkien" : ["../lib/datasets/tolkien.txt",
               [1000, 0, 0],
               ["frodo", "was"],
               [],
               [],
               [],
               nltk.MLEProbDist],
    "tifu" : ["../datasets/tifu/storybot.txt",
               [1000, 0, 0],
               ["today", "i"],
               [],
               [],
               [],
               nltk.MLEProbDist]
}

class StoryGen:
    def __init__(self, shortname, min_grams=2, max_grams=5):
        self.shortname = shortname
        self.min_grams = min_grams
        self.max_grams = max_grams

        (filepath, limits, startSeq, self.preferred, self.preferred_seq,
        self.term_except, smoothing_factory) = story_map[shortname]
        self.max_length, self.min_length, self.min_preferred = limits

        raw = open(filepath, 'r').read()
        tokens = nltk.word_tokenize(raw)
        words = [w.lower() for w in tokens]
        self.vocabulary = set(words)
        print("Creating corpus...", file=sys.stderr)

        # used for originality checking, remove whitespace and lower case
        self.text = "".join(raw.lower().split())

        self.models = [None] * (max_grams+1)
        self.estimates = [None] * (max_grams+1)

        print("Creating {0}-{1} grams models...".format(min_grams, max_grams),
              file=sys.stderr)
        for n in range(min_grams, max_grams+1):
            ngrams = nltk.ngrams(words, n)
            formatted = []
            for grams in ngrams:
                prev = grams[:-1]
                res = grams[-1]
                formatted.append((prev, res))
            dist = nltk.ConditionalFreqDist(formatted)
            self.models[n] = dist
            self.estimates[n] = nltk.ConditionalProbDist(dist,
                smoothing_factory, bins=len(self.vocabulary))

        self.posTagger = nltk.StanfordPOSTagger(pos_training_path, pos_jar_path)
        self.startPhrase = [[w, t] for (w,t) in self.posTagger.tag(startSeq)]

    def nextInstance(self):
        print("Generating story, please wait...", file=sys.stderr)
        out = self.startPhrase[:]
        usedPreference = False
        prefSeqIndex = 0
        succeeded = True

        num_tries = 0 #So we don't get stuck

        # Start printing with the starting phrase.
        for i in range (0, len(out)-1):
            print(out[i][0], end=" ", flush=True)

        # last token type != terminator
        while not self.isTerminator(out[-1][0], out[-1][1]):

            print(out[-1][0], end=" ", flush=True)

            num_tries = num_tries + 1
            if num_tries > 10:
                out.pop()
                num_tries = 0

            if not succeeded:
                if VERBOSE: print("Retrying...", file=sys.stderr)
            succeeded = False

            num_prev = len(out)
            if VERBOSE: print("Length: ", len(out), file=sys.stderr)

            max_grams = min(self.max_grams, num_prev+1)
            min_grams = min(self.min_grams, num_prev+1)
            assert min_grams != max_grams

            for grams in range(max_grams, min_grams-1, -1):
                if succeeded:
                    break

                if VERBOSE: print("Trying {0}-grams".format(grams),
                                  file=sys.stderr)

                dist = self.models[grams]
                word = out[-1]

                amountBack = grams-1
                prevWords = tuple((x[0] for x in out[-amountBack:]))
                if VERBOSE: print("Prev: ", prevWords, file=sys.stderr)

                most_common = (
                [x[0] for x in dist[prevWords].most_common(top_amount)])
                estimates = self.estimates[grams][prevWords]

                if VERBOSE:
                    print("Most common: {0} choices".format(len(most_common)),
                    file=sys.stderr)

                if len(most_common) < min_amount and not grams == 2:
                    # try next gram
                    continue

                if VERBOSE: print("Most common: ", most_common, file=sys.stderr)

                taggedMostCommon = self.posTagger.tag(most_common);

                # take the only choice
                if len(taggedMostCommon) == 1:
                    next_word, next_type = taggedMostCommon[0]
                    out.append([next_word, next_type])
                    succeeded = True
                    break

                allowed = []

                for next_word, next_type in taggedMostCommon:
                    if not self.isAllowed(next_word, next_type, word, out):
                        continue

                    allowed.append([next_word, next_type])

                # filter allowed, sometimes the estimates are non-positive
                allowed = [[w, t] for w,t in allowed if estimates.prob(w) > 0]

                if VERBOSE:
                    print("Allowed: {0} choices".format(len(allowed)),
                        file=sys.stderr)
                if VERBOSE:
                    print("Allowed: ", [x[0] for x in allowed], file=sys.stderr)

                if len(allowed) == 0:
                    if grams > 2:
                        continue
                    else:
                        out.append([".", "."])
                        succeeded = True
                        break

                # prefer termination
                if len(out) > self.max_length:
                    for next_word, next_type in allowed:
                        if self.isTerminator(next_word, next_type):
                            succeeded = True
                            out.append([next_word, next_type])
                            num_tries = 0
                            break

                if succeeded:
                    break

                # try preference words
                if len(self.preferred) > 0:
                    for next_word, next_type in allowed:
                        if next_word in self.preferred:
                            succeeded = True
                            out.append([next_word, next_type])
                            num_tries = 0
                            break

                if succeeded:
                    break

                # try preference sequence
                if prefSeqIndex < len(self.preferred_seq)-1:
                    if word[0] == self.preferred_seq[prefSeqIndex]:
                        for next_word, next_type in allowed:
                            if next_word == self.preferred_seq[prefSeqIndex+1]:
                                succeeded = True
                                prefSeqIndex += 1
                                out.append([next_word, next_type])
                                num_tries = 0
                                break

                if succeeded:
                    break

                probs = [estimates.prob(w) for w, _ in allowed]
                normalized = normalize(probs)

                # pick weighted choice
                choice = random.random()
                prob = 0 # cumulative probability
                allowed_with_prob = zip(allowed, normalized)
                for next_tuple, next_prob in allowed_with_prob:
                    if prob + next_prob >= choice:
                        out.append(next_tuple)
                        succeeded = True
                        break
                    prob += next_prob

        #print(out, file=sys.stdout)
        return embellish(out)

    # Check if a word is allowed, depending on word, type, previous word,
    # and the full sequence.
    def isAllowed(self, next_word, next_type, word, out):
        # Do not put preferred word too early, decided by min_preferred.
        if len(out) < self.min_preferred and next_word in self.preferred:
            return False

        # Only use preferred word once.
        if next_word in self.preferred and next_word in [x[0] for x in out]:
            return False

        # Do not terminate sentence before preferred word.
        if self.isTerminator(next_word, next_type):
            for pref in self.preferred:
                if pref not in [x[0] for x in out]:
                    return False

        # Do not terminate too early.
        if (len(out) < self.min_length and
            self.isTerminator(next_word, next_type)):
            return False

        # Check if the sequence is forbidden, e.g. terminator after adjective.
        if (word[1] in forbidden_type_sequences and
            next_type in forbidden_type_sequences[word[1]]):
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

    # Some memes do not end on any terminator, e.g. Wonka has "?" in the middle.
    def isTerminator(self, next_word, next_type):
        if next_type in terminator_types and next_word not in self.term_except:
            return True

def normalize(prob_list):
    prob_sum = sum(prob_list)
    return [math.exp(math.log(p) - math.log(prob_sum)) for p in prob_list]

def embellish(tokens):
    first = tokens[0][0].capitalize()
    middle = " ".join([x[0] for x in tokens[1:-1]])
    end = tokens[-1][0]
    return first + " " + middle + end

def run(num, shortname):
    x = StoryGen(shortname)

    for _ in range(0, num):
        res = x.nextInstance()
        if "".join(res.lower().split()) in x.text:
            # Alerts non-original sentences, we may not need this.
            print(res + " NON-ORIGINAL")
        else:
            print(res)

def main(argv):
   shortname = ''
   try:
      opts, args = getopt.getopt(argv,"n:v",)
   except getopt.GetoptError:
       print('Error: No shortname provided.', file=sys.stderr)
       print('Available shortnames: TBA',
             file=sys.stderr)
       print('Sample use: storybot.py -n tifu', file=sys.stderr)
       sys.exit(2)
   for opt, arg in opts:
      if opt == '-n':
          shortname = arg
          if shortname not in story_map:
              print('Error: Invalid shortname.', file=sys.stderr)
              print('Available shortnames: TBA',
                    file=sys.stderr)
              sys.exit(2)
      if opt == '-v':
          VERBOSE = True
   run(1, shortname)

if __name__ == "__main__":
   main(sys.argv[1:])
