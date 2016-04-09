import sys
import re, string

def cleanfile_topics(filename):
    pattern = re.compile('[^a-z ]', re.UNICODE)
    with open(filename, 'r') as infile:
        text = infile.read().lower()
        text = re.sub('\n', ' ', text)
        text = pattern.sub('', text)
        return text

def cleanfile(filename):
    with open(filename, 'r') as infile:
        text = infile.read().lower()
        text = re.sub('\n', ' ', text)
        return text

def storybot_file(path, N):
    with open(path + 'storybot.txt', 'w') as file:
        for i in range (0, N):
            file.write(cleanfile(path + str(i) + '.txt'))

def topics_file(path, N):
    with open(path + 'topics.txt', 'w') as file:
        for i in range (0, N):
            file.write(cleanfile_topics(path + str(i) + '.txt') + '\n')

def main(argv):
    if len(argv) == 2:
        storybot_file(argv[0], int(argv[1]))
    elif len(argv) == 3:
        topics_file(argv[0], int(argv[1]))
    else:
        print("Insufficient arguments:")
        print("process_files.py [path] [N] [-t]")
        return

if __name__ == "__main__":
       main(sys.argv[1:])
