import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import ptb_word_lm as nn
import random

max_lstm_steps = 8
draw_from = 20
lstm = nn.Lstm("model5.ckpt","simple-examples/data/ptb.train.txt", max_lstm_steps)

def random_lstm_story(start, count):
    text = start
    for i in range(count):
        while True:
            roll_begin = max(0, len(text) - max_lstm_steps)
            pred = lstm.predict_sorted(text[roll_begin:])
            w, p = pred
            if(w[0] == "<eos>"):
                text.append(w[0])
            else:
                text.append(w[random.randint(0, draw_from)])
            if(text[-1]=="<eos>"):
                break
    return text

def test_prediction(text):
    pred = lstm.predict_sorted(text)
    w, p = pred
    print("The input text: {}".format(text))
    print("likely continues by one of: {}".format(w[0:20]))
    print("--------")
    
test_prediction(["today", "i"])
test_prediction(["he"])
test_prediction(["we", "met"])
test_prediction(["we", "met", "her"])
test_prediction(["mary", "had"])
test_prediction(["my", "father"])
test_prediction(["why", "is"])
test_prediction(["where", "is"])
test_prediction(["where", "are"])
test_prediction(["where", "are", "those"])
test_prediction(["where", "are", "those", "happy"])
test_prediction(["where", "are", "those", "happy", "days"])
test_prediction(["have"])
test_prediction(["have","you"])
test_prediction(["have","you","ever"])
test_prediction(["have","you","ever","seen"])
test_prediction(["have","you","ever","seen","the"])
test_prediction(["have","you","ever","seen","the","rain"])

print("And now stand by for a complete story...")

print(random_lstm_story(["the", "company"], 8))
