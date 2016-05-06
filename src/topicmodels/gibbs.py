from __future__ import division

import os
import sys
from datetime import datetime

import vocabparser

import numpy as np
from scipy.spatial.distance import cdist

# Constants
K = 25
alpha = 0.3
beta = 0.3
conv_iterations = 400
samples = 50
sample_interval = 5

# Current time in format [HH:MM]
def timestr():
  return "[{}]".format(datetime.now().strftime('%H:%M'))

# Create W matrix
def create_W():
  if(os.path.isfile('tmp/Wmatrix.npy')):
    return np.load('tmp/Wmatrix.npy')
  file = open('tmp/parsed.txt')
  W = np.zeros((1,2))
  document = 0
  for line in file:
    ns = line.split()
    for i in range (1, len(ns)):
      woc = ns[i].split(':')
      word = int(woc[0])
      occs = int(woc[1])
      for j in range (0, occs):
        row = np.array([document, word])
        W = np.vstack((W, row))
    document = document + 1
    if document%100 == 0:
      print('Parsed ' + document + 'documents.')
  W = np.delete(W, 0, axis = 0)
  np.save('tmp/Wmatrix', W)
  return W

def init_matrices():
  for i in range (0, Z.size):
    d, w = W[i]
    j = Z[i]
    VT[w, j] += 1
    TW[j] += 1
    DT[d, j] += 1
    DW[d] += 1

def prob(j, d, w):
  phi = (VT[w, j]+beta)/(TW[j]+V*beta)
  theta = (DT[d, j]+alpha)/(DW[d]-1+K*alpha)
  return phi*theta

def gibbs_step(i):
  d, w = W[i]
  j = Z[i]
  jOld = j
  # Remove word / topic combo
  VT[w, j] -= 1
  TW[j] -= 1
  DT[d, j] -= 1
  zprob = np.zeros(K)
  for k in range (0, K):
    zprob[k] = prob(k, d, w)
  zprob = zprob / sum(zprob)
  j = np.where(np.random.multinomial(1, zprob) == 1)[0][0]
  Z[i] = j
  VT[w, j] += 1
  TW[j] += 1
  DT[d, j] += 1
  if (jOld == j):
    return 0
  else:
    return 1

# Runs the specified number of iterations, or less if the changes
# stay under 35% for 10 consecutive iterations.
def gibbs(iterations):
  convergence_counter = 0
  for it in range (0, iterations):
    changes = 0
    for i in range (0, Z.size):
      changes += gibbs_step(i)
    if (it != 0 and it % 10 == 0):
      print(timestr() +
            " Iteration {} out of {}, changes: ".format(it, iterations) + 
            "{:.0%}".format(changes/Z.size))
    if (changes/Z.size < 0.35):
      if(convergence_counter > 10):
        np.save('tmp/convergedZ', Z)
        return
      convergence_counter += 1
    else:
      convergence_counter = 0
    np.save('tmp/convergedZ', Z)

def sample(n, interval):
  DT_copy = np.array(DT)
  for i in range (0, n-1):
    gibbs(interval)
    DT_copy += DT
    print(timestr() +
            " Sample {} out of {}.".format(i, n))
  np.save('tmp/DT', DT_copy)
  DT_copy = DT_copy/n
  DT_copy = DT_copy/sum(DT_copy)
  return DT_copy

def main(inputfile, outputname):
  global Z, W, V, D, VT, TW, DT, DW
  # Create necessary dirs
  if not os.path.exists('tmp'):
    os.makedirs('tmp')
  if not os.path.exists('matrices'):
    os.makedirs('matrices')

  # V: Vocabulary size, D: Number of documents
  V, D = vocabparser.parseall(inputfile)
  # W: For each word, one entry [document index, word index]
  W = create_W()
  # Most probable topic for each word
  Z = np.random.randint(0, K, W.shape[0])
  # Word index -> topic -> num
  VT = np.zeros((V, K))
  # Topic -> num words
  TW = np.zeros(K)
  # Document -> topic -> num
  DT = np.zeros((D, K))
  # Document -> num words (only immutable one)
  DW = np.zeros(D)

  init_matrices()
  print(timestr() + " Running {} iterations, please wait.".format(conv_iterations))
  gibbs(conv_iterations)
  print(timestr() + " Sampling {} times, please wait.".format(samples))
  DT_samples = sample(samples, sample_interval)

  # Calculate distance matrix
  dists = cdist(DT_samples, DT_samples)
  np.save('matrices/' + outputname, dists)

  return dists

if __name__ == "__main__":
  if len(sys.argv) != 3:
    print('Insufficient arguments: python gibbs.py inputfile outname')
  main(sys.argv[1], sys.argv[2])