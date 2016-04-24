import ptb_word_lm as nn
lstm = nn.Lstm("model3.ckpt","simple-examples/data/ptb.train.txt")

def test_prediction(text):
    pred = lstm.predict(text)
    w, p = pred
    print(text)
    print(w[0:20])
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
