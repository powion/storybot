import sys 
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))

from crawler.process_files import all_patterns, cleanfile

import numpy as np

def get_indices(n, matrix_path):
  dists = np.load(matrix_path)
  i = np.random.randint(dists.shape[0])
  return np.argpartition(dists[i], n)[:n]

def cluster(n, doc_path, matrix_path):
  indices = get_indices(n, matrix_path)
  with open(doc_path + 'topic_storybot.txt', 'w') as file:
    for index in indices:
      file.write(cleanfile(doc_path + str(index) + '.txt', [all_patterns[2]]))

if __name__ == "__main__":
    if len(sys.argv) != 4:
      print('Insufficient arguments.')
      print('python cluster_files.py n doc_path matrix_path')
    cluster(int(sys.argv[1]), sys.argv[2], sys.argv[3])