import sys

word_index = {}
next_index = 1
dictionary = []

def parseline(line):
    global word_index, next_index
    line_words = {}
    for word in line.split():
       if word in word_index:
          index = word_index[word]
       else:
           index = next_index
           word_index[word] = next_index
           dictionary.append(word)
           next_index += 1
       if index in line_words:
           line_words[index]+= 1
       else:
           line_words[index] = 1
    output = ''
    for index, count in line_words.items():
        output += str(index) + ':' + str(count) + ' '
    return output

def parseall(filename, outname):
    n_docs = 0
    with open(outname + '_tmp/parsed.txt', 'w') as o:
        with open(filename) as f:
             for n, line in enumerate(f):
                 n_docs += 1
                 o.write(str(n+1)+ ' ' + parseline(line) + '\n')
    with open(outname + '_tmp/dict.txt', 'w') as d:
        for word in dictionary:
            d.write(word+'\n')
    return next_index, n_docs

def main(argv):
    parseall(argv[0], argv[1])

if __name__ == "__main__":
       main(sys.argv[1:])

