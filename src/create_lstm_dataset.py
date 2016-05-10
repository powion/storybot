import sys
import os
import new_storybot
import operator
from collections import Counter


if(len(sys.argv) != 3):
    print("Run this program as python3 create_lstm_dataset.py /path/to/input.txt /output/directory. \n"
          "e.g. python3 create_lstm_dataset.py ../datasets/tifu/storybot.txt ../datasets/tifu_lstm/")
    exit()
filepath = sys.argv[1]
data_path = sys.argv[2] # "../datasets/tifu_lstm"

vocab_limit = 10000
# special tokens: <unk>, (<eos>)
special_tokens = 1
# train, validate, test
data_split = [0.85, 0.1, 0.05]
data_files = ["ptb.train.txt", "ptb.valid.txt", "ptb.test.txt"]

#### Get text (and then list of words) via new_storybot. #####
# words = ['hello', '<eos>', 'my', '<eos>', 'friends', '<eos>']
text = open(filepath, 'r', encoding="utf8").read().lower()
words = new_storybot.text2words(text)
s_terminator = new_storybot.s_terminator
##############################################################

n_sentences = words.count(s_terminator)
assert(n_sentences > 200)

# Split the text into train, validate and test subsets. Keep sentences intact.
def split_dataset(words, data_split, s_term):
    dsum = sum(data_split)
    assert(dsum < 1.00001 and dsum > 0.99999)
    n_sentences = words.count(s_term)
    sentences_done = 0
    pos = 0
    split_no = 0
    spsum = 0
    w = ''
    out = []
    for sp in data_split:
        out_split = []
        spsum += sp
        # Process sentences for one data subset.
        while sentences_done < spsum*n_sentences:
            # Process one sentence.
            while not w==s_term:
                w = words[pos]
                out_split.append(w)
                pos += 1
            sentences_done += 1
            w = ''
        out += [out_split]
        split_no += 1
    return out
    
# Write words into a text file. Use '\n' instead of s_terminator. Add whitespaces as required.
def write_words(fn, words, s_term):
    with open(fn, 'w') as f:
        # Write a space at the begining of each output text file
        # to match the original ptb dataset format.
        f.write(' ')
        for w in words:
            if w==s_term:
                w = '\n '
            else:
                w += ' '
            f.write(w)

# Create a limited dictionary of vocabulary.
def vocabulary_ltd(words):
    top_words = Counter(words).most_common(vocab_limit - special_tokens)
    wdict = dict(top_words)
    return wdict
 
# Replace words unknown to the dictionary by '<unk>'.
def words_ltd(words, wdict):
    new_words = []
    # Substitute less common words by <unk>.
    for w in words:
        if w in wdict:
            new_words.append(w)
        else:
            new_words.append('<unk>')
    return new_words

# Split the dataset -> train, validate, test.
dsplit = split_dataset(words, data_split, s_terminator)
# Build a dictionary from the training set.
wdict = vocabulary_ltd(dsplit[0])

# Filter everything with the dictionary and write out to files.
for i in range(0, len(data_files)):
    new_words = words_ltd(dsplit[i], wdict)
    fn = os.path.join(data_path, data_files[i])
    write_words(fn, new_words, s_terminator)



