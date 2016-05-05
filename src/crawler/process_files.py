import sys
import re, string

all_patterns = [
              re.compile('[^a-z ]', re.UNICODE),
              re.compile('(\w*http\w+\s?|\w+http\w*\s?)', re.UNICODE),
              re.compile('http[^\s]+', re.UNICODE)
        ]

def cleanfile(filename, patterns):
    with open(filename, 'r') as infile:
        text = infile.read().lower()
        text = re.sub('\n', ' ', text)
        for pattern in patterns:
            text = pattern.sub('', text)
        text = re.sub('\s+', ' ', text)
        return text

def process_file(path, outname, patterns, lineend):
    with open(path + outname + '.txt', 'w') as file:
        i = 0
        try:
            while True:
                file.write(cleanfile(path + str(i) + '.txt', patterns) + lineend)
                i += 1
        except IOError:
            print(i, 'files processed.')
            return

def main(argv):
    if len(argv) == 1:
        process_file(argv[0], 'storybot', [all_patterns[2]], '')
    elif len(argv) == 2:
        process_file(argv[0], 'topics', all_patterns[:2], '\n')
    else:
        print("Insufficient arguments:")
        print("process_files.py path [-t]")
        return

if __name__ == "__main__":
       main(sys.argv[1:])
