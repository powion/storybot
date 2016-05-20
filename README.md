# storybot

Storytelling bot for Information Retrieval project. The project website with sample generated stories is at https://powion.github.io/storybot/.

# Usage

Run src/storybot.py using
```
python storybot.py -n [pride|tolkien]
```
to have storybot start writing stories at about 0.5 wps. 
Optionally -v can be added for verbose output, specifying what options the program chooses from for each word.

The script ptb_word_lm.py in src/lstm can be executed when training a new LSTM model. src/create_lstm_dataset.py preprocesses any text file and creates a dataset folder. ptb_word_lm.py can then run training on this dataset.

# Install Dependencies in Ubuntu


Install PIP for Python 3, NLTK, punkt tokenizer and averaged_perceptron_tagger POS tagger

```
sudo apt-get install python3-pip
sudo pip3 install nltk
sudo mkdir /usr/share/nltk_data
sudo python3
>> import nltk
>> nltk.download()
>>c
>>d
>>/usr/share/nltk_data
>>m
# and download the "punkt" tokenizer
>>d
>>punkt
# also download averaged_perceptron_tagger the same way
```
, Whoosh, a search engine for Python
```
sudo pip3 install Whoosh
```
and finally TensorFlow and numpy.
```
sudo pip3 install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.8.0-cp34-cp34m-linux_x86_64.whl
sudo apt-get install python3-numpy
```
