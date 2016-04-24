# storybot

Storytelling bot for Information Retrieval project.

# Usage

Run src/storybot.py using
```
python storybot.py -n [pride|tolkien]
```
to have storybot start writing stories at about 0.5 wps. 
Optionally -v can be added for verbose output, specifying what options the program chooses from for each word.

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
